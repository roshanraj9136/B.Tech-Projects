import os
from pathlib import Path
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.core.config import settings

class ReportService:
    @staticmethod
    def generate_pdf_report(result_data: Dict[str, Any], output_path: Path) -> Path:
        """
        Generates an evidence-driven, publication-grade forensic PDF analysis report.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        
        # Custom color palette (Linear/Vercel inspired dark slate & indigo)
        c_primary = colors.HexColor("#0f172a") # Slate 900
        c_accent = colors.HexColor("#2563eb") # Blue 600
        c_fake = colors.HexColor("#dc2626")   # Red 600
        c_real = colors.HexColor("#16a34a")   # Green 600
        c_gray = colors.HexColor("#475569")   # Slate 600
        c_light = colors.HexColor("#f8fafc")  # Slate 50
        c_border = colors.HexColor("#cbd5e1") # Slate 300
        
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=c_primary,
            fontName="Helvetica-Bold"
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=c_gray,
            fontName="Helvetica"
        )
        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            textColor=c_accent,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1e293b"),
            fontName="Helvetica"
        )
        bold_style = ParagraphStyle(
            "BodyBold",
            parent=body_style,
            fontName="Helvetica-Bold"
        )
        
        elements = []
        
        # 1. Header Banner
        verdict_obj = result_data.get("verdict", {})
        verdict_text = verdict_obj.get("verdict", "INCONCLUSIVE")
        verdict_color = c_fake if verdict_text == "LIKELY MANIPULATED" else (c_real if verdict_text == "LIKELY AUTHENTIC" else c_gray)
        
        header_table_data = [
            [
                Paragraph("<b>VIDEO DEEPFAKE DETECTION</b><br/><font size=8 color='#64748b'>Explainable AI Forensic Analysis Report</font>", title_style),
                Paragraph(f"<font size=8 color='#64748b'>ANALYSIS ID</font><br/><b>{result_data.get('analysis_id', 'N/A')[:18]}...</b><br/><font size=8 color='#64748b'>{result_data.get('created_at', '')}</font>", subtitle_style)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[4.0 * inch, 3.2 * inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=8))
        
        # 2. Executive Verdict Card
        p_fake = verdict_obj.get("p_fake", 0.5)
        p_real = verdict_obj.get("p_real", 0.5)
        
        verdict_card_data = [
            [
                Paragraph(f"<font size=10 color='#64748b'>FORENSIC VERDICT</font><br/><font size=16 color='{verdict_color.hexval()}'><b>{verdict_text}</b></font>", body_style),
                Paragraph(f"<font size=10 color='#64748b'>MANIPULATION PROBABILITY</font><br/><font size=14><b>{p_fake:.1%}</b></font><br/><font size=8 color='#64748b'>P(REAL): {p_real:.1%}</font>", body_style),
                Paragraph(f"<font size=8 color='#64748b'>THRESHOLDS</font><br/><font size=8>Authentic: &lt;{verdict_obj.get('threshold_authentic', 0.3):.2f}<br/>Manipulated: &ge;{verdict_obj.get('threshold_manipulated', 0.7):.2f}</font>", body_style),
                Paragraph(f"<font size=8 color='#64748b'>CLIPS / DURATION</font><br/><font size=8><b>{verdict_obj.get('n_clips_analyzed', 0)} clips</b> ({verdict_obj.get('video_duration_s', 0)}s)<br/>Time: {verdict_obj.get('processing_time_s', 0)}s</font>", body_style)
            ]
        ]
        verdict_card = Table(verdict_card_data, colWidths=[2.2 * inch, 1.8 * inch, 1.6 * inch, 1.6 * inch])
        verdict_card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_light),
            ('BOX', (0, 0), (-1, -1), 1, c_border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(verdict_card)
        elements.append(Spacer(1, 10))
        
        # 3. Dynamic Forensic Explanation
        elements.append(Paragraph("Forensic Summary & Evidence Synthesis", h2_style))
        elements.append(Paragraph(result_data.get("final_explanation", "No explanation available."), body_style))
        elements.append(Spacer(1, 10))
        
        # 4. Spatial vs Temporal Attribution (Shapley Values)
        branch = result_data.get("branch_analysis", {})
        elements.append(Paragraph("Branch Attribution (Exact Shapley Decomposition)", h2_style))
        branch_table_data = [
            ["Branch", "Diagnostic Focus", "Evidence Share (%)", "Shapley Value (phi)"],
            ["Spatial Head (S)", "Appearance, facial anatomy, synthesis boundary artifacts", f"{branch.get('pct_spatial', 0):.1f}%", f"{branch.get('phi_spatial', 0):+.4f}"],
            ["Temporal Head (T)", "Motion continuity, temporal jitter, inter-frame coherence", f"{branch.get('pct_temporal', 0):.1f}%", f"{branch.get('phi_temporal', 0):+.4f}"]
        ]
        branch_table = Table(branch_table_data, colWidths=[1.8 * inch, 3.2 * inch, 1.2 * inch, 1.0 * inch])
        branch_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(branch_table)
        elements.append(Spacer(1, 10))
        
        # 5. Facial Component Analysis
        components_obj = result_data.get("facial_components", {}).get("components", {})
        elements.append(Paragraph("Facial Component Attribution (FCG Query Space)", h2_style))
        comp_table_data = [
            ["Facial Component", "Signed Logit Contribution", "Normalized Share (%)", "Evidence Pushes Towards", "Importance"]
        ]
        for part_name, part_val in components_obj.items():
            comp_table_data.append([
                part_name.capitalize(),
                f"{part_val.get('signed_contribution', 0):+.4f}",
                f"{part_val.get('normalized_share_pct', 0):.1f}%",
                part_val.get("evidence_direction", "N/A"),
                part_val.get("relative_importance", "N/A")
            ])
            
        comp_table = Table(comp_table_data, colWidths=[1.5 * inch, 1.8 * inch, 1.4 * inch, 1.5 * inch, 1.0 * inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#334155")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(comp_table)
        elements.append(Spacer(1, 10))
        
        # 6. Heatmaps & Visual Evidence
        face_crop_file = settings.HEATMAPS_DIR / f"{result_data['analysis_id']}_face.png"
        spatial_hm_file = settings.HEATMAPS_DIR / f"{result_data['analysis_id']}_spatial_hm.png"
        temporal_hm_file = settings.HEATMAPS_DIR / f"{result_data['analysis_id']}_temporal_hm.png"
        
        images_row = []
        if face_crop_file.exists():
            images_row.append([
                Paragraph("<b>Extracted Face Crop</b>", body_style),
                Image(str(face_crop_file), width=2.0 * inch, height=2.0 * inch)
            ])
        if spatial_hm_file.exists():
            images_row.append([
                Paragraph("<b>Spatial 16x16 Heatmap</b>", body_style),
                Image(str(spatial_hm_file), width=2.0 * inch, height=2.0 * inch)
            ])
        if temporal_hm_file.exists():
            images_row.append([
                Paragraph("<b>Temporal 16x16 Heatmap</b>", body_style),
                Image(str(temporal_hm_file), width=2.0 * inch, height=2.0 * inch)
            ])
            
        if len(images_row) == 3:
            elements.append(Paragraph("Visual Forensic Heatmaps (16x16 Patch Decomposition)", h2_style))
            img_table_data = [
                [images_row[0][0], images_row[1][0], images_row[2][0]],
                [images_row[0][1], images_row[1][1], images_row[2][1]]
            ]
            img_table = Table(img_table_data, colWidths=[2.4 * inch, 2.4 * inch, 2.4 * inch])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ]))
            elements.append(KeepTogether(img_table))
            elements.append(Spacer(1, 10))
            
        # 7. Video Quality & Forensic Limitations
        quality = result_data.get("quality_report", {})
        elements.append(Paragraph("Video Quality & Robustness Assessment", h2_style))
        q_notes = "<br/>".join([f"&bull; {n}" for n in quality.get("quality_notes", [])])
        quality_p = (
            f"<b>Resolution:</b> {quality.get('resolution')} | <b>FPS:</b> {quality.get('fps')} | "
            f"<b>Sharpness:</b> {quality.get('blur_assessment')} ({quality.get('blur_score')} var) | "
            f"<b>Compression:</b> {quality.get('compression_level')}<br/>"
            f"{q_notes}"
        )
        elements.append(Paragraph(quality_p, body_style))
        elements.append(Spacer(1, 8))
        
        # 8. Footer & Citations
        elements.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=4, spaceAfter=6))
        elements.append(Paragraph(
            "<font size=7 color='#64748b'><b>Methodology & Architecture:</b> Yue-Hua Han et al., 'Towards More General Video-based Deepfake Detection through Facial Component Guided Adaptation for Foundation Model' (CVPR 2025, arXiv:2404.05583). "
            "Attributions computed via exact Shapley decomposition and additive LayerNorm-Linear projections. Formal video deepfake forensic analysis report.</font>",
            body_style
        ))
        
        doc.build(elements)
        return output_path
