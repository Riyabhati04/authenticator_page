import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Initialize App
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_123") # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# --- Helper Functions ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Email and password are required.')
            return redirect(url_for('signup'))
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.')
            return redirect(url_for('signup'))
            
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/task/create', methods=['POST'])
@login_required
def create_task():
    title = request.form['title']
    if title:
        new_task = Task(title=title, user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/task/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/task/edit/<int:id>', methods=['POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == session['user_id']:
        new_title = request.form['title']
        if new_title:
            task.title = new_title
            db.session.commit()
    return redirect(url_for('dashboard'))

# --- Main ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
