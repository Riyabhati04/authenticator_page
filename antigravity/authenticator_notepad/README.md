# Task Manager Application

A simple, secure, and functional Task Manager web application built with Python, Flask, and SQLite.

## Features

- **User Authentication**: Secure Signup and Login using password hashing.
- **Task Management**: Create, Read, Update, and Delete (CRUD) tasks.
- **User Isolation**: Users can only see and manage their own tasks.
- **Responsive Design**: Clean and simple UI that works on desktop and mobile.

## Project Structure

```
task-manager/
├── app.py              # Main application logic (Backend + Routes)
├── database.db         # SQLite database (created on first run)
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── templates/          # HTML Templates
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
└── static/
    └── style.css       # CSS Styles
```

## Setup & Installation

1.  **Clone or Download** the project.
2.  **Navigate** to the project directory:
    ```bash
    cd task-manager
    ```
3.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Start the Application**:
    ```bash
    python app.py
    ```
2.  **Open in Browser**:
    Go to `http://127.0.0.1:5000`

## Test Cases

You can verify the application by following these steps:

1.  **Signup Flow**:
    - Go to `/signup`.
    - Enter a valid email and password.
    - Click "Sign Up".
    - **Expected**: Redirected to Login page with a success message.

2.  **Login Flow**:
    - Go to `/login`.
    - Enter the credentials created above.
    - Click "Login".
    - **Expected**: Redirected to Dashboard (`/dashboard`).

3.  **Create Task**:
    - On Dashboard, enter "Buy Groceries" in the input box.
    - Click "Add Task".
    - **Expected**: Page reloads, "Buy Groceries" appears in the list.

4.  **Edit Task**:
    - Click "Edit" next to "Buy Groceries".
    - Change text to "Buy Groceries & Milk".
    - Click "Save".
    - **Expected**: Task title updates in the list.

5.  **Delete Task**:
    - Click "Delete" next to the task.
    - **Expected**: Task is removed from the list.

6.  **Logout**:
    - Click "Logout" button.
    - **Expected**: Redirected to Login page. Try accessing `/dashboard` directly, should redirect to Login.

## Recommended VS Code Extensions

For the best development experience, install the following extensions:

- **Python** (`ms-python.python`): Essential for Python development.
- **Pylance** (`ms-python.vscode-pylance`): Provides fast and feature-rich language support.
- **Jinja** (`wholroyd.jinja`): Syntax highlighting for Flask templates.
- **SQLite Viewer** (`qwtel.sqlite-viewer`): Easily view and query your SQLite database.

## Approach


- **Backend**: Used Flask for its simplicity and flexibility. `Flask-SQLAlchemy` handles database interactions cleanly using ORM models (`User`, `Task`).
- **Security**: `werkzeug.security` is used for hashing passwords (PBKDF2) to ensure user data safety. `session` management is handled by Flask's secure cookie sessions.
- **Frontend**: Jinja2 templating allows dynamic content rendering. CSS is kept minimal but functional for a clean user experience.
