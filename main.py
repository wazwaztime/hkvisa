#!/usr/bin/env python3
"""
Hong Kong Visa Appointment Checker
Main application for checking visa appointments and sending notifications
"""
import os
import sys
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from typing import List

from france_checker import FranceSchengenChecker
from us_checker import USVisaChecker
from australia_checker import AustraliaVisaChecker
from email_notifier import EmailNotifier


class VisaAppointmentChecker:
    """Main application for checking visa appointments"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv('config.env')
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', '')
        
        # Schedule configuration
        self.schedule_time = os.getenv('SCHEDULE_TIME', '09:00')
        
        # Feature flags
        self.check_france = os.getenv('CHECK_FRANCE_SCHENGEN', 'true').lower() == 'true'
        self.check_us = os.getenv('CHECK_US_VISA', 'true').lower() == 'true'
        self.check_australia = os.getenv('CHECK_AUSTRALIA_VISA', 'true').lower() == 'true'
        
        # Initialize checkers
        self.checkers = []
        if self.check_france:
            self.checkers.append(FranceSchengenChecker())
        if self.check_us:
            self.checkers.append(USVisaChecker())
        if self.check_australia:
            self.checkers.append(AustraliaVisaChecker())
        
        # Initialize email notifier
        if self.smtp_username and self.smtp_password:
            self.email_notifier = EmailNotifier(
                self.smtp_server,
                self.smtp_port,
                self.smtp_username,
                self.smtp_password
            )
        else:
            self.email_notifier = None
            print("⚠ Warning: Email credentials not configured. Notifications disabled.")
    
    def check_all_visas(self) -> List:
        """Check all enabled visa types"""
        print(f"\n{'='*70}")
        print(f"🔍 Starting visa appointment check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        results = []
        for checker in self.checkers:
            print(f"Checking {checker.country_name}...")
            result = checker.check_appointments()
            results.append(result)
            print(checker.format_result(result))
        
        return results
    
    def send_notification(self, results: List):
        """Send email notification with results"""
        if not self.email_notifier:
            print("⚠ Email notifications are disabled. Skipping.")
            return
        
        if not self.recipient_email:
            print("⚠ No recipient email configured. Skipping notification.")
            return
        
        subject = f"HK Visa Appointments - {datetime.now().strftime('%Y-%m-%d')}"
        success = self.email_notifier.send_email(self.recipient_email, subject, results)
        
        if success:
            print(f"✓ Notification sent to {self.recipient_email}")
        else:
            print(f"✗ Failed to send notification to {self.recipient_email}")
    
    def run_check_and_notify(self):
        """Run visa check and send notification"""
        results = self.check_all_visas()
        self.send_notification(results)
        print(f"\n{'='*70}")
        print("✓ Check completed")
        print(f"{'='*70}\n")
    
    def run_once(self):
        """Run the checker once and exit"""
        print("Running in one-time mode...")
        self.run_check_and_notify()
    
    def run_scheduled(self):
        """Run the checker on a schedule"""
        print(f"🕐 Scheduling daily checks at {self.schedule_time}")
        print(f"📧 Notifications will be sent to: {self.recipient_email}")
        print(f"Active checkers: {len(self.checkers)}")
        for checker in self.checkers:
            print(f"  - {checker.country_name}")
        print("\nPress Ctrl+C to stop\n")
        
        # Schedule the job
        schedule.every().day.at(self.schedule_time).do(self.run_check_and_notify)
        
        # Run once immediately on startup
        print("Running initial check...")
        self.run_check_and_notify()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     Hong Kong Visa Appointment Checker                      ║
    ║     查询香港各国签证预约时间系统                                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check if config file exists
    if not os.path.exists('config.env'):
        print("⚠ Warning: config.env not found. Using default/environment settings.")
        print("   Copy config.example.env to config.env and configure your settings.\n")
    
    checker = VisaAppointmentChecker()
    
    # Determine run mode
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        checker.run_once()
    else:
        try:
            checker.run_scheduled()
        except KeyboardInterrupt:
            print("\n\n✓ Scheduler stopped by user")
            sys.exit(0)


if __name__ == '__main__':
    main()
