import React from 'react';
import axios from 'axios';

function FileCard({ file, token }) {
  const handleDownload = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/download/${file.filename}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', file.filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Download failed');
    }
  };

  return (
    <div className="card">
      <h3 className="text-lg font-bold">{file.filename}</h3>
      <p className="text-sm">Uploaded: {new Date(file.uploaded_at).toLocaleString()}</p>
      <p className="text-sm">Tags: {Object.entries(file.tags).map(([k, v]) => `${k}: ${v}`).join(', ')}</p>
      <button className="mt-2 w-full" onClick={handleDownload}>
        Download
      </button>
    </div>
  );
}

export default FileCard;
