import React, { useState } from 'react';
import { TableContainer, Table, Thead, Th, Tbody, Tr, Td } from '../ui/Table';
import Button from '../ui/Button';
import { api } from '../../services/api';

function TableView({
  tableData,
  visibleColumns,
  visibleFields,
  activeTable,
  effectiveParentJobId,
  loading,
}) {
  const [cleaning, setCleaning] = useState(false);
  const [cleanMessage, setCleanMessage] = useState('');

  const handleCleanData = async () => {
    try {
      setCleaning(true);
      setCleanMessage('');
      
      if (!effectiveParentJobId) {
        setCleanMessage('✗ No parent job ID found. Please generate data first.');
        setCleaning(false);
        return;
      }
      
      const dataCount = tableData.length;
      const response = await api.cleanData(dataCount, effectiveParentJobId);
      const result = await response.json();
      
      if (result.success) {
        setCleanMessage(`✓ Cleaning queued: ${result.totalChunks} chunks → ${result.processingPath} (Parent: ${result.parentJobId})`);
      } else {
        setCleanMessage(`✗ Failed: ${result.message}`);
      }
    } catch (error) {
      setCleanMessage(`✗ Error: ${error.message}`);
    } finally {
      setCleaning(false);
    }
  };

  return (
    <TableContainer>
      {loading ? (
        <div>Loading...</div>
      ) : tableData.length > 0 ? (
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
      
      {tableData.length > 0 && (
        <div className="mt-6 flex flex-col items-center gap-3">
          <Button
            variant="action"
            onClick={handleCleanData}
            disabled={cleaning}
            className="max-w-md"
          >
            {cleaning ? 'Processing...' : 'Clean Data'}
          </Button>
          {cleanMessage && (
            <p className={`text-sm ${
              cleanMessage.startsWith('✓') ? 'text-green-400' : 'text-red-400'
            }`}>
              {cleanMessage}
            </p>
          )}
        </div>
      )}
    </TableContainer>
  );
}

export default TableView;
