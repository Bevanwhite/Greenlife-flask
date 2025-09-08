import jwt
from greenlife import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    services = db.relationship('Service', backref='user_service',lazy=True)
    client_appointments = db.relationship('Appointment', foreign_keys='Appointment.client_id', backref='appointment_client', lazy=True)
    therapist_appointments = db.relationship('Appointment', foreign_keys='Appointment.therapist_id', backref='appointment_therapist', lazy=True)
    sender = db.relationship('Conversation', foreign_keys='Conversation.user_id', backref='sender', lazy=True)
    queries = db.relationship('Query', backref='user_query', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}')"
    
    def get_reset_token(self, expires_sec=1800):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_sec)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            return None
        return User.query.get(user_id)
    
class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)

    receiver = db.relationship('Conversation', foreign_keys='Conversation.therapist_id', backref='receiver', lazy=True)
    therapist = db.relationship('User', backref='therapist', lazy=True)

    def __repr__(self):
        return f"Therapist('{self.user_id}','{self.specialization}', '{self.bio}')"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    user = db.relationship("User", backref="admin", lazy=True)

    def __repr__(self):
        return f"Admin('{self.id}','{self.user_id}')"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'), nullable=False)
    duration_options_id = db.Column(db.Integer, db.ForeignKey('duration_options.id'), nullable=False)

    def __repr__(self):
        return f"Service('{self.name}','{self.description}', '{self.price}', '{self.user_service}')"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)

    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    def __repr__(self):
        return f"Appointment('{self.id}','{self.appointment_time}', '{self.date_posted}')"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.now())
    method = db.Column(db.String(20))  # cash, card, online
    status = db.Column(db.String(20), default="paid")

    appointment = db.relationship("Appointment", backref="payment", lazy=True)

    def __repr__(self):
        return f"Payment('{self.id}','{self.appointment_id}', '{self.amount}')"


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=db.func.now())
    last_message_at = db.Column(db.DateTime)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)   # could be user.id OR therapist.id
    sender_role = db.Column(db.String(20), nullable=False)  # "user" or "therapist"
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)

    conversation = db.relationship("Conversation", backref="messages", lazy=True)

    def __repr__(self):
        return f"Message('{self.id}','{self.conversation_id}', '{self.content}')"
    
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), unique=True, nullable=False)
    subject = db.Column(db.String(120), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Query('{self.id}','{self.status}', '{self.subject}')"
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship("User", backref="reviews", lazy=True)
    service = db.relationship("Service", backref="reviews", lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"
    
class ServiceType(db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    services = db.relationship('Service', backref='service_type', lazy=True)

    def __repr__(self):
        return f"<ServiceType {self.name}>"
    
class DurationOptions(db.Model):
    __tablename__ = 'duration_options'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    minute = db.Column(db.Integer, unique=True, nullable=False)

    services = db.relationship('Service', backref='duration_option', lazy=True)

    def __repr__(self):
        return f"<DurationOptions {self.name}>"