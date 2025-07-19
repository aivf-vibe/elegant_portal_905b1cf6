
#!/usr/bin/env python3
"""
DentalFlow CRM Landing Page Backend
Handles contact form submissions and sends emails
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=['*'])

# Email configuration
SMTP_CONFIG = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'user': 'noreply@aivf.io',
    'password': 'qzvdqdnejuyugmpq',
    'from_email': 'noreply@aivf.io',
    'to_email': 'info@vibestud.io'
}

def send_email(form_data):
    """Send email notification for new contact form submission"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"New DentalFlow CRM Inquiry - {form_data.get('practice_name', 'Unknown Practice')}"
        msg['From'] = SMTP_CONFIG['from_email']
        msg['To'] = SMTP_CONFIG['to_email']
        
        # Create email body
        text_body = f"""
        New DentalFlow CRM Inquiry
        
        Practice Name: {form_data.get('practice_name', 'N/A')}
        Contact Name: {form_data.get('contact_name', 'N/A')}
        Email: {form_data.get('email', 'N/A')}
        Phone: {form_data.get('phone', 'N/A')}
        Practice Size: {form_data.get('practice_size', 'N/A')}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0ea5e9;">New DentalFlow CRM Inquiry</h2>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #1e293b; margin-bottom: 15px;">Contact Information</h3>
                    <p><strong>Practice Name:</strong> {form_data.get('practice_name', 'N/A')}</p>
                    <p><strong>Contact Name:</strong> {form_data.get('contact_name', 'N/A')}</p>
                    <p><strong>Email:</strong> <a href="mailto:{form_data.get('email', '')}">{form_data.get('email', 'N/A')}</a></p>
                    <p><strong>Phone:</strong> <a href="tel:{form_data.get('phone', '')}">{form_data.get('phone', 'N/A')}</a></p>
                    <p><strong>Practice Size:</strong> {form_data.get('practice_size', 'N/A')}</p>
                </div>
                
                <div style="background: #e0f2fe; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #0369a1;">
                        <strong>Submitted:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
                    <p style="color: #64748b; font-size: 14px;">
                        This inquiry was submitted through the DentalFlow CRM landing page.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach parts
        text_part = MIMEText(text_body, 'plain')
        html_part = MIMEText(html_body, 'html')
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as server:
            server.starttls()
            server.login(SMTP_CONFIG['user'], SMTP_CONFIG['password'])
            server.send_message(msg)
            
        logger.info(f"Email sent successfully for {form_data.get('email', 'unknown')}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@app.route('/')
def index():
    """Serve the main landing page"""
    return open('index.html').read()

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['practice_name', 'contact_name', 'email', 'phone', 'practice_size']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Send email
        email_sent = send_email(data)
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Thank you! We\'ll contact you within 24 hours to set up your free trial.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send email. Please try again or contact us directly.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error handling contact form: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 53725))
    app.run(host='0.0.0.0', port=port, debug=False)

