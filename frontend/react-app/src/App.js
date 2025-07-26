import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import './index.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  return (
    <Router>
      <div className="min-h-screen bg-cyberpunk">
        <Routes>
          <Route path="/" element={<Login setToken={setToken} />} />
          <Route path="/dashboard" element={<Dashboard token={token} setToken={setToken} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
