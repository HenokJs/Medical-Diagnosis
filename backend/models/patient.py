from datetime import datetime
from . import db


class Patient(db.Model):
    """Patient demographic information."""
    
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=False, default='unknown')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    diagnosis_sessions = db.relationship('DiagnosisSession', backref='patient', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.patient_id}: {self.age}yo {self.gender}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_sessions': self.diagnosis_sessions.count()
        }
