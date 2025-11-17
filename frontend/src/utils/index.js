import { BREAKPOINTS, DATA_COUNT_LIMITS } from '../constants';

// Utility function to calculate max columns based on window width
export function getMaxColumns(windowWidth, totalColumns) {
  if (windowWidth < BREAKPOINTS.SMALL) {
    return Math.max(2, totalColumns - 6);
  } else if (windowWidth < BREAKPOINTS.MEDIUM) {
    return Math.max(3, totalColumns - 4);
  } else if (windowWidth < BREAKPOINTS.LARGE) {
    return Math.max(4, totalColumns - 3);
  }
  return totalColumns;
}

// Utility function to get visible columns/fields with created_at always at the end
export function getVisibleColumnsAndFields(config, maxColumns) {
  const { columns, fields } = config;
  const createdAtIndex = fields.indexOf('created_at');
  
  if (createdAtIndex === -1) {
    // No created_at column, just slice normally
    return {
      visibleColumns: columns.slice(0, maxColumns),
      visibleFields: fields.slice(0, maxColumns)
    };
  }
  
  // Remove created_at from arrays temporarily
  const columnsWithoutCreatedAt = columns.filter((_, idx) => idx !== createdAtIndex);
  const fieldsWithoutCreatedAt = fields.filter(field => field !== 'created_at');
  
  // Take up to maxColumns-1 items, then add created_at at the end
  const numToTake = Math.max(1, maxColumns - 1);
  const slicedColumns = columnsWithoutCreatedAt.slice(0, numToTake);
  const slicedFields = fieldsWithoutCreatedAt.slice(0, numToTake);
  
  return {
    visibleColumns: [...slicedColumns, columns[createdAtIndex]],
    visibleFields: [...slicedFields, 'created_at']
  };
}

// Utility function for input validation
export function validateDataCount(value) {
  return Math.max(DATA_COUNT_LIMITS.MIN, Math.min(DATA_COUNT_LIMITS.MAX, Number(value)));
}