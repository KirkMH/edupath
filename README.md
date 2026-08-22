# EduPath

**EduPath** is a Django-based web application designed to guide students toward suitable academic programs and career paths. By combining **aptitude assessments** with **O*NET RIASEC interest profiling** (Realistic, Investigative, Artistic, Social, Enterprising, Conventional), EduPath analyzes student responses and delivers personalized program recommendations, alignment insights, and score breakdowns.

---

## 🚀 Features

- **Aptitude & Interest Assessments**: Dynamic tests to evaluate student skills and RIASEC interest dimensions.
- **Personalized Recommendations**: Top recommended academic programs tailored to each student's profile.
- **Student Profile Management**: Tracking student demographics, test activity, and historical results.
- **Customization & Admin Panel**: Admin controls for managing questions, programs, and assessment parameters.

---

## 📋 Prerequisites

Before running EduPath, ensure you have the following installed:

- **Python 3.10+**
- **Git**
- **pip** (Python package installer)

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/KirkMH/edupath.git
cd edupath
```

*(Note: If the codebase is inside a subfolder such as `code`, navigate into that directory where `manage.py` is located).*

---

### 2. Create a Virtual Environment

Create an isolated Python virtual environment:

- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt):**
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```

- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

---

### 3. Install Dependencies

Install the required Python packages specified in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables (`.env`)

Create a `.env` file in the root directory of the project (the directory containing `manage.py`):

```bash
# Example file creation (.env)
SECRET_KEY="your-custom-secret-key-here"
```

> **Note**: Replace `"your-custom-secret-key-here"` with your actual secret key or development key.

---

### 5. Run Database Migrations

Set up the database schema by applying migrations:

```bash
python manage.py migrate
```

---

### 6. Create an Admin User (Optional)

To access the Django Admin dashboard (`/admin/`), create a superuser account:

```bash
python manage.py createsuperuser
```

Follow the prompts to specify a username, email, and password.

---

### 7. Run the Development Server

Start the local development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 📁 Project Structure

```
EduPath/
├── assessment/          # Student profile, assessment processing, and view logic
├── customization/       # Program definitions, aptitude & interest question management
├── edupath/             # Core project configuration (settings, URLs, WSGI)
├── static/              # CSS styles, images, and static assets
├── templates/           # HTML templates (Auth, Assessment, Dashboard, Admin)
├── .env                 # Environment variables configuration
├── .gitignore           # Git ignore rules
├── db.sqlite3           # SQLite database
├── manage.py            # Django management script
└── requirements.txt     # Python project dependencies
```
