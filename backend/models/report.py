from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from . import db


class Report(db.Model):
    """Generated clinical report."""
    
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('diagnosis_sessions.id'), nullable=False, index=True)
    
    # Report metadata
    report_type = db.Column(db.String(50), default='clinical_summary')
    format = db.Column(db.String(20), default='json')  # 'json', 'pdf', 'html'
    
    # Report content
    report_data = db.Column(JSON, nullable=False)
    
    # File information (if saved)
    file_path = db.Column(db.String(500))
    file_size_bytes = db.Column(db.Integer)
    
    # Metadata
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    generated_by = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Report {self.report_id}>'
    
    def to_dict(self, include_data=False):
        """Convert to dictionary."""
        data = {
            'id': self.id,
            'report_id': self.report_id,
            'session_id': self.session.session_id if self.session else None,
            'session_db_id': self.session_id,
            'report_type': self.report_type,
            'format': self.format,
            'file_path': self.file_path,
            'file_size_bytes': self.file_size_bytes,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'generated_by': self.generated_by
        }
        
        if include_data:
            data['report_data'] = self.report_data
        
        return data
