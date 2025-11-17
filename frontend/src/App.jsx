import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage, DataTablePage } from './components';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/user-table" element={<DataTablePage />} />
      </Routes>
    </Router>
  );
}

export default App;