"""
Data Transformation Functions for V1.0: Small Batch Processing (Pandas)

This module contains Silver and Gold layer transformation logic for small batches (<=10k records).
Uses Pandas for efficient, in-memory data processing.

Transformations:
- Silver Layer: Data cleaning, deduplication, standardization
- Gold Layer: Business logic, aggregations, dimensional modeling
"""

import pandas as pd
import json
import logging
import os
import importlib
from typing import Dict, List
from datetime import datetime
from transformations.pandas.tables.user import transform_user_data

logger = logging.getLogger(__name__)

# Dynamically discover available transformation functions
def _discover_entity_transforms() -> Dict[str, callable]:
    """
    Automatically discover transformation functions from the tables folder.
    
    Looks for modules with functions named transform_{entity}_data.
    Falls back to manual processing for entities without dedicated transforms.
    """
    entity_transforms = {}
    tables_dir = os.path.dirname(__file__) + '/tables'
    
    if not os.path.exists(tables_dir):
        logger.warning(f"Tables directory not found: {tables_dir}")
        return entity_transforms
    
    # Scan for Python files in tables directory
    for filename in os.listdir(tables_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # Remove .py extension
            
            try:
                # Import the module
                module_path = f'transformations.pandas.tables.{module_name}'
                module = importlib.import_module(module_path)
                
                # Look for transform function
                transform_func_name = f'transform_{module_name}_data'
                if hasattr(module, transform_func_name):
                    entity_transforms[module_name] = getattr(module, transform_func_name)
                    logger.info(f"Found transformation function for {module_name}: {transform_func_name}")
                    
            except ImportError as e:
                logger.debug(f"Could not import {module_path}: {e}")
            except Exception as e:
                logger.warning(f"Error processing {module_name}: {e}")
    
    return entity_transforms


class PandasTransformer:
    """Transform raw e-commerce data through Medallion architecture layers (Pandas-based)"""
    
    def __init__(self):
        """Initialize transformer"""
        self.records_processed = 0
        self.transformation_log = []
        self.entity_transforms = _discover_entity_transforms()
    
    def transform_to_silver(self, raw_data: List[Dict]) -> pd.DataFrame:
        """
        Transform raw data to Silver layer (cleaned, standardized).
        
        **Data Source:** Bronze layer (shanlee-raw-data/{userId}/{jobId}.json)
        **Data Destination:** Silver layer (silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet)
        **Purpose:** Clean, deduplicate, and standardize raw data for analytics
        
        Automatically discovers and uses transformation functions from the tables folder.
        Only processes entities that have dedicated transformation functions.
        
        Operations:
        1. Auto-discover entity transformation functions from tables/*.py modules
        2. Apply entity-specific transformation functions for discovered entities
        3. Data type conversion and standardization
        4. Remove duplicates by entity keys
        5. Handle missing values and validation
        
        Args:
            raw_data: List of raw record dictionaries from Bronze layer
            
        Returns:
            DataFrame with Silver layer structure
        """
        try:
            self.records_processed = len(raw_data)
            
            # Process all entities with available transformation functions
            entity_dataframes = {}
            
            for entity_type, transform_func in self.entity_transforms.items():
                # Use centralized transformation function
                raw_entity_df = pd.DataFrame({entity_type: [record.get(entity_type, {}) for record in raw_data]})
                entity_df = transform_func(raw_entity_df)
                entity_dataframes[entity_type] = entity_df
            
            # Extract DataFrames for easier access
            users_df = entity_dataframes['user']
            
            # Combine into single Silver layer DataFrame
            silver_df = pd.DataFrame({
                'record_type': ['user'] * len(users_df),
                'user_id': users_df['id'],
                'entity_id': users_df['id'],
                'email': users_df['email'],
                'phone': users_df['phone_number'],
                'age': users_df['age'],
                'processing_timestamp': datetime.utcnow().isoformat()
            })
            
            return silver_df
            
        except Exception as e:
            logger.error(f"Error transforming to Silver layer: {str(e)}")
            raise
    
    def transform_to_gold(self, silver_df: pd.DataFrame) -> Tuple[Dict[str, pd.DataFrame], Dict]:
        """
        Transform Silver layer data to Gold layer (aggregated, business-ready).
        
        Creates dimensional tables:
        1. dim_users: User demographic dimensions
        2. dim_time: Time dimension
        3. fact_orders: Order facts
        4. agg_user_metrics: User analytics aggregations
        
        Args:
            silver_df: Silver layer DataFrame
            
        Returns:
            Tuple of (dict of DataFrames, metadata)
        """
        try:
            start_time = datetime.now()
            gold_tables = {}
            
            # Create dim_users
            dim_users = silver_df[silver_df['record_type'] == 'user'][
                ['user_id', 'email', 'age']
            ].drop_duplicates()
            dim_users['age_group'] = pd.cut(
                dim_users['age'],
                bins=[0, 18, 25, 35, 50, 65, 100],
                labels=['<18', '18-24', '25-34', '35-49', '50-64', '65+']
            )
            gold_tables['dim_users'] = dim_users
            
            # Create dim_time
            time_data = []
            base_date = pd.Timestamp.now().date()
            for i in range(365):
                current_date = base_date - pd.Timedelta(days=i)
                time_data.append({
                    'date_id': int(current_date.strftime('%Y%m%d')),
                    'date': current_date,
                    'day_of_week': current_date.strftime('%A'),
                    'month': current_date.month,
                    'year': current_date.year,
                    'quarter': (current_date.month - 1) // 3 + 1
                })
            dim_time = pd.DataFrame(time_data)
            gold_tables['dim_time'] = dim_time
            
            # Create fact tables
            fact_orders = silver_df[silver_df['record_type'] == 'user'].agg({
                'user_id': 'count',
                'email': 'count'
            }).reset_index()
            fact_orders.columns = ['user_id', 'order_count']
            gold_tables['fact_orders'] = fact_orders
            
            # Create aggregations
            agg_metrics = silver_df.groupby('user_id').agg({
                'email': 'first',
                'age': 'first'
            }).reset_index()
            agg_metrics.columns = ['user_id', 'email', 'age']
            gold_tables['agg_user_metrics'] = agg_metrics
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            metadata = {
                'layer': 'gold',
                'tables_created': list(gold_tables.keys()),
                'total_rows_gold': sum(len(df) for df in gold_tables.values()),
                'processing_duration_seconds': duration,
                'transformation_timestamp': start_time.isoformat()
            }
            
            logger.info(f"Gold transformation complete: {metadata}")
            return gold_tables, metadata
            
        except Exception as e:
            logger.error(f"Error transforming to Gold layer: {str(e)}")
            raise
    

def json_to_dataframe(json_data: str) -> List[Dict]:
    """
    Parse JSON data from blob storage into list of records.
    
    Args:
        json_data: JSON string from blob
        
    Returns:
        List of record dictionaries
    """
    try:
        return json.loads(json_data)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {str(e)}")
        raise


def dataframe_to_parquet(df: pd.DataFrame, path: str) -> None:
    """
    Save DataFrame as Parquet for ADLS Gen2.
    
    Args:
        df: DataFrame to save
        path: Output path
    """
    try:
        df.to_parquet(path, index=False, compression='snappy')
        logger.info(f"Saved {len(df)} rows to {path}")
    except Exception as e:
        logger.error(f"Failed to save Parquet: {str(e)}")
        raise
