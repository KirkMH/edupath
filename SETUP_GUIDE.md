# EduPath Setup Guide

This guide takes you from a computer with nothing installed to EduPath running in your browser. It covers:

1. Installing Visual Studio Code (VS Code)
2. Installing Python
3. Installing Git and getting the project
4. Opening the project in VS Code
5. Creating a virtual environment
6. Installing Django and the other project requirements
7. Creating the `.env` file
8. Migrating the database
9. Running the app

Steps are given for **Windows** and **macOS**. Run every command in the VS Code terminal unless a step says otherwise.

---

## 1. Install Visual Studio Code

1. Go to <https://code.visualstudio.com/> and download the installer for your system.
2. Run the installer.
   - **Windows:** accept the defaults. On the **Select Additional Tasks** page, tick **Add "Open with Code" action** and **Add to PATH**.
   - **macOS:** open the downloaded `.zip` and drag **Visual Studio Code** into **Applications**.
3. Open VS Code.
4. Install the Python extension:
   1. Click the **Extensions** icon in the left sidebar, or press `Ctrl+Shift+X` (Windows) / `Cmd+Shift+X` (macOS).
   2. Search for **Python** and install the one published by **Microsoft**. It also installs **Pylance** and **Python Debugger**.
5. Optional: install the **Django** extension by **Baptiste Darthenay**. It adds syntax highlighting for Django templates.

---

## 2. Install Python

EduPath uses Django 5.2, which needs **Python 3.10 or newer**. Install the latest stable Python 3 release.

### Windows

1. Go to <https://www.python.org/downloads/> and download the latest Python 3 installer.
2. Run the installer. On the first screen, tick **Add python.exe to PATH**, then click **Install Now**.
3. When it finishes, close and reopen any open terminals so they pick up the new PATH.

### macOS

1. Go to <https://www.python.org/downloads/> and download the latest Python 3 installer for macOS.
2. Open the `.pkg` file and follow the prompts.
3. When it finishes, the installer opens a Finder window. Double-click **Install Certificates.command** in it. This lets Python make secure web requests, which EduPath needs to reach the O\*NET API.

### Check the installation

Open a new terminal and run:

- **Windows:**
  ```powershell
  python --version
  ```
- **macOS:**
  ```bash
  python3 --version
  ```

You should see `Python 3.10` or a later version. On Windows, if you get *"Python was not found"* or the Microsoft Store opens, Python is not on your PATH. Run the installer again, choose **Modify**, and make sure **Add Python to environment variables** is ticked.

---

## 3. Install Git and Get the Project

### Install Git

- **Windows:** download Git from <https://git-scm.com/download/win> and run the installer with the default options.
- **macOS:** open **Terminal** and run `git --version`. If Git is not installed, macOS asks to install the **Command Line Developer Tools**. Click **Install**.

Check it works:

```bash
git --version
```

### Clone the project

1. In VS Code, press `Ctrl+Shift+P` (Windows) / `Cmd+Shift+P` (macOS) to open the Command Palette.
2. Type **Git: Clone** and press Enter.
3. Paste the repository URL and press Enter:
   ```
   https://github.com/KirkMH/edupath.git
   ```
4. Choose a folder to save the project in.
5. When VS Code asks **Would you like to open the cloned repository?**, click **Open**.

If you already have the project folder (for example, from a `.zip` file), skip cloning and open it instead: **File → Open Folder…**, then select the folder that contains `manage.py`.

---

## 4. Open a Terminal in VS Code

Open the built-in terminal with **Terminal → New Terminal**, or press `` Ctrl+` ``.

The terminal opens in the project folder. Check that you are in the right place by listing the files. You should see `manage.py` and `requirements.txt`:

- **Windows:** `dir`
- **macOS:** `ls`

---

## 5. Create and Activate a Virtual Environment

A virtual environment keeps EduPath's packages separate from the rest of your computer. Create it once, inside the project folder:

- **Windows:**
  ```powershell
  python -m venv .venv
  ```
- **macOS:**
  ```bash
  python3 -m venv .venv
  ```

Activate it. You must do this every time you open a new terminal to work on the project:

- **Windows (PowerShell, the VS Code default):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **macOS:**
  ```bash
  source .venv/bin/activate
  ```

When it is active, the terminal prompt starts with `(.venv)`.

> **Windows: "running scripts is disabled on this system"**
> PowerShell blocks the activation script by default. Allow scripts for your user account, then run the activation command again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### Point VS Code at the virtual environment

1. Press `Ctrl+Shift+P` / `Cmd+Shift+P` and run **Python: Select Interpreter**.
2. Choose the entry that shows `.venv` (for example `Python 3.x ('.venv')`).

New VS Code terminals now activate the virtual environment for you.

From here on, use `python` on both Windows and macOS. Inside an active virtual environment, `python` always means the environment's Python.

---

## 6. Install Django and the Project Requirements

Django and every other package EduPath needs are listed in `requirements.txt`, with the exact versions the project was built with. Do not install Django on its own; install the whole list.

1. Upgrade `pip`, the Python package installer:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Install the requirements:
   ```bash
   python -m pip install -r requirements.txt
   ```

This installs:

| Package | Purpose |
| :--- | :--- |
| `Django` 5.2.17 | The web framework |
| `asgiref`, `sqlparse`, `tzdata` | Libraries Django depends on |
| `python-dotenv` | Reads settings from the `.env` file |
| `dotenv` | Older alias package for `python-dotenv` |
| `typing_extensions` | Python typing helpers |

Check that Django is installed:

```bash
python -m django --version
```

You should see `5.2.17`.

---

## 7. Create the `.env` File

EduPath reads two private settings from a file named `.env` in the project folder. The file is not stored in Git, so every computer needs its own.

1. In VS Code, right-click in the **Explorer** panel on the empty space below the files and choose **New File…**.
2. Name it `.env` (with the leading dot). It must sit next to `manage.py`.
3. Add these two lines:
   ```
   SECRET_KEY="paste-a-secret-key-here"
   ONET_API_KEY="paste-your-o-net-key-here"
   ```
4. Save the file.

### `SECRET_KEY`

Django uses this to sign sessions and passwords. Generate a random one with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it between the quotes.

### `ONET_API_KEY`

EduPath gets the 60 interest (RIASEC) questions and the interest scores from O\*NET Web Services. An O\*NET API key has already been provided for this project, so you do not need to register for one. The key is not stored in this guide or in Git; ask the project maintainer for it, then put it in place of `your-o-net-key-here`:

```
ONET_API_KEY="your-o-net-key-here"
```

Copy that whole line into your `.env` file in place of the `ONET_API_KEY` line from step 3.

Without a key, the app still starts and the interest scores are calculated locally. However, on a new, empty database the interest questions cannot be downloaded, so the Preference assessment will have no questions.

> **Keep `.env` private.** Never commit it to Git or share it. It is already listed in `.gitignore`.

---

## 8. Migrate the Database

EduPath uses SQLite, so there is no database server to install. The database is the file `db.sqlite3` in the project folder.

Apply the migrations. This creates the database file if it does not exist, and brings its tables up to date with the code:

```bash
python manage.py migrate
```

The output lists each migration followed by `OK`. If every migration has already been applied, it prints `No migrations to apply.`

### Load the starter data (new database only)

Skip this if your `db.sqlite3` already contains the questions and programs (for example, the copy that comes with the repository).

On a new, empty database, load the aptitude questions, the degree programs and their criteria, and the majors, **in this order**:

```bash
python seed_aptitude_questions.py
```

```bash
python seed_program_criteria.py
```

```bash
python seed_major_criteria.py
```

The majors script needs the programs from the second script, so run them in this order. The interest questions are downloaded from O\*NET the first time a student opens the Preference assessment.

### Create an admin account

Create an account for the admin site (`/admin/`), where questions, programs and criteria are managed:

```bash
python manage.py createsuperuser
```

Enter a username, an email address (optional) and a password when asked. The password is not shown while you type.

---

## 9. Run the App

Start the development server:

```bash
python manage.py runserver
```

When you see `Starting development server at http://127.0.0.1:8000/`, open these addresses in your browser:

| Address | What it is |
| :--- | :--- |
| <http://127.0.0.1:8000/> | EduPath home page; students sign up and sign in here |
| <http://127.0.0.1:8000/admin/> | Admin site; sign in with the account from step 8 |

The server reloads by itself when you save a code change. To stop it, click in the terminal and press `Ctrl+C`.

---

## Starting Work Again Later

Each time you come back to the project:

1. Open the project folder in VS Code.
2. Open a terminal (`` Ctrl+` ``). If `(.venv)` is not shown at the start of the prompt, activate the virtual environment (step 5).
3. If you pulled new code, install any new requirements and apply new migrations:
   ```bash
   python -m pip install -r requirements.txt
   ```
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

---

## Troubleshooting

| Problem | Fix |
| :--- | :--- |
| `ModuleNotFoundError: No module named 'django'` | The virtual environment is not active. Activate it (step 5), or select the `.venv` interpreter in VS Code. |
| `'python' is not recognized…` (Windows) | Python is not on your PATH. Re-run the Python installer, choose **Modify**, and tick **Add Python to environment variables**. Then open a new terminal. |
| `running scripts is disabled on this system` (Windows) | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again. |
| `Error: That port is already in use.` | Another server is using port 8000. Stop it, or run on another port: `python manage.py runserver 8001`. |
| `You have unapplied migration(s)…` when starting the server | Run `python manage.py migrate`. |
| The Preference assessment shows no questions | The interest questions could not be downloaded. Check that `ONET_API_KEY` in `.env` is correct and that you are online, then reload the page. |
| Pages show no styling | Make sure you started the app with `python manage.py runserver` and that `DEBUG = True` in `edupath/settings.py`. |
