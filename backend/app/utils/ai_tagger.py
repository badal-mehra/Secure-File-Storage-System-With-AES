from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.db.models import File

class AnomalyDetector:
    def __init__(self):
        # Simulated LSTM-based anomaly detector
        pass

    def check_access(self, user_id: int, action: str, db: Session) -> bool:
        # Simulate anomaly detection based on access frequency
        recent_accesses = db.query(File).filter(
            File.user_id == user_id,
            File.uploaded_at > datetime.utcnow() - timedelta(minutes=5)
        ).count()
        is_anomalous = recent_accesses > 5  # Flag if more than 5 uploads in 5 minutes
        return is_anomalous
