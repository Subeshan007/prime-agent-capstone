"""
PDF Generator Utility using ReportLab.
Converts Markdown-style text to a formatted PDF.
"""
import re
import html

def clean_markdown(text):
    """
    Converts markdown bold/italic to ReportLab XML tags.
    Escapes other XML characters.
    """
    # Escape XML characters first
    text = html.escape(text)
    
    # Replace **text** with <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Replace *text* with <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    return text

def generate_pdf_report(content: str) -> bytes:
    """
    Generates a PDF report from markdown text.
    Returns the PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(
        name='TitleCustom',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1F2124')
    ))
    
    styles.add(ParagraphStyle(
        name='Heading2Custom',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#3A7BFA')
    ))
    
    styles.add(ParagraphStyle(
        name='BodyCustom',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.HexColor('#1F2124')
    ))

    story = []
    
    # Add Title
    story.append(Paragraph("Research Report", styles['TitleCustom']))
    story.append(Spacer(1, 12))

    # Process content line by line (simple markdown parser)
    lines = content.split('\n')
    
    current_list_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            # End of list if we were in one
            if current_list_items:
                story.append(ListFlowable(
                    [ListItem(Paragraph(item, styles['BodyCustom'])) for item in current_list_items],
                    bulletType='bullet',
                    start='circle'
                ))
                current_list_items = []
            continue
            
        # Headers
        if line.startswith('# '):
            text = clean_markdown(line[2:])
            story.append(Paragraph(text, styles['TitleCustom']))
        elif line.startswith('## '):
            text = clean_markdown(line[3:])
            story.append(Paragraph(text, styles['Heading2Custom']))
        elif line.startswith('### '):
            text = clean_markdown(line[4:])
            story.append(Paragraph(text, styles['Heading3']))
            
        # Bullet Points
        elif line.startswith('- ') or line.startswith('* '):
            text = clean_markdown(line[2:])
            current_list_items.append(text)
            
        # Normal Text
        else:
            # If we were building a list, flush it
            if current_list_items:
                story.append(ListFlowable(
                    [ListItem(Paragraph(item, styles['BodyCustom'])) for item in current_list_items],
                    bulletType='bullet',
                    start='circle'
                ))
                current_list_items = []
                
            text = clean_markdown(line)
            story.append(Paragraph(text, styles['BodyCustom']))

    # Flush any remaining list items
    if current_list_items:
        story.append(ListFlowable(
            [ListItem(Paragraph(item, styles['BodyCustom'])) for item in current_list_items],
            bulletType='bullet',
            start='circle'
        ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
