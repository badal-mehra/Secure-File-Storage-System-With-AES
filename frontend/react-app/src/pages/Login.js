import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      const url = isRegister ? 'http://localhost:8000/register' : 'http://localhost:8000/token';
      const data = isRegister ? { username, password } : new URLSearchParams({ username, password });
      const response = await axios.post(url, data);
      if (!isRegister) {
        const token = response.data.access_token;
        setToken(token);
        localStorage.setItem('token', token);
        navigate('/dashboard');
      } else {
        alert('Registration successful. Please log in.');
        setIsRegister(false);
      }
    } catch (error) {
      alert(isRegister ? 'Registration failed' : 'Login failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20">
      <h1 className="text-4xl font-bold text-center mb-8">{isRegister ? 'Register' : 'Login'} to SecureAI-Drive</h1>
      <div className="card">
        <input
          type="text"
          placeholder="Username"
          className="mb-4 w-full"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="mb-4 w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="w-full" onClick={handleSubmit}>
          {isRegister ? 'Register' : 'Login'}
        </button>
        <button
          className="text-neon mt-4 w-full text-center"
          onClick={() => setIsRegister(!isRegister)}
        >
          {isRegister ? 'Switch to Login' : 'Switch to Register'}
        </button>
      </div>
    </div>
  );
}

export default Login;
