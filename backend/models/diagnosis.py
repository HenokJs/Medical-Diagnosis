from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from . import db


class DiagnosisSession(db.Model):
    """Complete diagnosis session with all data."""
    
    __tablename__ = 'diagnosis_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    
    # Input data
    submitted_symptoms = db.Column(ARRAY(db.String), nullable=False)
    free_text_input = db.Column(db.Text)
    symptom_duration_days = db.Column(db.Integer)
    additional_notes = db.Column(db.Text)
    
    # Analysis results
    overall_severity = db.Column(db.String(20))
    risk_level = db.Column(db.String(20))
    symptoms_processed = db.Column(db.Integer)
    symptoms_matched = db.Column(db.Integer)
    
    # Metadata
    processing_time_ms = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    extracted_symptoms = db.relationship('ExtractedSymptom', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    predictions = db.relationship('DiagnosisPrediction', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    rule_alerts = db.relationship('RuleEngineAlert', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<DiagnosisSession {self.session_id}>'
    
    def to_dict(self, include_details=False):
        """Convert to dictionary."""
        data = {
            'id': self.id,
            'session_id': self.session_id,
            'patient_id': self.patient_id,
            'submitted_symptoms': self.submitted_symptoms,
            'free_text_input': self.free_text_input,
            'symptom_duration_days': self.symptom_duration_days,
            'overall_severity': self.overall_severity,
            'risk_level': self.risk_level,
            'symptoms_processed': self.symptoms_processed,
            'symptoms_matched': self.symptoms_matched,
            'processing_time_ms': self.processing_time_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_details:
            data['patient'] = self.patient.to_dict() if self.patient else None
            data['extracted_symptoms'] = [s.to_dict() for s in self.extracted_symptoms]
            data['predictions'] = [p.to_dict() for p in self.predictions.order_by(DiagnosisPrediction.rank)]
            data['rule_alerts'] = [a.to_dict() for a in self.rule_alerts]
            data['reports'] = [r.to_dict() for r in self.reports]
        
        return data


class ExtractedSymptom(db.Model):
    """NLP-extracted symptoms from free text."""
    
    __tablename__ = 'extracted_symptoms'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('diagnosis_sessions.id'), nullable=False, index=True)
    
    symptom_name = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(20), nullable=False)  # 'checkbox', 'nlp', 'merged'
    confidence = db.Column(db.Float)
    matched_in_model = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExtractedSymptom {self.symptom_name} ({self.source})>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'symptom_name': self.symptom_name,
            'source': self.source,
            'confidence': self.confidence,
            'matched_in_model': self.matched_in_model
        }


class DiagnosisPrediction(db.Model):
    """Individual disease prediction."""
    
    __tablename__ = 'diagnosis_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('diagnosis_sessions.id'), nullable=False, index=True)
    
    rank = db.Column(db.Integer, nullable=False)  # 1, 2, 3 for top-3
    disease_name = db.Column(db.String(200), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    
    # Explainability
    matched_symptoms = db.Column(ARRAY(db.String))
    important_features = db.Column(JSON)
    reasoning = db.Column(db.Text)
    
    # Treatment guidance (non-prescriptive)
    precautions = db.Column(ARRAY(db.String))
    recommendations = db.Column(ARRAY(db.String))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_session_rank', 'session_id', 'rank'),
    )
    
    def __repr__(self):
        return f'<DiagnosisPrediction #{self.rank}: {self.disease_name} ({self.confidence_score:.2%})>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'rank': self.rank,
            'disease_name': self.disease_name,
            'confidence_score': self.confidence_score,
            'severity': self.severity,
            'description': self.description,
            'matched_symptoms': self.matched_symptoms,
            'important_features': self.important_features,
            'reasoning': self.reasoning,
            'precautions': self.precautions,
            'recommendations': self.recommendations
        }


class RuleEngineAlert(db.Model):
    """Rule engine triggered alerts."""
    
    __tablename__ = 'rule_engine_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('diagnosis_sessions.id'), nullable=False, index=True)
    
    rule_name = db.Column(db.String(200), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # 'warning', 'urgent', 'info'
    message = db.Column(db.Text, nullable=False)
    triggered_by_symptoms = db.Column(ARRAY(db.String))
    priority = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RuleEngineAlert {self.rule_name}: {self.alert_type}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'rule_name': self.rule_name,
            'alert_type': self.alert_type,
            'message': self.message,
            'triggered_by_symptoms': self.triggered_by_symptoms,
            'priority': self.priority
        }
