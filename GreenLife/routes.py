from flask import render_template, url_for, flash, redirect
from greenlife import app
from greenlife.forms import RegistrationForm, LoginForm
from greenlife.models import User, Service, Appointment, Message, Query

posts = [
    {
        'author': 'Jeffery White',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jhon Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html.j2', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html.j2',title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html.j2', title="Register", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged In!', 'success')
            return redirect(url_for('home'))
        else: 
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('Login.html.j2', title="Login", form=form)