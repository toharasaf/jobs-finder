import markdown
from xhtml2pdf import pisa

def create_cv_pdf(md_text: str, output_filename: str) -> bool:
    """
    Converts a Markdown formatted CV string into a stylized PDF file.
    """
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_text, extensions=['tables'])
    
    # Wrap in basic HTML structure with CSS for styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: Helvetica, Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #333333;
            }}
            h1 {{
                font-size: 20pt;
                text-align: center;
                color: #2c3e50;
                margin-bottom: 5px;
            }}
            h2 {{
                font-size: 14pt;
                color: #2980b9;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 3px;
                margin-top: 15px;
                margin-bottom: 10px;
            }}
            p {{
                margin: 5px 0;
            }}
            .contact-info {{
                text-align: center;
                font-size: 10pt;
                color: #7f8c8d;
                margin-bottom: 20px;
            }}
            ul {{
                margin-top: 5px;
                margin-bottom: 10px;
            }}
            li {{
                margin-bottom: 3px;
            }}
            strong {{
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    try:
        with open(output_filename, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)
            
        return not pisa_status.err
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
