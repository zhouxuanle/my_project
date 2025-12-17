import React, { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { useWindowWidth, useDataFolders, useDataTablePage } from '../../hooks';
import { getMaxColumns, getVisibleColumnsAndFields } from '../../utils';
import LeftMenu from '../LeftMenu';
import FoldersView from './FoldersView';
import FolderTablesView from './FolderTablesView';
import TableView from './TableView';

function DataTablePage() {
  const location = useLocation();
  const locationParentJobId = location.state?.parentJobId;
 
  const page = useDataTablePage({
    locationState: location.state,
    locationParentJobId,
    locationKey: location.key,
  });
  
  const { folders, loading: foldersLoading, error: foldersError } = useDataFolders({ autoFetch: true });

  // Memoize table config for current active table
  const currentTableConfig = page.currentTableConfig;

  // Responsive: determine how many columns to show based on window width
  const windowWidth = useWindowWidth();
  
  // Calculate visible columns and fields with responsive behavior
  const { visibleColumns, visibleFields } = useMemo(() => {
    const maxColumns = getMaxColumns(windowWidth, currentTableConfig.columns.length);
    return getVisibleColumnsAndFields(currentTableConfig, maxColumns);
  }, [windowWidth, currentTableConfig]);

  return (
    <div className="App app-with-left-menu">
      <LeftMenu />
      
      <header className="App-header">
        <h1 className="page-title">Data Tables</h1>
        
        {page.mode === 'folders' ? (
          <FoldersView
            foldersLoading={foldersLoading}
            foldersError={foldersError}
            folders={folders}
            onSelectFolder={page.selectFolder}
            onBackToTables={page.backToTables}
          />
        ) : page.mode === 'folderTables' && page.selectedFolder ? (
          <FolderTablesView
            selectedFolder={page.selectedFolder}
            tables={page.tables}
            onOpenFolderTable={page.openFolderTable}
            onBackToFolders={page.backToFolders}
          />
        ) : (
          <TableView
            tableData={page.tableData}
            visibleColumns={visibleColumns}
            visibleFields={visibleFields}
            activeTable={page.activeTable}
            effectiveParentJobId={page.effectiveParentJobId}
            loading={page.loading}
          />
        )}

        <div className="empty-page empty-page-style"></div>
      </header>
    </div>
  );
}

export default DataTablePage;
