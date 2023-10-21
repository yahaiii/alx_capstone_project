from flask import make_response, render_template, Blueprint
from flask_login import login_required, current_user
from app.models import Transaction
import pdfkit

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/download_transactions_pdf', methods=['GET'])
@login_required
def download_transactions_pdf():

    # Query transactions for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Render the HTML template using Flask's render_template function
    rendered_template = render_template('transactions_report_template.html', transactions=transactions)

    # Define options for PDF generation
    pdf_options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }

    # Set the path to wkhtmltopdf executable in the configuration in Windows
    # config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # Set the path to wkhtmltopdf executable on Ubuntu
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    # REMEMBER to:
    # sudo apt-get update
    # sudo apt-get install wkhtmltopdf


    # Initialize PDFKit with the configuration
    pdfkit_from_string = pdfkit.PDFKit(rendered_template, 'string', options=pdf_options, configuration=config)

    # Generate the PDF using pdfkit
    pdf_file = pdfkit_from_string.to_pdf()

    # Create a response with the PDF data
    response = make_response(pdf_file)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=transactions.pdf'

    return response
