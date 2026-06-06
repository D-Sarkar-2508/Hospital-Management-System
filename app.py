from flask import Flask, render_template, request, jsonify, session  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
from datetime import datetime, date
import json
import os

app = Flask(__name__)
app.secret_key = 'ds_hospital_secret_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ds_hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
#  MODELS
# ─────────────────────────────────────────────

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(10), unique=True, nullable=False)
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    blood_group = db.Column(db.String(10))
    age = db.Column(db.Integer)
    health_issues = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200))
    department = db.Column(db.String(100))
    fees = db.Column(db.Float, default=500)
    chamber = db.Column(db.String(100))
    blood_group = db.Column(db.String(10))
    age = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

class Pharmacist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    blood_group = db.Column(db.String(10))
    age = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

class Receptionist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    blood_group = db.Column(db.String(10))
    age = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class TestBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    test_name = db.Column(db.String(100))
    test_price = db.Column(db.Float)
    booking_date = db.Column(db.String(20))
    booking_time = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Booked')
    report_date = db.Column(db.String(20))
    patient = db.relationship('Patient', backref='test_bookings')

class OTBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    ot_name = db.Column(db.String(100))
    doctor_name = db.Column(db.String(100))
    ot_cost = db.Column(db.Float)
    status = db.Column(db.String(20), default='Pending')
    confirmed_date = db.Column(db.String(20))
    patient = db.relationship('Patient', backref='ot_bookings')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    preferred_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Pending')
    confirmed_date = db.Column(db.String(20))
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

# ─────────────────────────────────────────────
#  SEED DATA
# ─────────────────────────────────────────────

TESTS = [
    {"name": "Complete Blood Count (CBC)", "price": 350},
    {"name": "Blood Sugar Fasting", "price": 120},
    {"name": "Lipid Profile", "price": 600},
    {"name": "Liver Function Test (LFT)", "price": 750},
    {"name": "Kidney Function Test (KFT)", "price": 800},
    {"name": "Thyroid Profile (T3/T4/TSH)", "price": 900},
    {"name": "Urine Routine Examination", "price": 150},
    {"name": "ECG", "price": 250},
    {"name": "Chest X-Ray", "price": 400},
    {"name": "MRI Brain", "price": 5500},
    {"name": "CT Scan Abdomen", "price": 4500},
    {"name": "Ultrasound Abdomen", "price": 1200},
    {"name": "HbA1c", "price": 450},
    {"name": "Vitamin D3", "price": 1100},
    {"name": "Vitamin B12", "price": 950},
    {"name": "COVID-19 RT-PCR", "price": 700},
    {"name": "Dengue NS1 Antigen", "price": 500},
    {"name": "Malaria Antigen Test", "price": 350},
    {"name": "Stool Routine Examination", "price": 180},
    {"name": "Serum Calcium", "price": 280},
]

OT_LIST = [
    {"name": "General Surgery OT", "cost": 25000},
    {"name": "Cardiac Surgery OT", "cost": 150000},
    {"name": "Neurosurgery OT", "cost": 180000},
    {"name": "Orthopaedic OT", "cost": 80000},
    {"name": "Laparoscopic OT", "cost": 45000},
    {"name": "Eye Surgery OT", "cost": 35000},
    {"name": "ENT Surgery OT", "cost": 30000},
    {"name": "Gynaecology OT", "cost": 40000},
    {"name": "Oncology Surgery OT", "cost": 120000},
    {"name": "Paediatric OT", "cost": 55000},
]

DEFAULT_DOCTORS = [
    {"name": "Dr. Arjun Sharma", "department": "General Medicine", "degree": "MBBS, MD (General Medicine)", "fees": 600, "chamber": "Room 101", "contact": "9800000001", "email": "arjun.sharma@dshospital.com", "address": "12 Park Street, Kolkata"},
    {"name": "Dr. Priya Mehta", "department": "General Medicine", "degree": "MBBS, DNB (Internal Medicine)", "fees": 550, "chamber": "Room 102", "contact": "9800000002", "email": "priya.mehta@dshospital.com", "address": "34 Lake Road, Kolkata"},
    {"name": "Dr. Rajesh Gupta", "department": "Cardiology", "degree": "MBBS, MD, DM (Cardiology)", "fees": 1200, "chamber": "Room 201", "contact": "9800000003", "email": "rajesh.gupta@dshospital.com", "address": "56 Bypass Road, Kolkata"},
    {"name": "Dr. Sunita Verma", "department": "Cardiology", "degree": "MBBS, MD, FACC", "fees": 1500, "chamber": "Room 202", "contact": "9800000004", "email": "sunita.verma@dshospital.com", "address": "78 Queens Road, Kolkata"},
    {"name": "Dr. Anil Bose", "department": "Neurology", "degree": "MBBS, MD, DM (Neurology)", "fees": 1400, "chamber": "Room 301", "contact": "9800000005", "email": "anil.bose@dshospital.com", "address": "90 College Street, Kolkata"},
    {"name": "Dr. Kavita Singh", "department": "Neurology", "degree": "MBBS, MD, DNB (Neurology)", "fees": 1300, "chamber": "Room 302", "contact": "9800000006", "email": "kavita.singh@dshospital.com", "address": "21 Central Ave, Kolkata"},
    {"name": "Dr. Raman Nair", "department": "Oncology", "degree": "MBBS, MD, DM (Oncology)", "fees": 2000, "chamber": "Room 401", "contact": "9800000007", "email": "raman.nair@dshospital.com", "address": "43 South End, Kolkata"},
    {"name": "Dr. Ananya Das", "department": "Oncology", "degree": "MBBS, MD, MRCP (UK)", "fees": 2200, "chamber": "Room 402", "contact": "9800000008", "email": "ananya.das@dshospital.com", "address": "65 North Road, Kolkata"},
    {"name": "Dr. Saurabh Joshi", "department": "Pediatrics", "degree": "MBBS, MD (Paediatrics), DCH", "fees": 700, "chamber": "Room 501", "contact": "9800000009", "email": "saurabh.joshi@dshospital.com", "address": "87 West Avenue, Kolkata"},
    {"name": "Dr. Meena Iyer", "department": "Pediatrics", "degree": "MBBS, DNB (Paediatrics)", "fees": 650, "chamber": "Room 502", "contact": "9800000010", "email": "meena.iyer@dshospital.com", "address": "9 East Lane, Kolkata"},
    {"name": "Dr. Pooja Rao", "department": "Gynecology", "degree": "MBBS, MS (Obs & Gynae), DGO", "fees": 900, "chamber": "Room 601", "contact": "9800000011", "email": "pooja.rao@dshospital.com", "address": "11 Garden Street, Kolkata"},
    {"name": "Dr. Nandita Banerjee", "department": "Gynecology", "degree": "MBBS, MD (Gynae)", "fees": 850, "chamber": "Room 602", "contact": "9800000012", "email": "nandita.banerjee@dshospital.com", "address": "33 Hill Road, Kolkata"},
    {"name": "Dr. Vikram Patel", "department": "Orthopedics", "degree": "MBBS, MS (Ortho), DNB", "fees": 1000, "chamber": "Room 701", "contact": "9800000013", "email": "vikram.patel@dshospital.com", "address": "55 Station Road, Kolkata"},
    {"name": "Dr. Deepak Choudhury", "department": "Orthopedics", "degree": "MBBS, MS, FRCS (UK)", "fees": 1100, "chamber": "Room 702", "contact": "9800000014", "email": "deepak.choudhury@dshospital.com", "address": "77 Market Lane, Kolkata"},
    {"name": "Dr. Suresh Pillai", "department": "Emergency", "degree": "MBBS, MD (Emergency Medicine)", "fees": 500, "chamber": "Emergency Wing", "contact": "9800000015", "email": "suresh.pillai@dshospital.com", "address": "99 Hospital Road, Kolkata"},
    {"name": "Dr. Reena Kapoor", "department": "Emergency", "degree": "MBBS, ATLS Certified", "fees": 500, "chamber": "Emergency Wing", "contact": "9800000016", "email": "reena.kapoor@dshospital.com", "address": "22 City Road, Kolkata"},
]

def seed_doctors():
    for d in DEFAULT_DOCTORS:
        if not Doctor.query.filter_by(email=d['email']).first():
            doc = Doctor(
                name=d['name'], department=d['department'], degree=d['degree'],
                fees=d['fees'], chamber=d['chamber'], contact=d['contact'],
                email=d['email'], address=d['address'],
                password=generate_password_hash('Doctor@123')
            )
            db.session.add(doc)
    db.session.commit()

# ─────────────────────────────────────────────
#  ROUTES – PAGES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patient_portal')
def patient_portal():
    if 'patient_id' not in session:
        return render_template('index.html')
    patient = Patient.query.get(session['patient_id'])
    return render_template('patient_portal.html', patient=patient,
                           tests=TESTS, ot_list=OT_LIST)

@app.route('/doctor_portal')
def doctor_portal():
    if 'doctor_id' not in session:
        return render_template('index.html')
    doctor = Doctor.query.get(session['doctor_id'])
    return render_template('doctor_portal.html', doctor=doctor)

@app.route('/pharmacist_portal')
def pharmacist_portal():
    if 'pharmacist_id' not in session:
        return render_template('index.html')
    pharmacist = Pharmacist.query.get(session['pharmacist_id'])
    today = date.today().strftime('%Y-%m-%d')
    bookings = TestBooking.query.filter_by(booking_date=today).all()
    return render_template('pharmacist_portal.html', pharmacist=pharmacist,
                           bookings=bookings)

@app.route('/receptionist_portal')
def receptionist_portal():
    if 'receptionist_id' not in session:
        return render_template('index.html')
    receptionist = Receptionist.query.get(session['receptionist_id'])
    ot_requests = OTBooking.query.filter_by(status='Pending').all()
    appt_requests = Appointment.query.filter_by(status='Pending').all()
    return render_template('receptionist_portal.html',
                           receptionist=receptionist,
                           ot_requests=ot_requests,
                           appt_requests=appt_requests)

@app.route('/admin_portal')
def admin_portal():
    if 'admin_id' not in session:
        return render_template('index.html')
    admin = Admin.query.get(session['admin_id'])
    return render_template('admin_portal.html', admin=admin)

# ─────────────────────────────────────────────
#  API – AUTH
# ─────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    role = data.get('role')
    try:
        hashed = generate_password_hash(data['password'])
        if role == 'patient':
            if Patient.query.filter((Patient.email == data['email']) | (Patient.contact == data['contact'])).first():
                return jsonify({'success': False, 'message': 'Email or contact already registered!'})
            obj = Patient(name=data['name'], address=data.get('address',''),
                          contact=data['contact'], dob=data.get('dob',''),
                          email=data['email'], password=hashed)
        elif role == 'doctor':
            if Doctor.query.filter((Doctor.email == data['email']) | (Doctor.contact == data['contact'])).first():
                return jsonify({'success': False, 'message': 'Email or contact already registered!'})
            obj = Doctor(name=data['name'], address=data.get('address',''),
                         contact=data['contact'], email=data['email'], password=hashed)
        elif role == 'pharmacist':
            if Pharmacist.query.filter((Pharmacist.email == data['email']) | (Pharmacist.contact == data['contact'])).first():
                return jsonify({'success': False, 'message': 'Email or contact already registered!'})
            obj = Pharmacist(name=data['name'], address=data.get('address',''),
                             contact=data['contact'], email=data['email'], password=hashed)
        elif role == 'receptionist':
            if Receptionist.query.filter((Receptionist.email == data['email']) | (Receptionist.contact == data['contact'])).first():
                return jsonify({'success': False, 'message': 'Email or contact already registered!'})
            obj = Receptionist(name=data['name'], address=data.get('address',''),
                               contact=data['contact'], email=data['email'], password=hashed)
        elif role == 'admin':
            if Admin.query.filter((Admin.email == data['email']) | (Admin.contact == data['contact'])).first():
                return jsonify({'success': False, 'message': 'Email or contact already registered!'})
            obj = Admin(name=data['name'], address=data.get('address',''),
                        contact=data['contact'], email=data['email'], password=hashed)
        else:
            return jsonify({'success': False, 'message': 'Invalid role'})
        db.session.add(obj)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Registered successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    role = data.get('role')
    identifier = data.get('identifier', '').strip()
    password = data.get('password', '')
    try:
        if role == 'patient':
            user = Patient.query.filter((Patient.email == identifier) | (Patient.contact == identifier)).filter_by(is_active=True).first()
            if user and check_password_hash(user.password, password):
                session['patient_id'] = user.id
                return jsonify({'success': True, 'redirect': '/patient_portal'})
        elif role == 'doctor':
            user = Doctor.query.filter((Doctor.email == identifier) | (Doctor.contact == identifier)).filter_by(is_active=True).first()
            if user and check_password_hash(user.password, password):
                session['doctor_id'] = user.id
                return jsonify({'success': True, 'redirect': '/doctor_portal'})
        elif role == 'pharmacist':
            user = Pharmacist.query.filter((Pharmacist.email == identifier) | (Pharmacist.contact == identifier)).filter_by(is_active=True).first()
            if user and check_password_hash(user.password, password):
                session['pharmacist_id'] = user.id
                return jsonify({'success': True, 'redirect': '/pharmacist_portal'})
        elif role == 'receptionist':
            user = Receptionist.query.filter((Receptionist.email == identifier) | (Receptionist.contact == identifier)).filter_by(is_active=True).first()
            if user and check_password_hash(user.password, password):
                session['receptionist_id'] = user.id
                return jsonify({'success': True, 'redirect': '/receptionist_portal'})
        elif role == 'admin':
            user = Admin.query.filter((Admin.email == identifier) | (Admin.contact == identifier)).first()
            if user and check_password_hash(user.password, password):
                session['admin_id'] = user.id
                return jsonify({'success': True, 'redirect': '/admin_portal'})
        return jsonify({'success': False, 'message': 'Invalid credentials!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({'success': True})

# ─────────────────────────────────────────────
#  API – PATIENT
# ─────────────────────────────────────────────

@app.route('/api/doctors/<department>')
def get_doctors_by_dept(department):
    doctors = Doctor.query.filter_by(department=department, is_active=True).all()
    return jsonify([{'id': d.id, 'name': d.name, 'degree': d.degree,
                     'fees': d.fees, 'chamber': d.chamber} for d in doctors])

@app.route('/api/book_test', methods=['POST'])
def book_test():
    if 'patient_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    data = request.json
    booking = TestBooking(
        patient_id=session['patient_id'],
        test_name=data['test_name'],
        test_price=data['test_price'],
        booking_date=data['booking_date'],
        booking_time=data['booking_time']
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Test booked successfully!'})

@app.route('/api/my_tests')
def my_tests():
    if 'patient_id' not in session:
        return jsonify([])
    bookings = TestBooking.query.filter_by(patient_id=session['patient_id']).all()
    return jsonify([{'id': b.id, 'test_name': b.test_name, 'test_price': b.test_price,
                     'booking_date': b.booking_date, 'booking_time': b.booking_time,
                     'status': b.status, 'report_date': b.report_date} for b in bookings])

@app.route('/api/book_ot', methods=['POST'])
def book_ot():
    if 'patient_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    data = request.json
    booking = OTBooking(
        patient_id=session['patient_id'],
        ot_name=data['ot_name'],
        doctor_name=data['doctor_name'],
        ot_cost=data['ot_cost']
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'success': True, 'message': 'OT booking request submitted!'})

@app.route('/api/my_ot_bookings')
def my_ot_bookings():
    if 'patient_id' not in session:
        return jsonify([])
    bookings = OTBooking.query.filter_by(patient_id=session['patient_id']).all()
    return jsonify([{'id': b.id, 'ot_name': b.ot_name, 'doctor_name': b.doctor_name,
                     'ot_cost': b.ot_cost, 'status': b.status,
                     'confirmed_date': b.confirmed_date} for b in bookings])

@app.route('/api/update_health_issues', methods=['POST'])
def update_health_issues():
    if 'patient_id' not in session:
        return jsonify({'success': False})
    data = request.json
    patient = Patient.query.get(session['patient_id'])
    patient.health_issues = data.get('health_issues', '')
    db.session.commit()
    return jsonify({'success': True, 'message': 'Health issues updated!'})

@app.route('/api/book_appointment', methods=['POST'])
def book_appointment():
    if 'patient_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    data = request.json
    appt = Appointment(
        patient_id=session['patient_id'],
        doctor_id=data['doctor_id'],
        preferred_date=data['preferred_date']
    )
    db.session.add(appt)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Appointment request submitted!'})

@app.route('/api/my_appointments')
def my_appointments():
    if 'patient_id' not in session:
        return jsonify([])
    
    # Fetch all appointments belonging to the logged-in patient
    appts = Appointment.query.filter_by(patient_id=session['patient_id']).all()
    
    # Format and return JSON data expected by patient_portal.html
    return jsonify([{
        'id': a.id,
        'doctor_name': a.doctor.name if a.doctor else 'Unknown Doctor',
        # Handles internal database spelling variations cleanly for uniform lookups
        'doctor_department': "Gynaecology & Obstetrics" if a.doctor and a.doctor.department == "Gynecology" else (a.doctor.department if a.doctor else 'N/A'),
        'preferred_date': a.preferred_date,
        'status': a.status,
        'confirmed_date': a.confirmed_date
    } for a in appts])
    
@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    role = data.get('role')
    try:
        if role == 'patient' and 'patient_id' in session:
            obj = Patient.query.get(session['patient_id'])
        elif role == 'doctor' and 'doctor_id' in session:
            obj = Doctor.query.get(session['doctor_id'])
        elif role == 'pharmacist' and 'pharmacist_id' in session:
            obj = Pharmacist.query.get(session['pharmacist_id'])
        elif role == 'receptionist' and 'receptionist_id' in session:
            obj = Receptionist.query.get(session['receptionist_id'])
        else:
            return jsonify({'success': False, 'message': 'Unauthorized'})
        for field in ['name', 'address', 'blood_group', 'age']:
            if field in data:
                setattr(obj, field, data[field])
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# ─────────────────────────────────────────────
#  API – DOCTOR
# ─────────────────────────────────────────────

@app.route('/api/update_degree', methods=['POST'])
def update_degree():
    if 'doctor_id' not in session:
        return jsonify({'success': False})
    data = request.json
    doctor = Doctor.query.get(session['doctor_id'])
    doctor.degree = data.get('degree', '')
    db.session.commit()
    return jsonify({'success': True, 'message': 'Degree updated!'})

@app.route('/api/update_department', methods=['POST'])
def update_department():
    if 'doctor_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized access"})
    
    data = request.get_json()
    dept = data.get('department')
    
    # Simple fix for spelling variance: map 'Gynaecology' layout selection to match 'Gynecology' seed data
    if dept == "Gynaecology":
        dept = "Gynecology"
        
    doctor = Doctor.query.get(session['doctor_id'])
    if doctor:
        doctor.department = dept
        db.session.commit()
        return jsonify({"success": True, "message": "Department updated successfully!"})
    
    return jsonify({"success": False, "message": "Doctor record not found"})

@app.route('/api/update_chamber', methods=['POST'])
def update_chamber():
    if 'doctor_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized access"})
        
    data = request.get_json()
    chamber = data.get('chamber')
    
    doctor = Doctor.query.get(session['doctor_id'])
    if doctor:
        doctor.chamber = chamber
        db.session.commit()
        return jsonify({"success": True, "message": "Chamber configuration updated!"})
        
    return jsonify({"success": False, "message": "Doctor record not found"})

@app.route('/api/update_fees', methods=['POST'])
def update_fees():
    if 'doctor_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized access"})
    data = request.get_json()
    fees = data.get('fees')
    if not fees or float(fees) <= 0:
        return jsonify({"success": False, "message": "Please enter a valid fee amount."})
    doctor = Doctor.query.filter_by(id=session['doctor_id']).first()
    if doctor:
        doctor.fees = float(fees)
        db.session.commit()
        return jsonify({"success": True, "message": "Consultation fees updated!"})
    return jsonify({"success": False, "message": "Doctor record not found"})

@app.route('/api/my_patients')
def my_patients():
    if 'doctor_id' not in session:
        return jsonify([])
    confirmed = Appointment.query.filter_by(doctor_id=session['doctor_id'], status='Confirmed').all()
    result = []
    for a in confirmed:
        p = a.patient
        result.append({'name': p.name, 'age': p.age, 'health_issues': p.health_issues,
                       'confirmed_date': a.confirmed_date})
    return jsonify(result)

# ─────────────────────────────────────────────
#  API – PHARMACIST
# ─────────────────────────────────────────────

@app.route('/api/complete_test', methods=['POST'])
def complete_test():
    if 'pharmacist_id' not in session:
        return jsonify({'success': False})
    data = request.json
    booking = TestBooking.query.get(data['booking_id'])
    if booking:
        booking.status = 'Completed'
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/api/set_report_date', methods=['POST'])
def set_report_date():
    if 'pharmacist_id' not in session:
        return jsonify({'success': False})
    data = request.json
    booking = TestBooking.query.get(data['booking_id'])
    if booking:
        booking.report_date = data['report_date']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Report date set!'})
    return jsonify({'success': False})

@app.route('/api/all_test_bookings')
def all_test_bookings():
    if 'pharmacist_id' not in session:
        return jsonify([])
    bookings = TestBooking.query.all()
    result = []
    for b in bookings:
        result.append({
            'id': b.id,
            'patient_name': b.patient.name,
            'patient_contact': b.patient.contact,
            'test_name': b.test_name,
            'booking_date': b.booking_date,
            'booking_time': b.booking_time,
            'status': b.status,
            'report_date': b.report_date
        })
    return jsonify(result)

# ─────────────────────────────────────────────
#  API – RECEPTIONIST
# ─────────────────────────────────────────────

@app.route('/api/confirm_ot', methods=['POST'])
def confirm_ot():
    if 'receptionist_id' not in session:
        return jsonify({'success': False})
    data = request.json
    booking = OTBooking.query.get(data['ot_id'])
    if booking:
        booking.status = 'Confirmed'
        booking.confirmed_date = data['confirmed_date']
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

# ADD THIS NEW ROUTE HERE:
@app.route('/api/reject_ot', methods=['POST'])
def reject_ot():
    if 'receptionist_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized access'})
    
    data = request.json
    booking = OTBooking.query.get(data['ot_id'])
    if booking:
        booking.status = 'Rejected'
        booking.confirmed_date = None  # Resets any temporary date allocation values
        db.session.commit()
        return jsonify({'success': True, 'message': 'OT booking request rejected!'})
        
    return jsonify({'success': False, 'message': 'OT booking record not found'})

@app.route('/api/confirm_appointment', methods=['POST'])
def confirm_appointment():
    if 'receptionist_id' not in session:
        return jsonify({'success': False})
    data = request.json
    appt = Appointment.query.get(data['appt_id'])
    if appt:
        appt.status = 'Confirmed'
        appt.confirmed_date = data['confirmed_date']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Appointment confirmed!'})
    return jsonify({'success': False})

@app.route('/api/reject_appointment', methods=['POST'])
def reject_appointment():
    if 'receptionist_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized access'})
    
    data = request.json
    appt = Appointment.query.get(data['appt_id'])
    if appt:
        appt.status = 'Rejected'
        appt.confirmed_date = None # Clear out any previous date settings if applicable
        db.session.commit()
        return jsonify({'success': True, 'message': 'Appointment request rejected!'})
        
    return jsonify({'success': False, 'message': 'Appointment record not found'})

@app.route('/api/all_ot_requests')
def all_ot_requests():
    if 'receptionist_id' not in session:
        return jsonify([])
    bookings = OTBooking.query.all()
    return jsonify([{
        'id': b.id, 'patient_name': b.patient.name,
        'ot_name': b.ot_name, 'doctor_name': b.doctor_name,
        'ot_cost': b.ot_cost, 'status': b.status,
        'confirmed_date': b.confirmed_date
    } for b in bookings])

@app.route('/api/all_appointments')
def all_appointments():
    if 'receptionist_id' not in session:
        return jsonify([])
    appts = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'patient_name': a.patient.name,
        'doctor_name': a.doctor.name,
        'doctor_department': a.doctor.department,
        'preferred_date': a.preferred_date,
        'status': a.status,
        'confirmed_date': a.confirmed_date
    } for a in appts])

# ─────────────────────────────────────────────
#  API – ADMIN
# ─────────────────────────────────────────────

@app.route('/api/admin/all/<role>')
def admin_all(role):
    if 'admin_id' not in session:
        return jsonify([])
    if role == 'patients':
        objs = Patient.query.all()
        return jsonify([{'id': o.id, 'name': o.name, 'email': o.email,
                         'contact': o.contact, 'address': o.address,
                         'dob': o.dob, 'blood_group': o.blood_group,
                         'age': o.age, 'is_active': o.is_active} for o in objs])
    elif role == 'doctors':
        objs = Doctor.query.all()
        return jsonify([{'id': o.id, 'name': o.name, 'email': o.email,
                         'contact': o.contact, 'department': o.department,
                         'degree': o.degree, 'fees': o.fees,
                         'chamber': o.chamber, 'is_active': o.is_active} for o in objs])
    elif role == 'pharmacists':
        objs = Pharmacist.query.all()
        return jsonify([{'id': o.id, 'name': o.name, 'email': o.email,
                         'contact': o.contact, 'address': o.address,
                         'is_active': o.is_active} for o in objs])
    elif role == 'receptionists':
        objs = Receptionist.query.all()
        return jsonify([{'id': o.id, 'name': o.name, 'email': o.email,
                         'contact': o.contact, 'address': o.address,
                         'is_active': o.is_active} for o in objs])
    return jsonify([])

@app.route('/api/admin/remove', methods=['POST'])
def admin_remove():
    if 'admin_id' not in session:
        return jsonify({'success': False})
    data = request.json
    role, uid = data.get('role'), data.get('id')
    try:
        if role == 'patient':
            obj = Patient.query.filter_by(id=uid).first()
            if obj:
                TestBooking.query.filter_by(patient_id=uid).delete()
                OTBooking.query.filter_by(patient_id=uid).delete()
                Appointment.query.filter_by(patient_id=uid).delete()
                db.session.delete(obj)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Patient permanently deleted!'})
        elif role == 'doctor':
            obj = Doctor.query.filter_by(id=uid).first()
            if obj:
                Appointment.query.filter_by(doctor_id=uid).delete()
                db.session.delete(obj)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Doctor permanently deleted!'})
        elif role == 'pharmacist':
            obj = Pharmacist.query.filter_by(id=uid).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Pharmacist permanently deleted!'})
        elif role == 'receptionist':
            obj = Receptionist.query.filter_by(id=uid).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Receptionist permanently deleted!'})
        return jsonify({'success': False, 'message': 'Record not found'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/api/admin/add', methods=['POST'])
def admin_add():
    if 'admin_id' not in session:
        return jsonify({'success': False})
    data = request.json
    role = data.get('role')
    hashed = generate_password_hash(data['password'])
    try:
        if role == 'doctor':
            obj = Doctor(name=data['name'], address=data.get('address',''),
                         contact=data['contact'], email=data['email'],
                         password=hashed, department=data.get('department',''),
                         degree=data.get('degree',''), fees=float(data.get('fees',500)),
                         chamber=data.get('chamber',''))
        elif role == 'pharmacist':
            obj = Pharmacist(name=data['name'], address=data.get('address',''),
                             contact=data['contact'], email=data['email'], password=hashed)
        elif role == 'receptionist':
            obj = Receptionist(name=data['name'], address=data.get('address',''),
                               contact=data['contact'], email=data['email'], password=hashed)
        elif role == 'patient':
            obj = Patient(name=data['name'], address=data.get('address',''),
                          contact=data['contact'], email=data['email'],
                          password=hashed, dob=data.get('dob',''))
        else:
            return jsonify({'success': False, 'message': 'Invalid role'})
        db.session.add(obj)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{role.capitalize()} added successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

with app.app_context():
    db.create_all()
    seed_doctors()

if __name__ == '__main__':
    app.run(debug=True, port=5000)