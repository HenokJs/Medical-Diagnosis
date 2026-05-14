"""Initial database schema with all required columns.

Revision ID: 001
Revises: 
Create Date: 2026-05-12 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create patients table
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.String(50), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(20), nullable=False, server_default='unknown'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('patient_id')
    )
    op.create_index('ix_patients_patient_id', 'patients', ['patient_id'])

    # Create diagnosis_sessions table
    op.create_table(
        'diagnosis_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(100), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('submitted_symptoms', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('free_text_input', sa.Text(), nullable=True),
        sa.Column('symptom_duration_days', sa.Integer(), nullable=True),
        sa.Column('additional_notes', sa.Text(), nullable=True),
        sa.Column('overall_severity', sa.String(20), nullable=True),
        sa.Column('risk_level', sa.String(20), nullable=True),
        sa.Column('symptoms_processed', sa.Integer(), nullable=True),
        sa.Column('symptoms_matched', sa.Integer(), nullable=True),
        sa.Column('processing_time_ms', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )
    op.create_index('ix_diagnosis_sessions_session_id', 'diagnosis_sessions', ['session_id'])
    op.create_index('ix_diagnosis_sessions_patient_id', 'diagnosis_sessions', ['patient_id'])
    op.create_index('ix_diagnosis_sessions_created_at', 'diagnosis_sessions', ['created_at'])

    # Create extracted_symptoms table
    op.create_table(
        'extracted_symptoms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('symptom_name', sa.String(200), nullable=False),
        sa.Column('source', sa.String(20), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('matched_in_model', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['diagnosis_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_extracted_symptoms_session_id', 'extracted_symptoms', ['session_id'])

    # Create diagnosis_predictions table
    op.create_table(
        'diagnosis_predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('disease_name', sa.String(200), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(20), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('matched_symptoms', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('important_features', postgresql.JSON(), nullable=True),
        sa.Column('reasoning', sa.Text(), nullable=True),
        sa.Column('precautions', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('recommendations', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['diagnosis_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_diagnosis_predictions_session_id', 'diagnosis_predictions', ['session_id'])
    op.create_index('idx_session_rank', 'diagnosis_predictions', ['session_id', 'rank'])

    # Create rule_engine_alerts table
    op.create_table(
        'rule_engine_alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('rule_name', sa.String(200), nullable=False),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('triggered_by_symptoms', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['diagnosis_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_rule_engine_alerts_session_id', 'rule_engine_alerts', ['session_id'])

    # Create reports table
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_id', sa.String(100), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('report_type', sa.String(50), nullable=False, server_default='clinical_summary'),
        sa.Column('format', sa.String(20), nullable=False, server_default='json'),
        sa.Column('report_data', postgresql.JSON(), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('generated_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['diagnosis_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('report_id')
    )
    op.create_index('ix_reports_report_id', 'reports', ['report_id'])
    op.create_index('ix_reports_session_id', 'reports', ['session_id'])
    op.create_index('ix_reports_generated_at', 'reports', ['generated_at'])


def downgrade():
    op.drop_index('ix_reports_generated_at', table_name='reports')
    op.drop_index('ix_reports_session_id', table_name='reports')
    op.drop_index('ix_reports_report_id', table_name='reports')
    op.drop_table('reports')
    
    op.drop_index('ix_rule_engine_alerts_session_id', table_name='rule_engine_alerts')
    op.drop_table('rule_engine_alerts')
    
    op.drop_index('idx_session_rank', table_name='diagnosis_predictions')
    op.drop_index('ix_diagnosis_predictions_session_id', table_name='diagnosis_predictions')
    op.drop_table('diagnosis_predictions')
    
    op.drop_index('ix_extracted_symptoms_session_id', table_name='extracted_symptoms')
    op.drop_table('extracted_symptoms')
    
    op.drop_index('ix_diagnosis_sessions_created_at', table_name='diagnosis_sessions')
    op.drop_index('ix_diagnosis_sessions_patient_id', table_name='diagnosis_sessions')
    op.drop_index('ix_diagnosis_sessions_session_id', table_name='diagnosis_sessions')
    op.drop_table('diagnosis_sessions')
    
    op.drop_index('ix_patients_patient_id', table_name='patients')
    op.drop_table('patients')
