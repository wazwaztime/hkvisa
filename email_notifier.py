"""
Email notification system for visa appointment updates
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime
import os


class EmailNotifier:
    """Send email notifications about visa appointments"""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def create_email_content(self, results: List[Dict]) -> str:
        """Create HTML email content from visa check results"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                h1 { color: #2c3e50; }
                .visa-card {
                    border: 2px solid #3498db;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 15px 0;
                    background-color: #ecf0f1;
                }
                .status-available { color: #27ae60; font-weight: bold; }
                .status-unavailable { color: #e74c3c; font-weight: bold; }
                .status-checking { color: #f39c12; font-weight: bold; }
                .status-error { color: #c0392b; font-weight: bold; }
                .info-row { margin: 8px 0; }
                .label { font-weight: bold; color: #34495e; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🌍 Hong Kong Visa Appointment Report</h1>
            <p><strong>Report Date:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        """
        
        if not results:
            html += "<p>No visa checks were performed.</p>"
        else:
            for result in results:
                status = result.get('status', 'unknown')
                status_class = f"status-{status}"
                
                html += f"""
                <div class="visa-card">
                    <h2>{result.get('country', 'Unknown Country')}</h2>
                    <div class="info-row">
                        <span class="label">Status:</span> 
                        <span class="{status_class}">{status.upper()}</span>
                    </div>
                """
                
                if result.get('earliest_date'):
                    html += f"""
                    <div class="info-row">
                        <span class="label">Earliest Available Date:</span> 
                        {result['earliest_date'].strftime('%Y-%m-%d')}
                    </div>
                    """
                
                html += f"""
                    <div class="info-row">
                        <span class="label">Message:</span> {result.get('message', 'N/A')}
                    </div>
                """
                
                if result.get('booking_url'):
                    html += f"""
                    <div class="info-row">
                        <span class="label">Booking URL:</span> 
                        <a href="{result['booking_url']}" target="_blank">{result['booking_url']}</a>
                    </div>
                    """
                
                html += """
                </div>
                """
        
        html += """
            <hr>
            <p style="color: #7f8c8d; font-size: 12px;">
                This is an automated report from the HK Visa Appointment Checker.<br>
                For questions or issues, please check the system logs.
            </p>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, recipient: str, subject: str, results: List[Dict]) -> bool:
        """Send email notification with visa appointment results"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = recipient
            
            # Create HTML content
            html_content = self.create_email_content(results)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✓ Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")
            return False
