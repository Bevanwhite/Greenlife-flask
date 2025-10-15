import jwt
from greenlife import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask import current_app
from sqlalchemy.orm import foreign

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===========================================================
# ROLE
# ===========================================================
class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', back_populates='role', lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"


# ===========================================================
# ADMIN
# ===========================================================
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    user = db.relationship("User", back_populates="admin_profile", lazy=True)

    def __repr__(self):
        return f"Admin('{self.id}', '{self.user_id}')"


# ===========================================================
# THERAPIST
# ===========================================================
class Therapist(db.Model):
    __tablename__ = "therapist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)

    user = db.relationship('User', back_populates='therapist_profile')
    therapist_services = db.relationship('TherapistService', back_populates='therapist', lazy=True)
    therapist_appointments = db.relationship('Appointment', back_populates='appointment_therapist', lazy=True)
    received_conversations = db.relationship('Conversation', back_populates='therapist', lazy=True)


# ===========================================================
# SERVICE
# ===========================================================
class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'), nullable=False)

    user = db.relationship('User', back_populates='services')
    service_type = db.relationship('ServiceType', back_populates='services')
    therapist_services = db.relationship('TherapistService', back_populates='service', lazy=True)


# ===========================================================
# THERAPISTSERVICE
# ===========================================================
class TherapistService(db.Model):
    __tablename__ = "therapist_service"

    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    duration_options_id = db.Column(db.Integer, db.ForeignKey('duration_options.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    therapist = db.relationship('Therapist', back_populates='therapist_services')
    service = db.relationship('Service', back_populates='therapist_services')
    duration_option = db.relationship('DurationOptions', back_populates='therapist_service')
    appointments = db.relationship('Appointment', back_populates='therapist_service', lazy=True)


# ===========================================================
# APPOINTMENT
# ===========================================================
class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(20))
    notes = db.Column(db.Text)

    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    therapist_service_id = db.Column(db.Integer, db.ForeignKey('therapist_service.id'), nullable=False)
    review_Id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)

    appointment_client = db.relationship('User', back_populates='client_appointments', lazy=True)
    appointment_therapist = db.relationship('Therapist', back_populates='therapist_appointments', lazy=True)
    therapist_service = db.relationship('TherapistService', back_populates='appointments', lazy=True)
    review = db.relationship('Review', back_populates='appointment', lazy=True)
    payment = db.relationship('Payment', back_populates='appointment', uselist=False)

# ===========================================================
# PAYMENT
# ===========================================================
class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, server_default=db.func.now())
    method = db.Column(db.String(20))
    status = db.Column(db.String(20), default="paid")

    appointment = db.relationship("Appointment", back_populates="payment", lazy=True)

    def __repr__(self):
        return f"Payment('{self.id}', '{self.appointment_id}', '{self.amount}')"


# ===========================================================
# CONVERSATION
# ===========================================================
class Conversation(db.Model):
    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    started_at = db.Column(db.DateTime, server_default=db.func.now())
    last_message_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='sent_conversations', lazy=True)
    therapist = db.relationship('Therapist', back_populates='received_conversations', lazy=True)
    messages = db.relationship('Message', back_populates='conversation', lazy=True)


# ===========================================================
# MESSAGE
# ===========================================================
class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)  # "user" or "therapist"
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, server_default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)

    conversation = db.relationship("Conversation", back_populates="messages", lazy=True)

    def __repr__(self):
        return f"Message('{self.id}', '{self.conversation_id}', '{self.content}')"


# ===========================================================
# QUERY
# ===========================================================
class Query(db.Model):
    __tablename__ = "query"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user_query = db.relationship('User', back_populates='queries', lazy=True)

    def __repr__(self):
        return f"Query('{self.id}', '{self.status}', '{self.subject}')"


# ===========================================================
# REVIEW
# ===========================================================
class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", back_populates="reviews", lazy=True)
    appointment = db.relationship("Appointment", back_populates="review", lazy=True)


# ===========================================================
# SERVICE TYPE
# ===========================================================
class ServiceType(db.Model):
    __tablename__ = "service_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    services = db.relationship('Service', back_populates='service_type', lazy=True)

    def __repr__(self):
        return f"<ServiceType {self.name}>"


# ===========================================================
# DURATION OPTIONS
# ===========================================================
class DurationOptions(db.Model):
    __tablename__ = "duration_options"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    minute = db.Column(db.Integer, unique=True, nullable=False)

    therapist_service = db.relationship('TherapistService', back_populates='duration_option', lazy=True)

    def __repr__(self):
        return f"<DurationOptions {self.name}>"
    

# ===========================================================
# USER
# ===========================================================
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Relationships
    services = db.relationship('Service', back_populates='user', lazy=True)
    client_appointments = db.relationship('Appointment', foreign_keys='Appointment.client_id', back_populates='appointment_client', lazy=True)
    sent_conversations = db.relationship('Conversation', back_populates='user', lazy=True)
    queries = db.relationship('Query', back_populates='user_query', lazy=True)
    therapist_profile = db.relationship('Therapist', back_populates='user', uselist=False, lazy=True)
    admin_profile = db.relationship('Admin', back_populates='user', uselist=False, lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)
    role = db.relationship('Role', back_populates='users')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

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
            return None
        except jwt.InvalidTokenError:
            return None
        return User.query.get(user_id)

