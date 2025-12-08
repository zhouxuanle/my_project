import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage, DataTablePage, PrivateRoute, DataFolders, DataFolderDetail } from './components';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route element={<PrivateRoute />}>
          <Route path="/user-table" element={<DataTablePage />} />
          <Route path="/data" element={<DataFolders />} />
          <Route path="/data/:parentJobId" element={<DataFolderDetail />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;