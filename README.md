# Secure-File-Storage-System-With-AES

A secure file storage system with AES encryption, AI-powered tagging, and anomaly detection. Built with FastAPI, React, and Typer, styled in a futuristic cyberpunk theme.

## Features
- **Backend**: FastAPI with JWT authentication, SQLite database, AES encryption using `cryptography`, AI tagging with HuggingFace, and simulated anomaly detection.
- **Frontend**: React with Tailwind CSS, cyberpunk-themed UI for login, file upload/download, and dashboard with file tags.
- **CLI**: Typer-based tool for login, upload, download, and listing files.
- **Deployment**: Docker Compose with Nginx reverse proxy.

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/badal-mehra/Secure-File-Storage-System-With-AES

##   Install dependencies:
pip install -r backend/requirements.txt
cd frontend/react-app && npm install
cd ../../cli && pip install -r requirements.txt

## Set up environment:
Copy backend/.env.template to backend/.env.
The JWT_SECRET_KEY will auto-generate if not set.

## Run with Docker:
cd docker
docker-compose up -d

---

### Step 6: Running the System
1. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   cd frontend/react-app && npm install
   cd ../../cli && pip install -r requirements.txt
