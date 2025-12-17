import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage, DataTablePage, PrivateRoute, Layout } from './components';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route element={<PrivateRoute />}>
            <Route path="/user-table" element={<DataTablePage />} />
          </Route>
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;