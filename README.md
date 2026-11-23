# 📖 MyRecord — Daily Life & Reflection Journal

**MyRecord** is an elegant, full-featured personal journaling and reflection web application built with **Django** and powered by **MySQL**. It allows you to document daily thoughts, track emotional wellness, attach multimedia memories (photos, voice notes, video clips), organize long-term aspirations into themed notebooks, and securely manage your account with full email verification and password recovery.

---

## 🎨 Design Philosophy & Color Palette

MyRecord features a modern split-screen aesthetic with a signature color system:
- **Forest Green (`#1f3d2b`)**: Calming organic tone used for sidebars, primary navigation, card surfaces, and buttons.
- **Sand Beige (`#e8dcc4`)**: Warm parchment tone for headlines, dates, tags, and delicate accents.
- **Electric Purple (`#8b5cf6`)**: Vibrant highlight color for active tabs, interactive controls, and analytics charts.

---

## ✨ Features

- 🔐 **Secure User Authentication**: Complete registration, login, logout, and account deletion with user data isolation.
- ✉️ **Email Verification**: New accounts require email confirmation before activation via secure, time-limited cryptographic tokens.
- 🔑 **Password Recovery (Forgot Password)**: Automated password reset workflow via Gmail SMTP.
- 📅 **Interactive Calendar & Diary Navigation**: Browse reflections by date or navigate forward/backward through monthly archives.
- 🎭 **Mood Tracking & Analytics**: Log your daily mood (Happy, Productive, Excited, Neutral, Tired, Sad, Angry) and visualize mood patterns with charts.
- ✍️ **Rich-Text Editor**: Powered by Quill.js with support for text formatting, bullet lists, blockquotes, and headers.
- 💾 **Real-Time Autosave**: Continuous background autosaving while writing entries and notebooks.
- 📸 **External Media Storage**: Dedicated media directory at `C:/myjournal` for photos, audio recordings, and videos.
- 💡 **Topic Notebooks**: Create separate thematic journals for long-term projects, reading notes, and personal goals.

---

## 🗄️ Database Architecture (MySQL)

MyRecord uses **MySQL** as its primary production-ready database engine.

### Database Connection Details
Database configuration is kept out of source code and loaded dynamically from the root [`.env`](.env) file:

```env
DB_NAME=myjournal
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### How Django Connects to MySQL
1. The project uses the native **`mysqlclient`** driver (configured in `myRecord/settings.py` under `DATABASES['default']`).
2. UTF-8 multi-byte charset (`utf8mb4`) is enforced to support international characters and emojis in journal entries.
3. `STRICT_TRANS_TABLES` mode is enabled to guarantee strict data integrity.

### Managing MySQL
- **MySQL Workbench**: Connect to `127.0.0.1:3306` with user `root` to inspect tables and run queries visually.
- **MySQL Command Line (CLI)**:
  ```bash
  mysql -u root -p
  CREATE DATABASE IF NOT EXISTS myjournal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

---

## 📁 Media Storage (`C:/myjournal`)

Uploaded user media (entry photos, audio voice notes, and video clips) is kept outside the code repository at:

```
C:/myjournal/
└── images/
    └── YYYY/
        └── MM/
            └── DD/
                └── uploaded_file.jpg
```

### Configuration in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = Path(r'C:\myjournal')

# Directory is automatically created if it does not exist
if not os.path.isdir(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, exist_ok=True)
```
In development mode (`DEBUG = True`), media is served directly via `django.conf.urls.static`.

---

## 📧 Email & Gmail SMTP Configuration

MyRecord sends real verification emails and password recovery links using **Gmail SMTP**.

### 1. Generating a Google App Password
1. Sign in to your Google Account and turn on **2-Step Verification** (under Security).
2. Go to **Security → 2-Step Verification → App passwords**.
3. Create an app password (e.g., named "MyRecord") and copy the 16-character code.

### 2. Configuring `.env`
Add the credentials to your [`.env`](.env) file (never commit this file to Git):

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
DEFAULT_FROM_EMAIL=MyJournal <your_email@gmail.com>
```

> **Tip:** You can switch back to printing emails in your terminal during offline development by setting:
> `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

### 3. Testing Email Delivery
Test your SMTP connection without making changes to the database:
```powershell
python manage.py send_test_email recipient@example.com
```
This utility command verifies the TLS connection, authenticates with Gmail, and sends a test message.

---

## 🔐 How the Authentication System Works

```
┌─────────────────┐       ┌──────────────────────┐       ┌─────────────────────┐
│ 1. User Signs Up├──────►│ 2. Account Created   ├──────►│ 3. Activation Email │
│ (Email + Pass)  │       │    (is_active=False) │       │    Sent via SMTP    │
└─────────────────┘       └──────────────────────┘       └──────────┬──────────┘
                                                                    │ User clicks link
┌─────────────────┐       ┌──────────────────────┐       ┌──────────▼──────────┐
│ 6. Access       │◄──────┤ 5. User Logs In      │◄──────┤ 4. Token Validated  │
│    Dashboard    │       │    (Active User)     │       │    (is_active=True) │
└─────────────────┘       └──────────────────────┘       └─────────────────────┘
```

### 1. User Registration
- Users register with **Username**, **Email Address**, **Password**, and **Confirm Password**.
- Email addresses must be unique (enforced case-insensitively).
- Passwords are validated using Django's built-in security validators (minimum length, similarity checks, common password checks).
- Upon sign-up, the account is created with `is_active = False`. The user cannot log in until their email is verified.

### 2. Email Verification Link & Token Generation
- Django generates a secure token using a custom `AccountActivationTokenGenerator` (`journal/tokens.py`), which hashes the user ID, timestamp, and active status (`is_active`).
- The link format is:
  `http://domain/activate/<uidb64>/<token>/`
- **Time-Limited**: The link expires automatically after 24 hours (`PASSWORD_RESET_TIMEOUT = 86400`).
- **One-Time Use**: Once the account is activated, `user.is_active` becomes `True`. Because `is_active` is part of the hash, the token is instantly invalidated and cannot be reused.

### 3. Resending Verification Emails
- If the email was missed or expired, users can request a new link at `/resend-verification/`.
- To prevent user enumeration attacks, a generic confirmation message is always displayed regardless of whether the email was found.

### 4. Verified Login Only
- If an unverified user attempts to log in, Django rejects authentication and displays a dedicated warning with a direct link to resend the verification email.
- Once verified, the user logs in and is redirected to their `/dashboard/`.

### 5. Forgot Password & Recovery Workflow
1. User clicks **"Forgot Password?"** on the login page (`/password-reset/`).
2. User enters their registered email address.
3. Django sends a secure, single-use password reset link.
4. User clicks the link to open the password confirmation form (`/password-reset-confirm/<uidb64>/<token>/`).
5. User enters and confirms their new password.
6. The password is encrypted, updated in MySQL, and the user is redirected to the login page.

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone <repository-url>
cd myRecord
```

### 2. Set Up Virtual Environment
```powershell
# Windows
python -m venv env
.\env\Scripts\activate

# Linux / macOS
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
DB_NAME=myjournal
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=MyJournal <your_email@gmail.com>
```

### 5. Create MySQL Database & Apply Migrations
```bash
# In MySQL terminal:
# CREATE DATABASE myjournal;

# In your terminal:
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 📂 Project Architecture

```
myRecord/
│── manage.py                                   # Django management tool
│── requirements.txt                            # Project dependencies
│── README.md                                   # Documentation
│── .env                                        # Secrets & DB/Email config (git-ignored)
│── .gitignore                                  # Git exclusion rules
│
│── myRecord/                                   # Project configuration
│   ├── __init__.py
│   ├── settings.py                             # Settings (MySQL, Media, SMTP, Auth)
│   ├── urls.py                                 # Root URL router
│   └── wsgi.py                                 # WSGI entry point
│
└── journal/                                    # Main journaling application
    ├── admin.py                                # Admin dashboard registration
    ├── apps.py
    ├── forms.py                                # Forms (Entry, Topic, Auth, Reset)
    ├── models.py                               # JournalEntry, JournalImage, Topic
    ├── tokens.py                               # Custom time-limited activation tokens
    ├── urls.py                                 # Application routes (Auth, Journal, Topics)
    ├── views.py                                # View logic & email handlers
    │
    ├── management/commands/
    │   └── send_test_email.py                  # Custom SMTP diagnostic CLI tool
    │
    ├── static/journal/                         # Static assets
    │   ├── css/style.css                       # Dashboard & journal design system
    │   └── css/login.css                       # Split-screen auth UI styling
    │
    └── templates/journal/                      # HTML templates
        ├── base.html                           # Main layout shell
        ├── dashboard.html                      # Calendar & mood analytics
        ├── auth/                               # Authentication templates
        │   ├── login.html                      # Login with inactive warnings & reset link
        │   ├── signup.html                     # Registration with email & pass validation
        │   ├── verification_sent.html          # Email sent confirmation
        │   ├── activation_success.html         # Successful email verification notice
        │   ├── activation_invalid.html         # Expired/invalid token notice
        │   ├── resend_verification.html        # Request fresh activation link
        │   ├── password_reset_form.html        # Enter email for password recovery
        │   ├── password_reset_done.html        # Reset email sent notice
        │   ├── password_reset_confirm.html     # Enter new password form
        │   └── password_reset_complete.html    # Password changed confirmation
        │
        ├── emails/                             # Email body templates
        │   ├── activation_email.html           # HTML account verification email
        │   ├── activation_email.txt            # Plain-text account verification email
        │   ├── password_reset_email.html       # HTML password reset email
        │   ├── password_reset_email.txt        # Plain-text password reset email
        │   └── password_reset_subject.txt      # Reset email subject
        │
        ├── entry/                              # Journal entry views
        │   ├── entry_form.html
        │   ├── entry_detail.html
        │   └── entry_confirm_delete.html
        │
        └── topic/                              # Topic notebook views
            ├── topic_list.html
            ├── topic_form.html
            ├── topic_detail.html
            └── topic_confirm_delete.html
```

---

## 🔒 Security Best Practices

- **Zero Hardcoded Secrets**: Passwords and keys are kept strictly in `.env`.
- **Git Protection**: `.env` and `*.env` are excluded via `.gitignore`.
- **Anti-Enumeration Protection**: The password reset and verification resend views never reveal whether an email address exists in the system.
- **CSRF Protection**: All forms include `{% csrf_token %}` to guard against Cross-Site Request Forgery.
- **Token Invalidation**: Email verification and password reset tokens expire after 24 hours and cannot be reused once processed.
