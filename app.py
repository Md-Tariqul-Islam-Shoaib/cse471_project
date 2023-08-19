from flask import Flask, render_template, request, redirect, session, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import bcrypt

share = Share()
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/admin/login'

app.secret_key = 'secret_key'
app.app_context().push()

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

@app.route('/register', methods=['Get', 'POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

