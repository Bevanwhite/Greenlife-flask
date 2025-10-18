from greenlife import db, bcrypt
from greenlife.models import (Role, ServiceType, User, Service, Therapist, Admin,
                               DurationOptions,TherapistService, AppointmentStatus,
                               Appointment,)
from datetime import datetime

def seed_data():
    # Add roles
    roles = ["admin", "therapist", "user"]

    for role in roles:
        if not Role.query.filter_by(name=role).first():
            db.session.add(Role(name=role))

    appointmentstatus = [
        AppointmentStatus(
            name='Scheduled',
            color = '#FFC107'
        ),
        AppointmentStatus(
            name='Confirmed',
            color = '#28A745'
        ),
        AppointmentStatus(
            name='CheckedIn',
            color = '#0D6EFD'
        ),
        AppointmentStatus(
            name='InProgress',
            color = '#FD7E14'
        ),
        AppointmentStatus(
            name='Completed',
            color = '#198754'
        ),
        AppointmentStatus(
            name='Cancelled',
            color = '#DC3545'
        ),
        AppointmentStatus(
            name='NoShow',
            color = '#B02A37'
        ),
        AppointmentStatus(
            name='Rescheduled',
            color = '#6F42C1'
        ),
        AppointmentStatus(
            name='PendingPayment',
            color = '#FFC107'
        ),
        AppointmentStatus(
            name='Refunded',
            color = '#0DCAF0'
        ),
    ]

    for i in appointmentstatus:
        if not AppointmentStatus.query.filter_by(name=i.name).first():
            db.session.add(AppointmentStatus(
                    name=i.name,
                    color=i.color
                )
            )

    service_types = [
        "Ayurvedic Therapy",
        "Yoga & Meditation",
        "Nutrition & Diet",
        "Physiotherapy",
        "Massage Therapy",
    ]

    for service_type in service_types:
        if not ServiceType.query.filter_by(name=service_type).first():
            db.session.add(ServiceType(name=service_type))

    duration_options = [
        DurationOptions(minute=30, name="30 minutes"), #1
        DurationOptions(minute=40, name="40 minutes"), #2
        DurationOptions(minute=45, name="45 minutes"), #3
        DurationOptions(minute=50, name="50 minutes"), #4
        DurationOptions(minute=60, name="1 hour"), #5
        DurationOptions(minute=70, name="1 hour 10 minutes"), #6
        DurationOptions(minute=75, name="1 hour 15 minutes"), #7
        DurationOptions(minute=90, name="1 hour 30 minutes"), #8
        DurationOptions(minute=120, name="2 hours"), #9
        DurationOptions(minute=180, name="3 hours"), #10
        DurationOptions(minute=240, name="4 hours"), #11
    ]

    for duration in duration_options:
        if not DurationOptions.query.filter_by(name=duration.name).first():
            db.session.add(DurationOptions(minute=duration.minute, name=duration.name))
    
    users = [
        User(
            username='jeffery_white',
            full_name='Jeffery White',
            email='jeffery1996.jbw@gmail.com',
            phone='0773843002',
            role_id=Role.query.filter_by(name="user").first().id,
            password=bcrypt.generate_password_hash("1").decode('utf-8')
        ),
        User(
            username="dr_smith",
            full_name="Dr. Sarah Smith",
            email="sarah.smith@example.com",
            phone="0779876543",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("1").decode('utf-8')
        ),
        User(
            username="admin",
            full_name="System Admin",
            email="Jefferybevan@gmail.com",
            phone="0751112233",
            role_id=Role.query.filter_by(name="admin").first().id,
            password=bcrypt.generate_password_hash("1").decode('utf-8')
        ),
        User(
            username="therapist_ayurveda",
            full_name="Dr. Anjali Perera",
            email="anjali.perera@example.com",
            phone="0711111111",
            image_file="therapist_ayurveda.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_yoga",
            full_name="Mr. Ravi Senanayake",
            email="ravi.senanayake@example.com",
            phone="0722222222",
            image_file="therapist_yoga.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_nutrition",
            full_name="Dr. Malini Fernando",
            email="malini.fernando@example.com",
            phone="0733333333",
            image_file="therapist_nutrition.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_physiotherapy",
            full_name="Mr. Nimal Jayawardena",
            email="nimal.jayawardena@example.com",
            phone="0744444444",
            image_file="therapist_physiotherapy.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_massage",
            full_name="Ms. Kavindi Silva",
            email="kavindi.silva@example.com",
            phone="0755555555",
            image_file="therapist_massage.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_acupuncture",
            full_name="Dr. Chen Wei",
            email="chen.wei@example.com",
            phone="0766666666",
            image_file="therapist_acupuncture.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_psychology",
            full_name="Dr. Priya Sharma",
            email="priya.sharma@example.com",
            phone="0777777777",
            image_file="therapist_psychology.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_chiropractic",
            full_name="Dr. James Wilson",
            email="james.wilson@example.com",
            phone="0788888888",
            image_file="therapist_chiropractic.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_reflexology",
            full_name="Ms. Mei Lin",
            email="mei.lin@example.com",
            phone="0799999999",
            image_file="therapist_reflexology.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        ),
        User(
            username="therapist_aromatherapy",
            full_name="Ms. Sophia Williams",
            email="sophia.williams@example.com",
            phone="0700000000",
            image_file="therapist_aromatherapy.jpg",
            role_id=Role.query.filter_by(name="therapist").first().id,
            password=bcrypt.generate_password_hash("2").decode('utf-8')
        )
    ]

    for user in users:
        if not User.query.filter_by(username=user.username,email=user.email).first():
            db.session.add(
                User(
                    username=user.username,
                    full_name=user.full_name,
                    email=user.email,
                    phone=user.phone,
                    password=user.password, 
                    role_id=user.role_id
                )
            )
                
    therapists = [
            Therapist(
                user_id=2,  # assuming auto-increment id = 2
                specialization="Ayurvedic Therapy",
                bio="Experienced therapist specializing in Ayurveda and holistic healing.",
                available=True
            ),
            Therapist(
                user_id=4,  # assuming auto-increment id = 2
                specialization="Ayurvedic Therapy",
                bio="Expert in traditional Ayurvedic healing.",
                available=True
            ),
            Therapist(
                user_id=5,  # assuming auto-increment id = 2
                specialization="Yoga & Meditation",
                bio="Certified yoga and meditation trainer.",
                available=True
            ),
            Therapist(
                user_id=6,  # assuming auto-increment id = 2
                specialization="Nutrition & Diet",
                bio="Nutritionist with 10 years of experience.",
                available=True
            ),
            Therapist(
                user_id=7,  # assuming auto-increment id = 2
                specialization="Physiotherapy",
                bio="Physiotherapist specialized in sports recovery.",
                available=True
            ),
            Therapist(
                user_id=8,  # assuming auto-increment id = 2
                specialization="Massage Therapy",
                bio="Professional massage therapist.",
                available=True
            )
    ]

    for therapist in therapists:
        if not Therapist.query.filter_by(user_id=therapist.user_id).first():
            db.session.add(
                Therapist(
                    user_id=therapist.user_id,  # assuming auto-increment id = 2
                    specialization=therapist.specialization,
                    bio=therapist.bio,
                    available=therapist.available
                )
            )

    admins = [
        Admin(
            user_id=3  # assuming auto-increment id = 3
        )
    ]

    for admin in admins:
        if not Therapist.query.filter_by(user_id=admin.user_id).first():
            db.session.add(
                Admin(user_id=admin.user_id)
            )

    services = [
        Service(
            name="Herbal Detox", 
            description="Full-body detox using traditional Ayurvedic herbs.",
            user_id=4, 
            service_type_id=1,
            service_image = 'Herbal Detox.jpg',
            active=True
        ),
        Service(
            name="Shirodhara", 
            description="Warm oil treatment poured over the forehead.",
            user_id=4, 
            service_type_id=1,
            service_image = 'Shirodhara.jpg',
            active=True
        ),
        Service(
            name="Panchakarma", 
            description="Deep cleansing and rejuvenation therapy.",
            user_id=4, 
            service_type_id=1,
            service_image = 'Panchakarma.jpg',
            active=True
        ),
        Service(
            name="Abhyanga Massage", 
            description="Oil-based massage for body balance.",
            user_id=4, 
            service_type_id=1,
            service_image = 'Abhyanga Massage.jpg',
            active=True
        ),
        Service(
            name="Nasya", 
            description="Nasal therapy with medicated oils.",
            user_id=4, 
            service_type_id=1,
            service_image = 'Nasya.jpg',
            active=True
        ),
        Service(
            name="Morning Yoga Flow", 
            description="Energizing yoga practice to start your day.",
            user_id=5, 
            service_type_id=2,
            service_image = 'Morning Yoga Flow.jpg',
            active=True
        ),
        Service(
            name="Pranayama Breathing", 
            description="Breathing exercises for calmness.",
            user_id=5, 
            service_type_id=2,
            service_image = 'Pranayama Breathing.jpg',
            active=True
        ),
        Service(
            name="Mindfulness Meditation", 
            description="Guided meditation for focus.",
            user_id=5, 
            service_type_id=2,
            service_image = 'Mindfulness Meditation.jpg',
            active=True
        ),
        Service(
            name="Yoga Nidra", 
            description="Deep relaxation yoga practice.",
            user_id=5, 
            service_type_id=2,
            service_image='Yoga Nidra.jpg',
            active=True
        ),
        Service(
            name="Hatha Yoga", 
            description="Traditional yoga for strength and flexibility.",
            user_id=5, 
            service_type_id=2,
            service_image = 'Hatha Yoga.jpg',
            active=True
        ),

        # Nutrition & Diet (therapists[2])
        Service(
            name="Diet Consultation", 
            description="Personalized diet plan consultation.",
            user_id=6, 
            service_type_id=3,
            service_image = 'Diet Consultation.jpg',
            active=True
        ),
        Service(
            name="Weight Management Program", 
            description="Nutrition plan for weight goals.",
            user_id=6, 
            service_type_id=3,
            service_image = 'Weight Management Program.jpg',
            active=True
        ),
        Service(
            name="Detox Meal Plan", 
            description="7-day detox diet plan.",
            user_id=6, 
            service_type_id=3,
            service_image = 'Detox Meal Plan.jpg',
            active=True
        ),
        Service(
            name="Diabetic Diet Counseling", 
            description="Diet guidance for managing diabetes.",
            user_id=6, 
            service_type_id=3,
            service_image = 'Diabetic Diet Counseling.jpg',
            active=True
        ),
        Service(
            name="Sports Nutrition", 
            description="Nutrition plans for athletes.",
            user_id=6, 
            service_type_id=3,
            service_image = 'Sports Nutrition.jpg',
            active=True
        ),

        # Physiotherapy (therapists[3])
        Service(
            name="Back Pain Relief", 
            description="Targeted therapy for lower back pain.",
            user_id=7, 
            service_type_id=4,
            active=True
        ),
        Service(
            name="Post-Surgery Rehab", 
            description="Recovery program for post-surgery.",
            user_id=7, 
            service_type_id=4,
            active=True
        ),
        Service(
            name="Sports Injury Therapy", 
            description="Rehab for sports injuries.",
            user_id=7, 
            service_type_id=4,
            active=True
        ),
        Service(
            name="Joint Mobilization", 
            description="Improve mobility and reduce stiffness.",
            user_id=7, 
            service_type_id=4,
            active=True
        ),
        Service(
            name="Neck & Shoulder Therapy", 
            description="Pain relief for neck and shoulder.",
            user_id=7, 
            service_type_id=4,
            active=True
        ),

        # Massage Therapy (therapists[4])
        Service(
            name="Swedish Massage", 
            description="Gentle, relaxing full-body massage.",
            user_id=8, 
            service_type_id=5,
            active=True
        ),
        Service(
            name="Deep Tissue Massage", 
            description="Massage focusing on deep tissues.",
            user_id=8, 
            service_type_id=5,
            active=True
        ),
        Service(
            name="Hot Stone Massage", 
            description="Warm stone therapy for stress relief.",
            user_id=8, 
            service_type_id=5,
            active=True
        ),
        Service(
            name="Aromatherapy Massage", 
            description="Essential oil massage for relaxation.",
            user_id=8, 
            service_type_id=5,
            active=True
        ),
        Service(
            name="Reflexology", 
            description="Pressure point therapy on feet and hands.",
            user_id=8, 
            service_type_id=5,
            active=True
        ),
    ]


    for service in services:
        if not Service.query.filter_by(name=service.name).first():
            db.session.add(
                Service(
                    name=service.name,
                    description=service.description,
                    user_id=service.user_id,
                    service_type_id=service.service_type_id,
                    service_image = service.service_image,
                    active= service.active
                )
            )

    therapist_services = [
        TherapistService(
            therapist_id = 1,
            service_id = 1,
            price = 4000.00,
            duration_options_id = 9,
            active =True
        ),
        TherapistService(
            therapist_id = 3,
            service_id = 1,
            price = 3000.00,
            duration_options_id = 8,
            active =True
        ),
        TherapistService(
            therapist_id = 2,
            service_id = 2,
            price = 3000.00,
            duration_options_id = 8,
            active =True
        ),
        TherapistService(
            therapist_id = 3,
            service_id = 2,
            price = 6000.00,
            duration_options_id = 3,
            active =True
        ),
        TherapistService(
            therapist_id = 4,
            service_id = 3,
            price = 6000.00,
            duration_options_id = 6,
            active =True
        ),
        TherapistService(
            therapist_id = 4,
            service_id = 3,
            price = 6000.00,
            duration_options_id = 6,
            active =True
        )
    ]
    for t in therapist_services:
        if not TherapistService.query.filter_by(therapist_id=t.therapist_id,
                                       service_id = t.service_id).first():
            db.session.add(
                TherapistService(
                    therapist_id=t.therapist_id,
                    service_id=t.service_id,
                    price=t.price,
                    duration_options_id=t.duration_options_id,
                    active=t.active
                )
            )
    
    appointments = [
        Appointment(
            appointment_time = '2025-10-18 12:00:00',
            status_id = 1,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-19 12:00:00',
            status_id = 2,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-20 12:00:00',
            status_id = 3,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-21 12:00:00',
            status_id = 4,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-22 12:00:00',
            status_id = 5,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-23 12:00:00',
            status_id = 6,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-24 12:00:00',
            status_id = 7,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-24 12:00:00',
            status_id = 8,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-24 12:00:00',
            status_id = 9,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        ),
        Appointment(
            appointment_time = '2025-10-24 12:00:00',
            status_id = 10,
            notes = '',
            client_id = 1,
            therapist_id = 3,
            therapist_service_id = 1
        )
    ]

    for t in appointments:

        if isinstance(t.appointment_time, str):
            t.appointment_time = datetime.strptime(t.appointment_time, "%Y-%m-%d %H:%M:%S")

        if not Appointment.query.filter_by(appointment_time=t.appointment_time,
                                       client_id = t.client_id,
                                       therapist_id=t.therapist_id,
                                       therapist_service_id = t.therapist_service_id).first():
            db.session.add(
                Appointment(
                    appointment_time = t.appointment_time,
                    status_id = t.status_id,
                    notes = t.notes,
                    client_id = t.client_id,
                    therapist_id = t.therapist_id,
                    therapist_service_id = t.therapist_service_id
                )
            )

    db.session.commit()
    print("✅ Roles & Service Types seeded successfully!")