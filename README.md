# 📖 MyRecord — Daily Life & Reflection Journal

**MyRecord** is an elegant, full-featured personal journaling and reflection web application built with **Django**. It is designed to help you capture your thoughts, track your daily moods, archive memories with media attachments (photos, audio, video), and organize long-term aspirations into dedicated topic notebooks.

---

## 🎨 Design Philosophy & Color Palette

MyRecord features a high-end luxury aesthetic built around a signature palette:
- **Forest Green (`#1f3d2b`)**: Deep, calming natural tones for sidebars, navigation surfaces, and card backgrounds.
- **Sand Beige (`#e8dcc4`)**: Warm parchment tone for headlines, dates, tags, and organic details.
- **Electric Purple (`#8b5cf6`)**: Vibrant accent color used for buttons, interactive highlights, active tabs, and chart indicators.

---

## ✨ Features

- 🔐 **User Authentication**: Secure sign-up and log-in with private, user-isolated journal entries and topics.
- 📅 **Interactive Calendar & Diary Navigation**: View past entries by day or jump forward and backward across months.
- 🎭 **Mood Tracking & Visual Analytics**: Record how you feel each day (Happy, Productive, Excited, Neutral, Tired, Sad, Angry) and review your emotional distribution via dynamic charts.
- ✍️ **Rich-Text Editor**: Powered by Quill.js for formatting bold/italic notes, lists, headers, and colored text.
- 💾 **Real-Time Autosave**: Changes to entries and topics are saved automatically in the background as you write.
- 📸 **Rich Media Attachments**: Attach photos, audio voice notes, and video clips to any daily reflection.
- 💡 **Topic Notebooks**: Create separate thematic journals for long-term projects, reading notes, and personal goals.

---

## 🛠️ Prerequisites

Ensure you have the following installed on your machine:
- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **pip** (Python package installer)
- **Git** (optional, for cloning)

---

## 🚀 Quick Start Guide

### 1. Clone or Open the Repository
```bash
git clone <repository-url>
cd myRecord
```

### 2. Create and Activate a Virtual Environment

**On Windows:**
```powershell
python -m venv env
.\env\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Initialize the SQLite database schema:
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional, for Django Admin)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📖 How to Use MyRecord

### Step 1: Sign Up & Log In
1. Navigate to `http://127.0.0.1:8000/`.
2. If you don't have an account yet, click **"Sign up"** at the bottom.
3. Fill in your username and password, then submit. You will automatically be logged in and redirected to your dashboard.

### Step 2: Exploring the Dashboard
- **Header**: Shows the active month and navigation arrows (`<` and `>`) to browse your history.
- **Mood Analytics**: A bar chart displaying your mood trends over time.
- **Monthly Calendar Grid**: Days with existing reflections show your chosen mood emoji. Click on an empty day to add an entry for that date, or click an existing day to view the reflection.

### Step 3: Writing Daily Entries
1. Click **"Write Today"** (or **"Write Entry"** in the sidebar).
2. Select your mood for the day.
3. Write your thoughts in the Quill rich-text editor.
4. *(Optional)* Click on **Audio**, **Add Photos**, or **Video** to attach media.
5. Content autosaves automatically while you type. Click **"Save Reflection"** when finished.

### Step 4: Managing Topics & Goals
1. Click **"Topics"** in the sidebar.
2. Click **"Create Topic"** to start a notebook for any subject (e.g., *Fitness Journey*, *Reading List*, *Startup Ideas*).
3. Use the menu (`⋮`) on any topic card to edit or delete it anytime.

---

## 📂 Project Architecture

```
myRecord/
│── manage.py               # Django management script
│── requirements.txt        # Python package dependencies
│── README.md               # Project documentation
│── db.sqlite3              # Local SQLite database
│── myRecord/               # Main project configuration
│   ├── settings.py         # Global settings & apps
│   ├── urls.py             # Top-level URL routing
│   └── wsgi.py
└── journal/                # Core journaling application
    ├── models.py           # JournalEntry, JournalImage, Topic models
    ├── views.py            # Authentication, Dashboard, CRUD & Autosave views
    ├── forms.py            # ModelForms for entries & topics
    ├── urls.py             # App URL routes
    ├── static/journal/     # CSS stylesheets, images & scripts
    │   ├── css/style.css   # Main design system (Forest Green / Sand / Purple)
    │   └── css/login.css   # 3D interactive auth screen styling
    └── templates/journal/  # Django HTML templates
        ├── base.html       # Sidebar and layout shell
        ├── dashboard.html  # Calendar & analytics dashboard
        ├── auth/           # Login & Signup screens
        ├── entry/          # Daily reflection forms, views, delete
        └── topic/          # Topics list, detail, and edit screens
```

---

## 🔒 Security & Best Practices

- In production environments, remember to set `DEBUG = False` and configure `ALLOWED_HOSTS` in `myRecord/settings.py`.
- Keep your `SECRET_KEY` secret using environment variables (e.g., `python-dotenv`).
