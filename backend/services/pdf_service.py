"""
PDF Generation Service using ReportLab
Generates professional medical reports in PDF format
"""

import logging
from datetime import datetime
from typing import Dict, Optional
from io import BytesIO

logger = logging.getLogger(__name__)

# Try to import ReportLab
try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.units import inch, cm
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, KeepTogether
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not installed. PDF generation will not be available.")


class PDFService:
    """Service for generating PDF reports."""
    
    def __init__(self):
        self.available = REPORTLAB_AVAILABLE
        if not self.available:
            logger.warning("PDF service initialized but ReportLab is not available")
    
    def generate_pdf(
        self,
        report_data: Dict,
        output_path: str = None
    ) -> Optional[BytesIO | str]:
        """
        Generate PDF report from report data.
        
        Args:
            report_data: Complete report data dictionary
            output_path: Optional output file path. If None, generates in memory.
            
        Returns:
            BytesIO buffer if generated in memory, file path if saved, None if error
        """
        if not self.available:
            logger.error("Cannot generate PDF: ReportLab not installed")
            return None
        
        try:
            # Create PDF document
            if output_path:
                doc = SimpleDocTemplate(
                    output_path,
                    pagesize=A4,
                    rightMargin=2*cm,
                    leftMargin=2*cm,
                    topMargin=2*cm,
                    bottomMargin=2*cm
                )
            else:
                buffer = BytesIO()
                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=A4,
                    rightMargin=2*cm,
                    leftMargin=2*cm,
                    topMargin=2*cm,
                    bottomMargin=2*cm
                )
            
            # Build PDF content
            story = []
            styles = self._get_styles()
            
            # Header
            story.extend(self._build_header(report_data, styles))
            story.append(Spacer(1, 0.5*cm))
            
            # Patient Information
            story.extend(self._build_patient_section(report_data, styles))
            story.append(Spacer(1, 0.5*cm))
            
            # Diagnosis Summary
            story.extend(self._build_diagnosis_section(report_data, styles))
            story.append(Spacer(1, 0.5*cm))
            
            # Top Predictions
            story.extend(self._build_predictions_section(report_data, styles))
            story.append(Spacer(1, 0.5*cm))
            
            # Clinical Findings
            story.extend(self._build_findings_section(report_data, styles))
            story.append(Spacer(1, 0.5*cm))
            
            # Recommendations
            if report_data.get('recommendation'):
                story.extend(self._build_recommendations_section(report_data, styles))
                story.append(Spacer(1, 0.5*cm))
            
            # Disclaimer
            story.extend(self._build_disclaimer_section(report_data, styles))
            
            # Build PDF
            doc.build(story)
            
            if output_path:
                logger.info(f"PDF generated successfully: {output_path}")
                return output_path

            buffer.seek(0)
            return buffer
                
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            return None
    
    def _get_styles(self):
        """Get custom paragraph styles."""
        styles = getSampleStyleSheet()
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#03045e'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0077b6'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#03045e'),
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        styles.add(ParagraphStyle(
            name='CustomSmall',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            spaceAfter=4
        ))
        
        return styles
    
    def _build_header(self, report_data: Dict, styles) -> list:
        """Build PDF header."""
        elements = []
        
        # Title
        title = Paragraph("CLINICAL DIAGNOSIS REPORT", styles['CustomTitle'])
        elements.append(title)
        
        # Report ID and Date
        report_id = report_data.get('report_id', 'N/A')
        generated_at = report_data.get('generated_at', datetime.utcnow().isoformat())
        
        info_data = [
            ['Report ID:', report_id],
            ['Generated:', generated_at[:19].replace('T', ' ') + ' UTC']
        ]
        
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0077b6')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(info_table)
        
        return elements
    
    def _build_patient_section(self, report_data: Dict, styles) -> list:
        """Build patient information section."""
        elements = []
        
        heading = Paragraph("Patient Information", styles['CustomHeading'])
        elements.append(heading)
        
        patient_info = report_data.get('patient_info', {})
        
        data = [
            ['Age:', str(patient_info.get('age', 'N/A'))],
            ['Gender:', str(patient_info.get('gender', 'N/A'))],
        ]
        
        if patient_info.get('patient_id'):
            data.insert(0, ['Patient ID:', patient_info['patient_id']])
        
        table = Table(data, colWidths=[4*cm, 12*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0077b6')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_diagnosis_section(self, report_data: Dict, styles) -> list:
        """Build diagnosis summary section."""
        elements = []
        
        heading = Paragraph("Diagnosis Summary", styles['CustomHeading'])
        elements.append(heading)
        
        diagnosis = report_data.get('diagnosis', {})
        
        data = [
            ['Overall Severity:', str(diagnosis.get('severity', 'Unknown')).upper()],
            ['Risk Level:', str(diagnosis.get('risk_level', 'Unknown')).upper()],
        ]
        
        table = Table(data, colWidths=[4*cm, 12*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0077b6')),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_predictions_section(self, report_data: Dict, styles) -> list:
        """Build top predictions section."""
        elements = []
        
        heading = Paragraph("Top 3 Differential Diagnoses", styles['CustomHeading'])
        elements.append(heading)
        
        diagnosis = report_data.get('diagnosis', {})
        predictions = diagnosis.get('top_predictions', [])[:3]
        
        if not predictions:
            elements.append(Paragraph("No predictions available", styles['CustomBody']))
            return elements
        
        # Create table data
        data = [['Rank', 'Disease', 'Confidence', 'Severity']]
        
        for idx, pred in enumerate(predictions, 1):
            disease = pred.get('disease', pred.get('disease_name', 'Unknown'))
            confidence = pred.get('confidence', pred.get('confidence_score', 0))
            severity = pred.get('severity', 'Unknown')
            
            data.append([
                f"#{idx}",
                disease,
                f"{confidence * 100:.1f}%",
                severity.upper()
            ])
        
        table = Table(data, colWidths=[2*cm, 8*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0077b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#90e0ef')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#caf0f8')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        # Add precautions and recommendations for top prediction
        if predictions:
            top_pred = predictions[0]
            
            if top_pred.get('precautions'):
                elements.append(Spacer(1, 0.3*cm))
                elements.append(Paragraph("<b>Precautions:</b>", styles['CustomBody']))
                for precaution in top_pred['precautions'][:3]:
                    elements.append(Paragraph(f"• {precaution}", styles['CustomBody']))
            
            if top_pred.get('recommendations'):
                elements.append(Spacer(1, 0.3*cm))
                elements.append(Paragraph("<b>Recommendations:</b>", styles['CustomBody']))
                for recommendation in top_pred['recommendations'][:3]:
                    elements.append(Paragraph(f"• {recommendation}", styles['CustomBody']))
        
        return elements
    
    def _build_findings_section(self, report_data: Dict, styles) -> list:
        """Build clinical findings section."""
        elements = []
        
        heading = Paragraph("Clinical Findings", styles['CustomHeading'])
        elements.append(heading)
        
        findings = report_data.get('clinical_findings', {})
        symptoms = findings.get('symptoms', [])
        rule_flags = findings.get('rule_flags', [])
        
        # Symptoms
        if symptoms:
            elements.append(Paragraph("<b>Matched Symptoms:</b>", styles['CustomBody']))
            symptoms_text = ", ".join(symptoms)
            elements.append(Paragraph(symptoms_text, styles['CustomBody']))
        
        # Rule alerts
        if rule_flags:
            elements.append(Spacer(1, 0.3*cm))
            elements.append(Paragraph(f"<b>Clinical Alerts:</b> {len(rule_flags)} alert(s) triggered", styles['CustomBody']))
        
        return elements
    
    def _build_recommendations_section(self, report_data: Dict, styles) -> list:
        """Build recommendations section."""
        elements = []
        
        heading = Paragraph("Clinical Recommendations", styles['CustomHeading'])
        elements.append(heading)
        
        recommendation = report_data.get('recommendation', '')
        elements.append(Paragraph(recommendation, styles['CustomBody']))
        
        return elements
    
    def _build_disclaimer_section(self, report_data: Dict, styles) -> list:
        """Build disclaimer section."""
        elements = []
        
        elements.append(Spacer(1, 1*cm))
        
        # Disclaimer box
        disclaimer = report_data.get('disclaimer', 
            'This system provides clinical decision support only. Results are not a substitute '
            'for professional medical advice, diagnosis, or treatment. Always seek the advice of '
            'qualified health providers with any questions regarding medical conditions.')
        
        disclaimer_para = Paragraph(
            f"<b>IMPORTANT MEDICAL DISCLAIMER:</b><br/>{disclaimer}",
            styles['CustomSmall']
        )
        
        disclaimer_table = Table([[disclaimer_para]], colWidths=[16*cm])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#caf0f8')),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor('#0077b6')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(disclaimer_table)
        
        return elements


# Singleton instance
pdf_service = PDFService()
