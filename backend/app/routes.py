from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .db.models import User, File
from .auth import get_password_hash, create_access_token, get_current_user, verify_password
from .utils.encryption import EncryptionManager
from .utils.ai_tagger import FileTagger
from ..ai_models.anomaly_detector import AnomalyDetector
from .db.database import get_db
import os
import json
from datetime import datetime

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    anomaly_detector = AnomalyDetector()
    if anomaly_detector.check_access(user.id, "upload", db):
        raise HTTPException(status_code=403, detail="Anomalous activity detected")

    os.makedirs(f"storage/{user.id}", exist_ok=True)
    temp_path = f"temp/{file.filename}"
    encrypted_path = f"storage/{user.id}/{file.filename}.enc"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    em = EncryptionManager(user.id, db)
    em.encrypt_file(temp_path, encrypted_path)

    tagger = FileTagger()
    tags = tagger.tag_file(temp_path)

    file_record = File(user_id=user.id, filename=file.filename, tags=json.dumps(tags))
    db.add(file_record)
    db.commit()

    os.remove(temp_path)
    return {"message": f"File {file.filename} uploaded successfully", "tags": tags}

@router.get("/files")
def list_files(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    files = db.query(File).filter(File.user_id == user.id).all()
    return [{"filename": f.filename, "tags": json.loads(f.tags), "uploaded_at": f.uploaded_at} for f in files]

@router.get("/download/{filename}")
async def download_file(filename: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    encrypted_path = f"storage/{user.id}/{filename}.enc"
    if not os.path.exists(encrypted_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    temp_path = f"temp/{filename}"
    em = EncryptionManager(user.id, db)
    em.decrypt_file(encrypted_path, temp_path)
    
    return FileResponse(temp_path, filename=filename, media_type="application/octet-stream")
