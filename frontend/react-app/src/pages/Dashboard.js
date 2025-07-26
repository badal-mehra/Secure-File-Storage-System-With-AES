import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import FileCard from '../components/FileCard';

function Dashboard({ token, setToken }) {
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/files', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setFiles(response.data);
    } catch (error) {
      alert('Failed to fetch files');
    }
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert(response.data.message);
      fetchFiles();
    } catch (error) {
      alert('Upload failed');
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-8">SecureAI-Drive Dashboard</h1>
      <button className="bg-accent text-white p-2 mb-8" onClick={handleLogout}>
        Logout
      </button>
      <div className="card mb-8">
        <h2 className="text-2xl mb-4">Upload File</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-4" />
        <button className="w-full" onClick={handleUpload}>
          Upload
        </button>
      </div>
      <h2 className="text-2xl mb-4">Your Files</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {files.map((file) => (
          <FileCard key={file.filename} file={file} token={token} />
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
