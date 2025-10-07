<div align="center">

# 🚀 Gmail Email Resender Pro
### *Intelligent Email Management & Automation System*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Gmail API](https://img.shields.io/badge/Gmail-API%20v1-red- 📊 **Scalable**: Handle hundreds of emailssvg)](https://developers.google.com/gmail/api)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/user/repo)

*Automate your email follow-ups with professional precision and intelligent scheduling*

[📋 Features](#-features) • [🎯 Quick Start](#-quick-start) • [🖥️ User Interface](#-user-interface) • [⚙️ Configuration](#-configuration) • [📊 Use Cases](#-use-cases)

</div>

---

## 🌟 What Makes This Special?

This isn't just another email automation tool. It's a **professional-grade email management system** that combines Gmail's native scheduling capabilities with intelligent filtering, recipient tracking, and interactive controls to help you manage your email communications efficiently and professionally.

## ✨ Features

### 🎯 **Smart Email Processing**
- **🤖 AI-Powered Filtering**: Automatically identifies emails using customizable keyword matching
- **🔍 Intelligent Parsing**: Extracts recipient, subject, content, and attachments with precision
- **📧 Professional Formatting**: Maintains original email structure and formatting
- **📎 Attachment Handling**: Preserves all attachments (PDFs, documents, images)

### 🕐 **Advanced Scheduling System**
- **⚡ Instant Send**: Immediate processing and delivery
- **📝 Draft Creation**: Generate drafts for manual scheduling in Gmail
- **⏰ Gmail-Style Scheduling**: Schedule delivery using Gmail's native scheduler
- **🗓️ Task Automation**: Windows Task Scheduler integration for automated execution
- **🔄 Background Processing**: Set-and-forget automation

### 🛡️ **Professional Safety Features**
- **🚫 Smart Exclusion System**: Permanent email exclusion with comment support
- **📊 Recipient Tracking**: Automatic counting of emails sent to each recipient
- **🔒 Duplicate Prevention**: Prevents sending duplicate emails
- **⚖️ Rate Limiting**: Configurable delays to respect Gmail API limits
- **� Email Validation**: Advanced recipient email validation

### 🎮 **Interactive User Experience**
- **👤 Interactive Mode**: Review each email before sending with rich previews
- **📋 Batch Processing**: Fully automated sending for large volumes
- **🧪 Dry Run Mode**: Test functionality without sending actual emails
- **� Real-time Progress**: Live progress tracking and status updates
- **📊 Comprehensive Reporting**: Detailed success/failure analytics

### 🔧 **Enterprise-Grade Configuration**
- **⚙️ Environment Variables**: Flexible configuration via `.env` files
- **📁 File-based Exclusions**: Manage excluded emails via external files
- **🎛️ Granular Controls**: Fine-tune every aspect of the sending process
- **� Comprehensive Logging**: Debug-level logging for troubleshooting

---

## 🖥️ User Interface

### 📱 **Interactive Dashboard**
When you launch the application, you're greeted with a clean, intuitive interface:

```
==================================================
📧 GMAIL EMAIL RESENDER PRO
==================================================
🎯 Intelligent Email Management System
⚡ Version 2.0 | Production Ready
==================================================

📊 SYSTEM STATUS
✅ Gmail API: Connected
✅ Credentials: Valid  
✅ Configuration: Loaded
📁 Exclusion List: 12 emails loaded
📊 Processing Limit: 200 emails per run

==================================================
EMAIL PROCESSING OPTIONS
==================================================
Choose how to handle emails:
1. 🚀 Send immediately
2. 📝 Create drafts only (you'll schedule in Gmail)  
3. ⏰ Schedule delivery time (create drafts now, deliver later)
4. 🗓️ Schedule script execution time (run script later)

Enter your choice (1-4): _
```

### 🎨 **Email Preview Interface**
Rich email previews help you make informed decisions:

```
============================================================
📧 Email 3/15 | 📊 Progress: 20%
============================================================
📧 To: contact@example.com
📋 Subject: Follow-up: Project Collaboration Opportunity
📅 Date: Wed, 1 Nov 2023 10:30:00 +0000
🏢 Domain: example.com (Auto-detected)
📊 Emails sent to this recipient: 1/2
============================================================

📝 EMAIL PREVIEW:
Dear Team,

I hope this message finds you well. I wanted to follow up 
on our previous conversation regarding the potential 
collaboration opportunity. I believe our organizations could 
benefit greatly from working together...

📎 Attachments: document.pdf, proposal.pdf
💡 Keywords detected: follow-up, collaboration, opportunity

============================================================
Do you want to resend this email? 
[Y]es | [N]o | [E]xclude permanently | [Q]uit: _
```

### 📊 **Real-time Analytics Dashboard**
Track your progress with live statistics:

```
==================================================
📊 PROCESSING ANALYTICS
==================================================
⏱️  Processing Time: 2m 34s
📧 Total Found: 47 emails
✅ Successfully Sent: 12 emails  
⏭️  Skipped: 8 emails
❌ Errors: 0 emails
🚫 Excluded: 3 emails
📈 Success Rate: 100%

==================================================
📋 RECIPIENT BREAKDOWN
==================================================
🏢 New Recipients: 8
🔄 Previous Recipients: 4 
🚫 At Send Limit: 3
⭐ High-Priority Contacts: 2

==================================================
⏰ NEXT SCHEDULED RUN
==================================================
📅 Date: Tomorrow at 9:00 AM
🎯 Estimated Emails: 15-20
📝 Mode: Automatic (Non-Interactive)
```

### 🎭 **Visual Status Indicators**
Clear visual feedback throughout the process:

- 🟢 **Success**: Green indicators for completed actions
- 🟡 **Warning**: Yellow for skipped or excluded emails  
- 🔴 **Error**: Red for failures or issues
- 🔵 **Info**: Blue for informational messages
- ⚡ **Action**: Lightning bolt for user actions required

---

## 🎯 Quick Start

### 📦 **One-Command Installation**
```bash
# Clone and setup in one command
git clone https://github.com/yourusername/gmail-resender-pro && cd gmail-resender-pro && pip install -r requirements.txt
```

### ⚡ **Requirements**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

### 🔐 **Gmail API Setup** (2 minutes)
1. **Create Project**: Visit [Google Cloud Console](https://console.cloud.google.com/)
2. **Enable Gmail API**: Search "Gmail API" → Enable
3. **Create Credentials**: APIs & Services → Credentials → Create OAuth 2.0 Client ID
4. **Download**: Save as `credentials/credentials.json`
5. **Done!** 🎉

### 🚀 **Launch Application**
```bash
python main.py
```

---

## 🎮 Usage Scenarios

### 🚀 **Scenario 1: Immediate Professional Follow-ups**
Perfect for urgent communications or immediate follow-ups:

```bash
python main.py
# Choose option 1: Send immediately
# Review each email interactively
# Send with professional delay between emails
```

**Best for**: Time-sensitive communications, small batches (5-10 emails)

### 📝 **Scenario 2: Gmail Native Scheduling** ⭐ **RECOMMENDED**
Leverage Gmail's powerful scheduling features:

```bash
python main.py
# Choose option 2: Create drafts only
# ✅ Script creates drafts with all content & attachments
# ✅ You schedule each one manually in Gmail
# ✅ Works even when computer is offline
```

**Benefits**: 
- 🎯 **Precision Control**: Schedule each email individually
- ⚡ **Gmail Features**: Use Gmail's smart scheduling suggestions
- 🔒 **Reliability**: Gmail handles delivery even if your computer is off
- 🎨 **Customization**: Edit drafts before scheduling

### ⏰ **Scenario 3: Automated Batch Scheduling**
Professional batch scheduling for strategic timing:

```bash
python main.py
# Choose option 3: Schedule delivery time  
# Enter: 2024-12-23 (Monday)
# Enter: 09:00 (Professional morning time)
# ✅ Creates drafts scheduled for Monday 9 AM
# ✅ Gmail automatically sends at scheduled time
```

**Perfect for**: 
- 📅 **Strategic Timing**: Schedule for optimal open rates
- 🌍 **Time Zone Optimization**: Target recipient's business hours
- 📊 **Batch Processing**: Handle 20-50 emails efficiently

### 🗓️ **Scenario 4: Advanced Task Automation**
Enterprise-level automation with Windows Task Scheduler:

```bash
python main.py
# Choose option 4: Schedule script execution
# Creates Windows Task Scheduler entry
# Script runs automatically at specified time
# Perfect for recurring weekly follow-ups
```

**Enterprise Features**:
- 🔄 **Recurring Execution**: Weekly, bi-weekly automation
- � **Background Processing**: No user intervention required
- 📈 **Scalable**: Handle hundreds of applications
- 📜 **Audit Trail**: Comprehensive logging for compliance

---

## 🎨 Advanced Features

### 🧠 **Smart Email Detection**
The system uses advanced algorithms to identify emails based on customizable keywords:

```python
# Intelligent keyword matching (customizable)
EMAIL_KEYWORDS = [
    "follow-up", "reminder", "check-in", "update", "inquiry",
    "proposal", "meeting", "collaboration", "opportunity", "project",
    "application", "job", "resume", "cover letter", "position"
]
```

### 🛡️ **Professional Safety Systems**

#### 🚫 **Smart Exclusion Management**
```bash
# excluded_emails.txt supports comments and organization
# ========================================
# AUTOMATED SYSTEMS / NO-REPLY ADDRESSES
# ========================================
noreply@automated-system.com
donotreply@newsletter-service.com

# ========================================  
# CONTACTS THAT EXPLICITLY REQUESTED NO RESENDS
# ========================================
contact@sensitive-client.com    # Requested no follow-ups on 2023-11-15
```

#### 📊 **Intelligent Recipient Tracking**
- **Automatic Counting**: Tracks all emails sent to each recipient
- **Configurable Limits**: Prevent over-emailing (default: 2 emails max)
- **Professional Compliance**: Maintains professional relationships

#### � **Duplicate Prevention Engine**
- **Subject + Recipient Matching**: Prevents exact duplicates
- **Cross-Session Memory**: Remembers across different runs
- **Smart Detection**: Identifies similar emails with different timestamps

---

## 🎯 Use Cases & Applications

### 💼 **Business & Professional**
- **📧 Sales Follow-ups**: Resend proposals, quotes, and sales communications
- **🤝 Client Relations**: Follow up on project updates, meeting requests
- **📋 Invoice Reminders**: Automated payment follow-ups and billing communications
- **🔄 Contract Follow-ups**: Resend contracts, agreements, and legal documents
- **📊 Report Distribution**: Resend monthly/quarterly reports to stakeholders

### 🎓 **Academic & Educational**
- **📚 Research Collaborations**: Follow up on research proposals and partnerships
- **🎯 Conference Submissions**: Resend paper submissions and presentation proposals
- **👨‍🎓 Student Communications**: Follow up on application materials and documents
- **📖 Publication Follow-ups**: Resend journal submissions and editorial communications

### 🏢 **Recruitment & HR**
- **💼 Job Applications**: Automated follow-ups for application submissions
- **📋 Interview Scheduling**: Resend interview invitations and scheduling emails
- **🎯 Candidate Communications**: Follow up with potential candidates
- **📊 Reference Requests**: Resend reference and recommendation requests

### 🤝 **Networking & Partnerships**
- **🌐 Professional Networking**: Follow up on LinkedIn connections and introductions
- **🤝 Partnership Proposals**: Resend collaboration and partnership opportunities
- **📅 Event Invitations**: Follow up on conference, webinar, and event invitations
- **💡 Speaking Opportunities**: Resend speaking proposals and event submissions

### 🛒 **E-commerce & Marketing**
- **🛍️ Product Inquiries**: Follow up on product demonstrations and consultations
- **📈 Marketing Campaigns**: Resend promotional materials to targeted segments
- **🎯 Customer Outreach**: Follow up on customer feedback and survey requests
- **💳 Payment Issues**: Automated follow-ups for failed payments or renewals

### 🏥 **Healthcare & Services**
- **⚕️ Appointment Reminders**: Follow up on medical appointment confirmations
- **📋 Insurance Claims**: Resend documentation and claim follow-ups
- **💊 Prescription Refills**: Automated pharmacy and medication reminders
- **🩺 Health Surveys**: Follow up on patient feedback and health questionnaires

### 🏠 **Real Estate & Property**
- **🏡 Property Inquiries**: Follow up on listing inquiries and viewing requests
- **📄 Documentation**: Resend contracts, lease agreements, and property documents
- **💰 Investment Opportunities**: Follow up on property investment proposals
- **🔧 Maintenance Requests**: Automated follow-ups for property maintenance issues

### 🎨 **Creative & Freelance**
- **🎨 Portfolio Submissions**: Follow up on design and creative project proposals
- **📝 Content Creation**: Resend writing samples and content proposals
- **📸 Photography Services**: Follow up on photography booking inquiries
- **🎵 Music & Entertainment**: Resend performance proposals and booking requests

---

## ⚙️ Configuration

### 🎛️ **Environment Variables** (`.env` file)

Create a `.env` file in your project root for easy configuration:

```bash
# ============================================
# 🔧 CORE SETTINGS
# ============================================
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
DRY_RUN=false                     # Test mode without sending emails
INTERACTIVE_MODE=true             # Ask before sending each email

# ============================================  
# 📧 EMAIL PROCESSING
# ============================================
MAX_EMAILS_PER_RECIPIENT=2        # Max emails to same recipient
MAX_EMAILS_PER_RUN=200           # Max emails to process per run
SEND_DELAY=2.0                   # Seconds between sends (API rate limiting)

# ============================================
# 🚫 EXCLUSION MANAGEMENT  
# ============================================
EXCLUSION_FILE=excluded_emails.txt    # File containing excluded emails
AUTO_EXCLUDE_AFTER_SEND=true         # Auto-add recipients after sending

# ============================================
# 📊 ADVANCED ANALYTICS
# ============================================
ENABLE_ANALYTICS=true            # Track detailed statistics
ANALYTICS_FILE=analytics.json    # Analytics data storage
COMPANY_DETECTION=true           # Auto-detect company names
```

### 📋 **Configuration Reference Table**

| 🔧 Setting | 📊 Default | 📝 Description | 🎯 Best Practice |
|------------|------------|----------------|------------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity | Use `DEBUG` for troubleshooting |
| `DRY_RUN` | `false` | Test without sending | Always test with `true` first |
| `INTERACTIVE_MODE` | `true` | User confirmation | Use `false` for automation |
| `MAX_EMAILS_PER_RECIPIENT` | `2` | Recipient email limit | Keep ≤ 3 for professionalism |
| `MAX_EMAILS_PER_RUN` | `200` | Batch processing limit | Adjust based on account limits |
| `SEND_DELAY` | `2.0` | Anti-spam delay | Increase if hitting rate limits |
| `AUTO_EXCLUDE_AFTER_SEND` | `true` | Auto-exclusion | Recommended for clean management |

### 🎯 **Email Detection Keywords**

Customize the keywords used to identify emails for resending in `config.py`:

```python
# 🔍 Smart Email Detection Keywords
EMAIL_KEYWORDS = [
    # Follow-up & Communication Terms
    "follow-up", "reminder", "check-in", "update", "inquiry",
    
    # Business & Professional Terms  
    "proposal", "meeting", "collaboration", "opportunity", "project",
    
    # Application & Recruitment Terms (if needed)
    "application", "job", "resume", "cover letter", "position",
    
    # Custom Keywords (Add your specific terms)
    "invoice", "contract", "partnership", "consultation", "demo"
]
```

### 🏢 **Professional Email Templates**

Customize the resend message in `config.py`:

```python
# 📧 Professional Resend Message (Customizable)
RESEND_MESSAGE = """
I hope this email finds you well. I wanted to follow up on my previous 
message to ensure it reached you successfully. 

I wanted to bring this to your attention again as I believe it may be 
of interest to you and your team.

Thank you for your time and consideration.

Best regards,
[Your Name]

---Original Message---
"""
```

---

## Email Exclusion

### Exclusion File
You can maintain a list of email addresses to permanently exclude from resending by creating or editing `excluded_emails.txt` (or the file specified in `EXCLUSION_FILE`).

**Format**:
- One email address per line
- Lines starting with `#` are treated as comments
- Email addresses are case-insensitive
- Empty lines are ignored

**Example `excluded_emails.txt`**:
```
# Companies that don't accept application resends
hr@company1.com
recruiter@example.org

# Automated systems
noreply@automated-system.com
donotreply@jobsite.com
```

### Interactive Exclusion
In interactive mode, you can permanently exclude emails by:
1. When prompted for an email, choose `e` or `exclude`
2. The email will be added to your exclusion file automatically
3. Future runs will skip this email address

### Auto-Exclusion After Sending
By default, the script automatically adds recipients to the exclusion list after successfully sending them an email. This ensures you won't accidentally resend to the same recipients in future runs.

**To disable auto-exclusion:**
```bash
AUTO_EXCLUDE_AFTER_SEND=false
```

**Behavior:**
- ✅ **Enabled (default)**: Recipients are automatically excluded after sending
- ❌ **Disabled**: You can resend to the same recipients in future runs (subject to `MAX_EMAILS_PER_RECIPIENT` limit)

## Recipient Email Limits

The script automatically tracks how many emails you've sent to each recipient and prevents over-emailing.

### How It Works
- Before resending, the script searches your entire sent folder
- Counts all emails previously sent to each recipient
- Skips recipients who have already received the maximum number of emails
- Default limit is 2 emails per recipient (configurable)

### Configuration
Set `MAX_EMAILS_PER_RECIPIENT` in your `.env` file:
```bash
# Allow maximum 3 emails to the same recipient
MAX_EMAILS_PER_RECIPIENT=3
```

### Example Scenarios
- **Recipient A**: Sent 1 email previously → ✅ Will resend
- **Recipient B**: Sent 2 emails previously (at limit) → ❌ Will skip
- **Recipient C**: Sent 3+ emails previously → ❌ Will skip

This prevents you from appearing spammy by sending too many applications to the same company.

## 📝 Example Usage Scenarios

### Scenario 1: Send Immediately
```bash
python main.py
# Choose option 1: Send immediately
# Process emails right away with interactive confirmation
```

### Scenario 2: Schedule for Business Hours
```bash
python main.py
# Choose option 2: Schedule for specific time today
# Enter: 09:00 (for 9 AM)
# Script creates task and exits immediately
# At 9 AM: Script runs automatically and sends emails
```

### Scenario 3: Schedule for Monday Morning
```bash
python main.py
# Choose option 3: Schedule for specific date and time
# Enter date: 2024-12-23
# Enter time: 08:30
# Script creates task and exits immediately
# On Monday 8:30 AM: Script runs automatically
```

### Scenario 4: Automatic Batch Processing
```bash
# Set INTERACTIVE_MODE=false in .env
python main.py
# Choose scheduling option
# Script creates task for automatic sending (no user prompts)
```

## Email Preview

In interactive mode, the script shows:
- Recipient email address
- Subject line
- Send date
- First 200 characters of email body

## Safety Features

- **Duplicate Prevention**: Won't resend to the same recipient for the same subject
- **Email Validation**: Validates recipient email addresses
- **Rate Limiting**: Configurable delays between sends
- **Comprehensive Logging**: All actions are logged to `logs/resender.log`

## Example Output

```
============================================================
Email 1/5
To: hr@company.com
Subject: Application for Software Developer Position
Date: Wed, 1 Nov 2023 10:30:00 +0000
============================================================
Body preview:
Dear Hiring Manager,

I am writing to express my interest in the Software Developer position posted on your company website. With 5 years of experience in Python development...

Do you want to resend this email? (y/n/e to exclude permanently/q to quit): y
✓ Email sent successfully to hr@company.com
```

## Troubleshooting

1. **Authentication Issues**: Delete `token.json` and re-run to re-authenticate
2. **No Emails Found**: Check that your keywords match your sent emails
3. **Rate Limiting**: Increase `SEND_DELAY` if you encounter API limits

## Security Notes

- Credentials are stored locally in `credentials/`
- The script only reads sent emails and sends new emails
- All email processing is done locally
- Consider using app-specific passwords for enhanced security