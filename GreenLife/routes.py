from flask import render_template, url_for, flash, redirect, request, abort
from greenlife import app, db, bcrypt, mail
from greenlife.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                             ServiceForm, RequestResetForm, ResetPasswordForm)
from greenlife.models import (User, Service, Appointment, Message,
                               Query, ServiceType, Role, Admin, Therapist)
from flask_login import login_user, current_user, logout_user, login_required
from greenlife.auth_decorators import role_required
import secrets
import os
from PIL import Image
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html.j2')

@app.route("/about")
def about():
    return render_template('about.html.j2',title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role = Role.query.filter_by(name='user').first()
        if role:
            role_id = role.id
        else:
            role_id = None
        user = User(username = form.username.data, 
                    full_name=form.full_name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    role_id=role_id,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! you are able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', title="Register", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page= request.args.get('next')
            if (next_page):
                return redirect(next_page)
            elif (user.role.name == 'admin' ):
                return redirect(url_for('account'))
            elif (user.role.name == 'therapist'):
                return redirect(url_for('about'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('Login.html.j2', title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html.j2',title='Account', image_file=image_file, form=form)

@app.route("/service")
@login_required
def service():
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.date_created.desc()).paginate(page=page, per_page=5)
    return render_template('service.html.j2', title="Services", services=services)

@app.route("/service/new",  methods=['GET','POST'])
@login_required
@role_required('admin', 'therapist')
def new_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(name=form.name.data, 
                          description=form.description.data,
                          user_id=current_user.id,
                          service_type_id=form.service_type.data,
                          duration_options_id = form.duration.data,
                          price=form.price.data)
        db.session.add(service)
        db.session.commit()
        flash('Your service has been created!', 'success')
        return redirect(url_for('service'))
    return render_template('create_service.html.j2', title='New Service', form=form,legend='New Service')

@app.route("/service/<int:service_id>")
@login_required
@role_required('admin', 'therapist')
def view_service(service_id):
    service =  Service.query.get_or_404(service_id)
    return render_template('view_service.html.j2', title='View Service', service=service)


@app.route("/service/<int:service_id>/update", methods=['GET','POST'])
@login_required
@role_required('admin', 'therapist')
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    if not (service.user_service == current_user or current_user.role.name == 'admin'):
        abort(403)
    form = ServiceForm(obj=service)
    form.original_name = service.name
    form.original_description = service.description
    form.original_service_type = service.service_type_id
    form.original_duration = service.duration_options_id
    form.original_price = service.price
    if form.validate_on_submit():
        if form.is_updated(form.name, form.description, form.service_type, form.duration, form.price):
            flash('No changes detected', 'warning')
            return redirect(url_for('service'))
        else:
            service.name = form.name.data
            service.description = form.description.data
            service.service_type_id = form.service_type.data
            service.duration_options_id = form.duration.data
            service.price = form.price.data
            db.session.commit()
            flash('Your service updated successfully', 'success')
            return redirect(url_for('service'))
    elif request.method == 'GET':
        form.name.data = service.name
        form.description.data = service.description
        form.service_type.data = str(service.service_type_id)
        form.duration.data = str(service.duration_options_id)
        form.price.data = service.price
    return render_template('create_service.html.j2', title='Update Service', form=form,
                           legend='Update Service')

@app.route("/service/<int:service_id>/delete", methods=['POST'])
@login_required
@role_required('admin', 'therapist')
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    if not (service.user_service == current_user or current_user.role.name == 'admin'):
        abort(403)
    db.session.delete(service)
    db.session.commit()
    flash('Your service has been deleted', 'success')
    return redirect(url_for('service'))

@app.route("/user/<string:username>")
@login_required
def user_services(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    services = Service.query.filter_by(user_service=user)\
        .order_by(Service.date_created.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_services.html.j2', title='Users', services=services, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender=('Green Life', 'jeffery1996.jbw@gmail.com'),
                  recipients=[user.email])
    reset_url = url_for('reset_token', token=token, _external=True)
    msg.body = render_template('email_reset_password.txt', 
                                 user=user, reset_url=reset_url)
    msg.html = render_template('email_reset_password.html.j2', 
                                 user=user, reset_url=reset_url)
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','success')
        return redirect(url_for('login'))
    return render_template('reset_request.html.j2', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been update! you are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html.j2', title='Reset Password', form=form)



@app.route("/appointment/new")
@login_required
@role_required('user')
def new_appointment():
    return render_template('create_appointment.html.j2', title='New Appointment')

@app.route("/message/new")
@role_required('user', 'therapist')
@login_required
def new_message():
    return render_template('create_message.html.j2', title='New Message')


@app.route("/query/new")
@login_required
@role_required('user', 'therapist', 'admin')
def new_query():
    return render_template('create_query.html.j2', title='New Query')
