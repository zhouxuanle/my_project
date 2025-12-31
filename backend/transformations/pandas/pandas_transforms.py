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
from typing import Dict, Tuple, List
from datetime import datetime
from transformations.pandas.tables.users import clean_users, calculate_quality_score
from transformations.pandas.tables.addresses import clean_addresses
from transformations.pandas.tables.orders import clean_orders

logger = logging.getLogger(__name__)


class PandasTransformer:
    """Transform raw e-commerce data through Medallion architecture layers (Pandas-based)"""
    
    def __init__(self):
        """Initialize transformer"""
        self.records_processed = 0
        self.records_cleaned = 0
        self.transformation_log = []
    
    def transform_to_silver(self, raw_data: List[Dict]) -> Tuple[pd.DataFrame, Dict]:
        """
        Transform raw data to Silver layer (cleaned, standardized).
        
        **Data Source:** Bronze layer (shanlee-raw-data/{userId}/{jobId}.json)
        **Data Destination:** Silver layer (silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet)
        **Purpose:** Clean, deduplicate, and standardize raw data for analytics
        
        Operations:
        1. Flatten nested data structure from Bronze layer
        2. Data type conversion
        3. Remove duplicates by user_id (deduplication)
        4. Standardize formats (email, phone, dates to ISO 8601)
        5. Handle missing values (null handling)
        6. Validate key fields (email regex, phone format, age range)
        7. Calculate data quality scores (0-100)
        
        Args:
            raw_data: List of raw record dictionaries from Bronze layer
            
        Returns:
            Tuple of (DataFrame with Silver layer structure, metadata dict with stats)
        """
        try:
            start_time = datetime.now()
            self.records_processed = len(raw_data)
            
            # Flatten raw data into individual DataFrames
            users_list = []
            addresses_list = []
            products_list = []
            orders_list = []
            
            for record in raw_data:
                # Extract user entity
                user = record.get('user', {})
                users_list.append({
                    'user_id': user.get('id'),
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'phone': user.get('phone_number'),
                    'sex': user.get('sex'),
                    'age': user.get('age'),
                    'created_at': user.get('create_time')
                })
                
                # Extract address entity
                address = record.get('address', {})
                addresses_list.append({
                    'address_id': address.get('id'),
                    'user_id': address.get('user_id'),
                    'city': address.get('city'),
                    'country': address.get('country'),
                    'postal_code': address.get('postal_code'),
                    'created_at': address.get('create_time')
                })
                
                # Extract product entity
                product = record.get('product', {})
                products_list.append({
                    'product_id': product.get('id'),
                    'name': product.get('name'),
                    'category_id': product.get('category_id'),
                    'created_at': product.get('create_time')
                })
                
                # Extract order entity
                order = record.get('order', {})
                orders_list.append({
                    'order_id': order.get('id'),
                    'user_id': order.get('user_id'),
                    'created_at': order.get('create_time')
                })
            
            # Convert to DataFrames
            users_df = pd.DataFrame(users_list)
            addresses_df = pd.DataFrame(addresses_list)
            products_df = pd.DataFrame(products_list)
            orders_df = pd.DataFrame(orders_list)
            
            # Perform cleaning operations
            users_df = clean_users(users_df)
            orders_df = clean_orders(orders_df)
            addresses_df = clean_addresses(addresses_df)
            
            # Remove duplicates
            initial_user_count = len(users_df)
            users_df = users_df.drop_duplicates(subset=['user_id'], keep='first')
            self.records_cleaned += (initial_user_count - len(users_df))
            
            # Combine into single Silver layer DataFrame
            silver_df = pd.DataFrame({
                'record_type': ['user'] * len(users_df),
                'user_id': users_df['user_id'],
                'entity_id': users_df['user_id'],
                'email': users_df['email'],
                'phone': users_df['phone'],
                'age': users_df['age'],
                'quality_score': calculate_quality_score(users_df),
                'processing_timestamp': datetime.utcnow().isoformat()
            })
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            metadata = {
                'layer': 'silver',
                'total_records_processed': self.records_processed,
                'total_records_cleaned': len(silver_df),
                'duplicates_removed': self.records_cleaned,
                'quality_score_avg': silver_df['quality_score'].mean(),
                'processing_duration_seconds': duration,
                'transformation_timestamp': start_time.isoformat()
            }
            
            logger.info(f"Silver transformation complete: {metadata}")
            return silver_df, metadata
            
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
                'age': 'first',
                'quality_score': 'mean'
            }).reset_index()
            agg_metrics.columns = ['user_id', 'email', 'age', 'avg_quality_score']
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
