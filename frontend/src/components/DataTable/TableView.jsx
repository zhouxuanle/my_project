import React from 'react';
import { TableContainer, Table, Thead, Th, Tbody, Tr, Td } from '../ui/Table';

function TableView({
  tableData,
  visibleColumns,
  visibleFields,
  activeTable,
  effectiveParentJobId,
}) {
  return (
    <TableContainer>
      {tableData.length > 0 ? (
        <Table>
          <Thead>
            <Tr>
              {visibleColumns.map((col, index) => (
                <Th key={index}>{col}</Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>
            {tableData.map((data, index) => (
              <Tr key={data.id || index}>
                {visibleFields.map((field, idx) => (
                  <Td key={idx}>{data[field]}</Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      ) : (
        <p>
          No {activeTable} data found. {effectiveParentJobId ? '' : 'Use the Data button to view generated data folders.'}
        </p>
      )}
    </TableContainer>
  );
}

export default TableView;
