from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy.orm import Session
from .db.models import User
import base64
import os

class EncryptionManager:
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
        self.user = db.query(User).filter(User.id == user_id).first()
        if self.user.salt:
            self.salt = base64.b64decode(self.user.salt)
        else:
            self.salt = os.urandom(16)
            self.user.salt = base64.b64encode(self.salt).decode("utf-8")
            db.commit()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.user.username.encode()))
        self.fernet = Fernet(key)

    def encrypt_file(self, input_path: str, output_path: str):
        with open(input_path, 'rb') as f:
            data = f.read()
        encrypted_data = self.fernet.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

    def decrypt_file(self, input_path: str, output_path: str):
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
