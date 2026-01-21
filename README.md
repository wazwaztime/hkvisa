# 🌍 Hong Kong Visa Appointment Checker

香港签证预约时间查询系统 - 自动检查多国签证预约时间并发送邮件通知

A system to automatically check visa appointment availability from Hong Kong to various countries and send daily email notifications.

## ✨ Features

- 🇫🇷 **France Schengen Visa**: Check appointment times at TLS Contact Hong Kong
- 🇺🇸 **US Visa**: Monitor appointment availability at US Consulate Hong Kong
- 🇦🇺 **Australia Visa**: Track appointment slots at VFS Global Hong Kong
- 📧 **Daily Email Reports**: Receive automated daily updates via email
- ⏰ **Flexible Scheduling**: Configure check times to suit your needs
- 🎯 **Modular Design**: Easy to add more countries

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Email account for sending notifications (Gmail recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/wazwaztime/hkvisa.git
   cd hkvisa
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings**
   ```bash
   cp config.example.env config.env
   ```
   
   Edit `config.env` with your settings:
   ```env
   # Email configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   RECIPIENT_EMAIL=your-email@gmail.com
   
   # Schedule time (24-hour format)
   SCHEDULE_TIME=09:00
   
   # Enable/disable specific visa checkers
   CHECK_FRANCE_SCHENGEN=true
   CHECK_US_VISA=true
   CHECK_AUSTRALIA_VISA=true
   ```

### Gmail Setup

For Gmail users, you need to create an App Password:

1. Go to your Google Account settings
2. Select Security → 2-Step Verification (enable if not already enabled)
3. Select App passwords
4. Generate a new app password for "Mail"
5. Use this password in `SMTP_PASSWORD`

## 📖 Usage

### Run Once (Test Mode)

Check visa appointments immediately without scheduling:

```bash
python main.py --once
```

### Run Scheduled (Continuous Mode)

Start the scheduler to check appointments daily at the configured time:

```bash
python main.py
```

The system will:
1. Run an initial check immediately
2. Schedule daily checks at the configured time (default: 09:00)
3. Send email notifications after each check
4. Keep running until you press Ctrl+C

### Example Output

```
╔══════════════════════════════════════════════════════════════╗
║     Hong Kong Visa Appointment Checker                      ║
║     查询香港各国签证预约时间系统                                 ║
╚══════════════════════════════════════════════════════════════╝

🕐 Scheduling daily checks at 09:00
📧 Notifications will be sent to: your-email@gmail.com
Active checkers: 3
  - France (Schengen)
  - United States
  - Australia

Running initial check...

======================================================================
🔍 Starting visa appointment check - 2026-01-21 09:00:00
======================================================================

Checking France (Schengen)...
============================================================
Country: France (Schengen)
Status: CHECKING
Message: Service requires real-time web scraping. Please check at: ...
Checked at: 2026-01-21 09:00:05
============================================================

✓ Email sent successfully to your-email@gmail.com
✓ Check completed
```

## 🏗️ Project Structure

```
hkvisa/
├── main.py                  # Main application entry point
├── visa_checker_base.py     # Abstract base class for checkers
├── france_checker.py        # France Schengen visa checker
├── us_checker.py           # US visa checker
├── australia_checker.py    # Australia visa checker
├── email_notifier.py       # Email notification system
├── requirements.txt        # Python dependencies
├── config.example.env      # Example configuration file
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | Email account username | Required |
| `SMTP_PASSWORD` | Email account password/app password | Required |
| `RECIPIENT_EMAIL` | Email address to receive notifications | Required |
| `SCHEDULE_TIME` | Daily check time (24h format) | `09:00` |
| `CHECK_FRANCE_SCHENGEN` | Enable France Schengen checker | `true` |
| `CHECK_US_VISA` | Enable US visa checker | `true` |
| `CHECK_AUSTRALIA_VISA` | Enable Australia visa checker | `true` |

## 🌐 Supported Visa Types

### France (Schengen)
- **Application Center**: TLS Contact Hong Kong
- **Website**: https://cn.tlscontact.com/hk/HKG/page.php?pid=tourism

### United States
- **Application Center**: US Consulate General Hong Kong
- **Website**: https://ais.usvisa-info.com/en-hk/niv

### Australia
- **Application Center**: VFS Global Hong Kong
- **Website**: https://www.vfsglobal.com/en/individuals/australia.html

## 📝 Adding New Countries

To add support for a new country:

1. Create a new checker class (e.g., `uk_checker.py`):
   ```python
   from visa_checker_base import VisaChecker
   
   class UKVisaChecker(VisaChecker):
       def __init__(self):
           super().__init__("United Kingdom")
           # Add URLs and configuration
       
       def check_appointments(self):
           # Implement checking logic
           pass
   ```

2. Add it to `main.py`:
   ```python
   from uk_checker import UKVisaChecker
   
   # In __init__ method:
   self.check_uk = os.getenv('CHECK_UK_VISA', 'true').lower() == 'true'
   if self.check_uk:
       self.checkers.append(UKVisaChecker())
   ```

3. Add configuration to `config.env`:
   ```env
   CHECK_UK_VISA=true
   ```

## ⚠️ Important Notes

1. **Web Scraping**: The current implementation provides a framework. Actual appointment checking requires:
   - Implementing web scraping logic for each visa center
   - Handling authentication where required
   - Respecting rate limits and terms of service

2. **Legal Considerations**: 
   - Always comply with the terms of service of visa appointment websites
   - Respect robots.txt and rate limits
   - Consider using official APIs if available

3. **Security**:
   - Never commit `config.env` to version control
   - Use app passwords, not main account passwords
   - Keep dependencies updated

## 🐛 Troubleshooting

### Email Not Sending

- Verify SMTP credentials in `config.env`
- Check that 2-Step Verification is enabled (Gmail)
- Ensure you're using an App Password, not your regular password
- Check firewall/network settings

### No Appointments Found

- The current implementation is a framework
- Actual web scraping logic needs to be implemented
- Check if visa center websites have changed their structure

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Note**: This system provides a framework for checking visa appointments. Actual implementation of web scraping for each visa center should be done responsibly and in accordance with each website's terms of service.