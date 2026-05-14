"""Add updated_at columns to existing tables.

Revision ID: 002
Revises: 001
Create Date: 2026-05-14 14:55:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add updated_at column to diagnosis_sessions if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='diagnosis_sessions' AND column_name='updated_at'
            ) THEN
                ALTER TABLE diagnosis_sessions 
                ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
    """)
    
    # Add updated_at column to extracted_symptoms if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='extracted_symptoms' AND column_name='updated_at'
            ) THEN
                ALTER TABLE extracted_symptoms 
                ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
    """)
    
    # Add updated_at column to diagnosis_predictions if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='diagnosis_predictions' AND column_name='updated_at'
            ) THEN
                ALTER TABLE diagnosis_predictions 
                ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
    """)
    
    # Add updated_at column to rule_engine_alerts if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='rule_engine_alerts' AND column_name='updated_at'
            ) THEN
                ALTER TABLE rule_engine_alerts 
                ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
    """)
    
    # Add updated_at column to reports if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='reports' AND column_name='updated_at'
            ) THEN
                ALTER TABLE reports 
                ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
    """)
    
    # Add updated_at column to patients if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='patients' AND column_name='updated_at'
            ) THEN
                ALTER TABLE patients 
                ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
    """)


def downgrade():
    # Remove updated_at columns
    op.execute("ALTER TABLE patients DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE diagnosis_sessions DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE extracted_symptoms DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE diagnosis_predictions DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE rule_engine_alerts DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE reports DROP COLUMN IF EXISTS updated_at")
