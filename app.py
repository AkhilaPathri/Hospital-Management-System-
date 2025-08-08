"""
🏥 Professional Hospital Management System
Created by: Akhila
Version: 2.0
Description: A comprehensive hospital management system with modern UI and complete functionality
"""

import streamlit as st
import json
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import date, timedelta
import uuid

# ----------------- PAGE CONFIGURATION ----------------------
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# ----------------- DATA MANAGEMENT ----------------------
def ensure_data_directory():
    """Ensure data directory exists"""
    if not os.path.exists("data"):
        os.makedirs("data")

def load_data(data_type):
    """Load data from JSON file"""
    ensure_data_directory()
    try:
        with open(f"data/{data_type}.json", 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data_type, data):
    """Save data to JSON file"""
    ensure_data_directory()
    with open(f"data/{data_type}.json", 'w') as f:
        json.dump(data, f, indent=4)

def generate_id(data_type):
    """Generate unique ID for new records"""
    data = load_data(data_type)
    if not data:
        return f"{data_type[0].upper()}001"

    # Extract numeric part and increment
    ids = [item['id'] for item in data if 'id' in item]
    if ids:
        last_id = max(ids)
        num = int(last_id[1:]) + 1
        return f"{data_type[0].upper()}{num:03d}"
    return f"{data_type[0].upper()}001"

def initialize_sample_data():
    """Initialize sample data if files don't exist"""
    ensure_data_directory()

    # Initialize patients
    if not os.path.exists("data/patients.json"):
        sample_patients = [
            {
                "id": "P001",
                "name": "John Doe",
                "age": 35,
                "gender": "Male",
                "phone": "+1-555-0123",
                "email": "john.doe@email.com",
                "address": "123 Main St, City, State 12345",
                "blood_group": "O+",
                "emergency_contact": "Jane Doe - +1-555-0124",
                "medical_history": "Hypertension, Diabetes",
                "allergies": "Penicillin",
                "admission_date": "2024-01-15",
                "discharge_date": "2024-01-20",
                "status": "Discharged",
                "assigned_doctor": "Dr. John Smith",
                "room_number": "101",
                "created_date": datetime.datetime.now().isoformat()
            },
            {
                "id": "P002",
                "name": "Mary Johnson",
                "age": 28,
                "gender": "Female",
                "phone": "+1-555-0125",
                "email": "mary.johnson@email.com",
                "address": "456 Oak Ave, City, State 12345",
                "blood_group": "A+",
                "emergency_contact": "Robert Johnson - +1-555-0126",
                "medical_history": "None",
                "allergies": "None",
                "admission_date": "2024-01-18",
                "discharge_date": None,
                "status": "Admitted",
                "assigned_doctor": "Dr. Sarah Wilson",
                "room_number": "205",
                "created_date": datetime.datetime.now().isoformat()
            }
        ]
        save_data("patients", sample_patients)

    # Initialize doctors
    if not os.path.exists("data/doctors.json"):
        sample_doctors = [
            {
                "id": "D001",
                "name": "Dr. John Smith",
                "specialization": "Cardiology",
                "experience": 15,
                "qualification": "MD, FACC",
                "phone": "+1-555-0201",
                "email": "john.smith@hospital.com",
                "schedule": "Mon-Fri: 9:00 AM - 5:00 PM",
                "consultation_fee": 200,
                "department": "Cardiology",
                "status": "Active",
                "created_date": datetime.datetime.now().isoformat()
            },
            {
                "id": "D002",
                "name": "Dr. Sarah Wilson",
                "specialization": "Pediatrics",
                "experience": 12,
                "qualification": "MD, FAAP",
                "phone": "+1-555-0202",
                "email": "sarah.wilson@hospital.com",
                "schedule": "Mon-Sat: 8:00 AM - 4:00 PM",
                "consultation_fee": 180,
                "department": "Pediatrics",
                "status": "Active",
                "created_date": datetime.datetime.now().isoformat()
            },
            {
                "id": "D003",
                "name": "Dr. Michael Brown",
                "specialization": "Orthopedics",
                "experience": 20,
                "qualification": "MD, FAAOS",
                "phone": "+1-555-0203",
                "email": "michael.brown@hospital.com",
                "schedule": "Tue-Sat: 10:00 AM - 6:00 PM",
                "consultation_fee": 250,
                "department": "Orthopedics",
                "status": "Active",
                "created_date": datetime.datetime.now().isoformat()
            }
        ]
        save_data("doctors", sample_doctors)

    # Initialize appointments
    if not os.path.exists("data/appointments.json"):
        sample_appointments = [
            {
                "id": "A001",
                "patient_id": "P001",
                "patient_name": "John Doe",
                "doctor_id": "D001",
                "doctor_name": "Dr. John Smith",
                "appointment_date": "2024-01-22",
                "appointment_time": "10:00 AM",
                "type": "Consultation",
                "status": "Scheduled",
                "notes": "Regular checkup",
                "created_date": datetime.datetime.now().isoformat()
            },
            {
                "id": "A002",
                "patient_id": "P002",
                "patient_name": "Mary Johnson",
                "doctor_id": "D002",
                "doctor_name": "Dr. Sarah Wilson",
                "appointment_date": "2024-01-23",
                "appointment_time": "2:00 PM",
                "type": "Follow-up",
                "status": "Completed",
                "notes": "Post-surgery checkup",
                "created_date": datetime.datetime.now().isoformat()
            }
        ]
        save_data("appointments", sample_appointments)

    # Initialize inventory
    if not os.path.exists("data/inventory.json"):
        sample_inventory = [
            {
                "id": "M001",
                "name": "Paracetamol",
                "category": "Medicine",
                "type": "Tablet",
                "quantity": 500,
                "unit": "Tablets",
                "price_per_unit": 0.50,
                "supplier": "PharmaCorp",
                "expiry_date": "2025-12-31",
                "minimum_stock": 100,
                "status": "In Stock",
                "created_date": datetime.datetime.now().isoformat()
            },
            {
                "id": "E001",
                "name": "Stethoscope",
                "category": "Equipment",
                "type": "Diagnostic",
                "quantity": 25,
                "unit": "Pieces",
                "price_per_unit": 150.00,
                "supplier": "MedEquip Inc",
                "expiry_date": None,
                "minimum_stock": 5,
                "status": "In Stock",
                "created_date": datetime.datetime.now().isoformat()
            }
        ]
        save_data("inventory", sample_inventory)

    # Initialize billing
    if not os.path.exists("data/billing.json"):
        sample_billing = [
            {
                "id": "B001",
                "patient_id": "P001",
                "patient_name": "John Doe",
                "bill_date": "2024-01-20",
                "items": [
                    {"description": "Consultation Fee", "quantity": 1, "rate": 200, "amount": 200},
                    {"description": "Room Charges (5 days)", "quantity": 5, "rate": 100, "amount": 500},
                    {"description": "Medicine", "quantity": 1, "rate": 50, "amount": 50}
                ],
                "subtotal": 750,
                "tax": 75,
                "discount": 0,
                "total": 825,
                "payment_status": "Paid",
                "payment_method": "Credit Card",
                "created_date": datetime.datetime.now().isoformat()
            }
        ]
        save_data("billing", sample_billing)

# ----------------- AUTHENTICATION ----------------------
USER_CREDENTIALS = {
    "admin": "admin123",
    "doctor": "doc123",
    "nurse": "nurse123",
    "akhila": "mypassword"
}

def authenticate_user(username, password):
    """Authenticate user credentials"""
    return username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password

def show_login_page():
    """Display login page"""
    st.markdown("<h1 style='text-align: center;'>🏥 Hospital Management Login</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.markdown("### Please enter your credentials")
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

            col_login, col_demo = st.columns(2)

            with col_login:
                login_button = st.form_submit_button("🔐 Login", use_container_width=True)

            with col_demo:
                demo_button = st.form_submit_button("👀 Demo Login", use_container_width=True)

            if login_button:
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_name = username.title()
                    st.session_state.user_role = "Administrator" if username == "admin" else "User"
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

            if demo_button:
                # Auto-login with demo credentials
                if authenticate_user("admin", "admin123"):
                    st.session_state.logged_in = True
                    st.session_state.username = "admin"
                    st.session_state.user_name = "Administrator"
                    st.session_state.user_role = "Administrator"
                    st.success("✅ Demo login successful!")
                    st.rerun()

        # Display demo credentials
        with st.expander("🔍 Demo Credentials"):
            st.markdown("""
            **Administrator:**
            - Username: `admin`
            - Password: `admin123`

            **Doctor:**
            - Username: `doctor`
            - Password: `doc123`

            **Nurse:**
            - Username: `nurse`
            - Password: `nurse123`

            **Creator:**
            - Username: `akhila`
            - Password: `mypassword`
            """)

# ----------------- CUSTOM CSS STYLING ----------------------
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Main theme colors - Unique Purple & Teal Theme */
    :root {
        --primary-color: #6C5CE7;
        --secondary-color: #A29BFE;
        --accent-color: #00CEC9;
        --success-color: #00B894;
        --warning-color: #FDCB6E;
        --danger-color: #E84393;
        --info-color: #74B9FF;
        --light-bg: #F8F9FF;
        --white: #ffffff;
        --text-dark: #2D3436;
        --text-light: #636E72;
        --border-color: #DDD6FE;
        --sidebar-bg: linear-gradient(180deg, #2E86AB 0%, #A23B72 100%);
    }

    /* Global Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Sidebar Styling - Fixed for visibility */
    .css-1d391kg, .css-1cypcdb, .css-17eq0hr, section[data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
    }

    .css-1d391kg .css-1v0mbdj, .css-1cypcdb .css-1v0mbdj,
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar text visibility */
    section[data-testid="stSidebar"] .markdown-text-container,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div {
        color: white !important;
    }

    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 50%, var(--accent-color) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(108, 92, 231, 0.3);
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }

    /* Sidebar user info styling */
    .sidebar-user-info {
        background: rgba(255,255,255,0.15) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        margin-bottom: 1.5rem !important;
        text-align: center !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }

    .sidebar-user-info h3 {
        color: white !important;
        margin: 0 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }

    .sidebar-user-info p {
        color: rgba(255,255,255,0.9) !important;
        margin: 0.5rem 0 0 0 !important;
        font-size: 1rem !important;
    }

    .sidebar-user-info small {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.85rem !important;
    }

    /* Card styling */
    .metric-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid var(--primary-color);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }

    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, var(--light-bg) 0%, var(--white) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--info-color);
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .success-card {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }

    .error-card {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4);
        background: linear-gradient(135deg, var(--accent-color) 0%, var(--primary-color) 100%);
    }

    /* Sidebar button styling */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    /* Professional table styling */
    .dataframe {
        border: none !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }

    .dataframe th {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }

    .dataframe td {
        padding: 0.75rem 1rem !important;
        border-bottom: 1px solid var(--border-color) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .dataframe tr:hover {
        background-color: var(--light-bg) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--light-bg);
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
    }

    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid var(--border-color);
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }

    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 2px solid var(--border-color);
    }

    /* Metric styling */
    .metric-container {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        border-top: 4px solid var(--primary-color);
    }

    /* Status badges */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------- UI HELPER FUNCTIONS ----------------------
def metric_card(title, value, delta=None):
    """Create a metric card with professional styling"""
    delta_html = ""
    if delta:
        color = "#00B894" if delta >= 0 else "#E84393"
        arrow = "↗️" if delta >= 0 else "↘️"
        delta_html = f'<p style="color: {color}; margin: 0; font-size: 14px; font-weight: 600;">{arrow} {abs(delta):.1f}%</p>'

    st.markdown(f"""
    <div class="metric-card fade-in">
        <h3 style="margin: 0; color: #6C5CE7; font-size: 2rem; font-weight: 700;">{value}</h3>
        <p style="margin: 0.5rem 0 0 0; color: #636E72; font-size: 1rem; font-weight: 500;">{title}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def info_card(title, content, icon="ℹ️"):
    """Create an information card with professional styling"""
    st.markdown(f"""
    <div class="info-card fade-in">
        <h4 style="margin: 0 0 0.5rem 0; color: #6C5CE7; font-weight: 600;">
            {icon} {title}
        </h4>
        <p style="margin: 0; color: #2D3436; line-height: 1.5;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def success_message(message):
    """Display success message with professional styling"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #d1f2eb 0%, #a3e4d7 100%);
                color: #00B894; padding: 1rem; border-radius: 10px;
                border: 1px solid #a3e4d7; margin: 1rem 0; font-weight: 600;">
        <strong>✅ {message}</strong>
    </div>
    """, unsafe_allow_html=True)

def error_message(message):
    """Display error message with professional styling"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fdeef4 0%, #fad1e1 100%);
                color: #E84393; padding: 1rem; border-radius: 10px;
                border: 1px solid #fad1e1; margin: 1rem 0; font-weight: 600;">
        <strong>❌ {message}</strong>
    </div>
    """, unsafe_allow_html=True)

def status_badge(status):
    """Create a professional status badge with new color scheme"""
    colors = {
        "Active": "#00B894",
        "Inactive": "#636E72",
        "Pending": "#FDCB6E",
        "Completed": "#00B894",
        "Cancelled": "#E84393",
        "Scheduled": "#6C5CE7",
        "Admitted": "#FDCB6E",
        "Discharged": "#00B894",
        "In Stock": "#00B894",
        "Out of Stock": "#E84393",
        "Low Stock": "#FDCB6E",
        "Paid": "#00B894",
        "Unpaid": "#E84393",
        "Partial": "#74B9FF"
    }

    color = colors.get(status, "#636E72")
    return f"""
    <span class="status-badge" style="background: {color}; color: white; padding: 0.3rem 0.8rem;
                 border-radius: 20px; font-size: 0.75rem; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 0.5px; margin-left: 0.5rem;
                 box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        {status}
    </span>
    """

# ----------------- HOME PAGE ----------------------
def show_home():
    """Display the home page with welcome message and overview"""

    # Welcome section
    st.title("🏥 Welcome to Hospital Management System")
    st.subheader("Your comprehensive healthcare management solution")
    st.write("Streamline patient care, manage appointments, track inventory, and generate reports - all in one place")
    st.markdown("---")

    # Quick stats overview
    st.markdown("### 📊 System Overview")

    # Get data for overview
    patients = load_data("patients")
    doctors = load_data("doctors")
    appointments = load_data("appointments")
    inventory = load_data("inventory")
    billing = load_data("billing")

    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-container fade-in">
            <h2 style="color: #6C5CE7; font-size: 2.5rem; margin: 0;">👥</h2>
            <h3 style="color: #2D3436; margin: 0.5rem 0;">{}</h3>
            <p style="color: #636E72; margin: 0;">Total Patients</p>
        </div>
        """.format(len(patients)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-container fade-in">
            <h2 style="color: #6C5CE7; font-size: 2.5rem; margin: 0;">👨‍⚕️</h2>
            <h3 style="color: #2D3436; margin: 0.5rem 0;">{}</h3>
            <p style="color: #636E72; margin: 0;">Total Doctors</p>
        </div>
        """.format(len(doctors)), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-container fade-in">
            <h2 style="color: #6C5CE7; font-size: 2.5rem; margin: 0;">📅</h2>
            <h3 style="color: #2D3436; margin: 0.5rem 0;">{}</h3>
            <p style="color: #636E72; margin: 0;">Appointments</p>
        </div>
        """.format(len(appointments)), unsafe_allow_html=True)

    with col4:
        total_revenue = sum([b.get('total', 0) for b in billing])
        st.markdown("""
        <div class="metric-container fade-in">
            <h2 style="color: #6C5CE7; font-size: 2.5rem; margin: 0;">💰</h2>
            <h3 style="color: #2D3436; margin: 0.5rem 0;">${:,.0f}</h3>
            <p style="color: #636E72; margin: 0;">Total Revenue</p>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)

    st.markdown("---")

    # Feature highlights
    st.markdown("### ✨ Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card fade-in">
            <h4 style="color: #6C5CE7; margin-bottom: 1rem;">👥 Patient Management</h4>
            <ul style="color: #2D3436; line-height: 1.6;">
                <li>Complete patient records</li>
                <li>Medical history tracking</li>
                <li>Admission & discharge management</li>
                <li>Emergency contact information</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card fade-in">
            <h4 style="color: #6C5CE7; margin-bottom: 1rem;">📅 Appointment System</h4>
            <ul style="color: #2D3436; line-height: 1.6;">
                <li>Easy appointment scheduling</li>
                <li>Doctor availability tracking</li>
                <li>Calendar view</li>
                <li>Appointment reminders</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card fade-in">
            <h4 style="color: #6C5CE7; margin-bottom: 1rem;">💳 Billing & Reports</h4>
            <ul style="color: #2D3436; line-height: 1.6;">
                <li>Automated billing system</li>
                <li>Payment tracking</li>
                <li>Financial reports</li>
                <li>Revenue analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Recent activity summary
    st.markdown("### 🕒 Recent Activity")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Recent Patients")
        if patients:
            recent_patients = sorted(patients, key=lambda x: x.get('created_date', ''), reverse=True)[:3]
            for patient in recent_patients:
                st.markdown(f"""
                <div style="background: #F8F9FF; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
                            border-left: 4px solid #6C5CE7; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <strong style="color: #2D3436;">{patient.get('name', 'Unknown')}</strong><br>
                    <small style="color: #636E72;">ID: {patient.get('id', 'N/A')} | Status: {patient.get('status', 'Unknown')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            info_card("No Patients", "No patient records found.")

    with col2:
        st.markdown("#### Upcoming Appointments")
        if appointments:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            upcoming = [apt for apt in appointments if apt.get('appointment_date', '') >= today and apt.get('status') == 'Scheduled']
            upcoming = sorted(upcoming, key=lambda x: x.get('appointment_date', ''))[:3]

            for appointment in upcoming:
                st.markdown(f"""
                <div style="background: #F8F9FF; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
                            border-left: 4px solid #00CEC9; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <strong style="color: #2D3436;">{appointment.get('patient_name', 'Unknown')}</strong><br>
                    <small style="color: #636E72;">{appointment.get('appointment_date', 'N/A')} at {appointment.get('appointment_time', 'N/A')}</small><br>
                    <small style="color: #636E72;">Doctor: {appointment.get('doctor_name', 'N/A')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            info_card("No Appointments", "No upcoming appointments found.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #6c757d;">
        <p style="margin: 0; font-size: 1.1rem;">
            <strong>Powered by Akhila ❤️</strong> | Version 2.0 | Professional Hospital Management System
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Last updated: {}
        </p>
    </div>
    """.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# ----------------- DASHBOARD ----------------------
def show_dashboard():
    """Display the main dashboard"""

    st.markdown("""
    <div class="main-header">
        <h1>🏥 Professional Hospital Management System</h1>
        <p>Comprehensive Healthcare Management Solution</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize sample data
    initialize_sample_data()

    # Get statistics
    patients = load_data("patients")
    doctors = load_data("doctors")
    appointments = load_data("appointments")
    inventory = load_data("inventory")
    billing = load_data("billing")

    # Key Performance Indicators
    st.markdown("### 📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Patients", len(patients), 5.2)

    with col2:
        active_patients = len([p for p in patients if p.get('status') == 'Admitted'])
        metric_card("Active Patients", active_patients, 2.1)

    with col3:
        metric_card("Total Doctors", len(doctors), 0.0)

    with col4:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        today_appointments = len([a for a in appointments if a.get('appointment_date') == today])
        metric_card("Today's Appointments", today_appointments, -1.5)

    st.markdown("---")

    # Charts and Analytics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Patient Analytics")

        if patients:
            status_data = {}
            for patient in patients:
                status = patient.get('status', 'Unknown')
                status_data[status] = status_data.get(status, 0) + 1

            if status_data:
                fig_patients = px.pie(
                    values=list(status_data.values()),
                    names=list(status_data.keys()),
                    title="Patient Status Distribution",
                    color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01', '#28a745']
                )
                fig_patients.update_layout(height=400)
                st.plotly_chart(fig_patients, use_container_width=True)
        else:
            info_card("No Data", "No patient data available for analysis.")

    with col2:
        st.markdown("### 💰 Revenue Analytics")

        if billing:
            monthly_revenue = {}
            for bill in billing:
                date = bill.get('bill_date', '')
                if date:
                    try:
                        month = date[:7]  # YYYY-MM format
                        monthly_revenue[month] = monthly_revenue.get(month, 0) + bill.get('total', 0)
                    except:
                        continue

            if monthly_revenue:
                months = list(monthly_revenue.keys())
                revenues = list(monthly_revenue.values())

                fig_revenue = px.bar(
                    x=months,
                    y=revenues,
                    title="Monthly Revenue",
                    color_discrete_sequence=['#2E86AB']
                )
                fig_revenue.update_layout(
                    height=400,
                    xaxis_title="Month",
                    yaxis_title="Revenue ($)"
                )
                st.plotly_chart(fig_revenue, use_container_width=True)
        else:
            info_card("No Data", "No billing data available for analysis.")

    # Recent Activities
    st.markdown("### 🕒 Recent Activities")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Recent Patients")
        if patients:
            recent_patients = sorted(patients, key=lambda x: x.get('created_date', ''), reverse=True)[:5]

            for patient in recent_patients:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                            border-left: 4px solid #2E86AB;">
                    <strong>{patient.get('name', 'Unknown')}</strong><br>
                    <small>ID: {patient.get('id', 'N/A')} | Status: {patient.get('status', 'Unknown')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            info_card("No Patients", "No recent patient records found.")

    with col2:
        st.markdown("#### Upcoming Appointments")
        if appointments:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            upcoming = [apt for apt in appointments if apt.get('appointment_date', '') >= today and apt.get('status') == 'Scheduled']
            upcoming = sorted(upcoming, key=lambda x: x.get('appointment_date', ''))[:5]

            for appointment in upcoming:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                            border-left: 4px solid #A23B72;">
                    <strong>{appointment.get('patient_name', 'Unknown')}</strong><br>
                    <small>{appointment.get('appointment_date', 'N/A')} at {appointment.get('appointment_time', 'N/A')}</small><br>
                    <small>Doctor: {appointment.get('doctor_name', 'N/A')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            info_card("No Appointments", "No upcoming appointments found.")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**Last Updated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    with col2:
        st.markdown(f"**System Status:** 🟢 Online")

    with col3:
        st.markdown(f"**User:** {st.session_state.get('user_name', 'Unknown')}")

# ----------------- PATIENT MANAGEMENT ----------------------
def show_patient_management():
    """Display patient management interface"""

    st.markdown("## 👥 Patient Management")
    st.markdown("Manage patient records, admissions, and medical information")

    # Check if we need to show a specific tab
    default_tab = 0
    if st.session_state.get('patient_tab') == 'Add Patient':
        default_tab = 1
        st.session_state.patient_tab = None  # Reset after use

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["📋 All Patients", "➕ Add Patient", "🔍 Search Patients"])

    with tab1:
        show_all_patients()

    with tab2:
        show_add_patient()

    with tab3:
        show_search_patients()

def show_all_patients():
    """Display all patients"""

    st.markdown("### 📋 All Patients")

    patients = load_data("patients")

    if not patients:
        info_card("No Patients", "No patient records found. Add your first patient using the 'Add Patient' tab.")
        return

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Patients", len(patients))

    with col2:
        admitted = len([p for p in patients if p.get('status') == 'Admitted'])
        metric_card("Currently Admitted", admitted)

    with col3:
        discharged = len([p for p in patients if p.get('status') == 'Discharged'])
        metric_card("Discharged", discharged)

    with col4:
        emergency = len([p for p in patients if 'emergency' in p.get('medical_history', '').lower()])
        metric_card("Emergency Cases", emergency)

    st.markdown("---")

    # Display patients in a table
    if patients:
        df = pd.DataFrame(patients)

        # Select relevant columns for display
        display_columns = ['id', 'name', 'age', 'gender', 'phone', 'status', 'assigned_doctor', 'room_number']
        available_columns = [col for col in display_columns if col in df.columns]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )

def show_add_patient():
    """Display add patient form"""

    st.markdown("### ➕ Add New Patient")

    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Personal Information")
            name = st.text_input("Full Name *", placeholder="Enter patient's full name")
            age = st.number_input("Age *", min_value=0, max_value=150, value=25)
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])

            st.markdown("#### Contact Information")
            phone = st.text_input("Phone Number *", placeholder="+1-555-0123")
            email = st.text_input("Email", placeholder="patient@email.com")
            address = st.text_area("Address", placeholder="Full address")
            emergency_contact = st.text_input("Emergency Contact", placeholder="Name - Phone")

        with col2:
            st.markdown("#### Medical Information")
            medical_history = st.text_area("Medical History", placeholder="Previous conditions, surgeries, etc.")
            allergies = st.text_area("Allergies", placeholder="Known allergies")

            st.markdown("#### Admission Details")
            admission_date = st.date_input("Admission Date", value=date.today())
            discharge_date = st.date_input("Expected Discharge Date", value=date.today())

            # Get list of doctors for assignment
            doctors = load_data("doctors")
            doctor_names = [f"Dr. {doc.get('name', 'Unknown')}" for doc in doctors if doc.get('status') == 'Active']
            assigned_doctor = st.selectbox("Assigned Doctor", ["None"] + doctor_names)

            room_number = st.text_input("Room Number", placeholder="e.g., 101, 205")
            status = st.selectbox("Status", ["Admitted", "Discharged", "Transferred", "Emergency"])

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("💾 Add Patient", type="primary", use_container_width=True)

        with col2:
            clear = st.form_submit_button("🔄 Clear Form", use_container_width=True)

        if submit:
            if name and age and gender and phone:
                patients = load_data("patients")
                patient_data = {
                    "id": generate_id("patients"),
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "blood_group": blood_group,
                    "emergency_contact": emergency_contact,
                    "medical_history": medical_history,
                    "allergies": allergies,
                    "admission_date": str(admission_date),
                    "discharge_date": str(discharge_date) if discharge_date != admission_date else None,
                    "status": status,
                    "assigned_doctor": assigned_doctor if assigned_doctor != "None" else None,
                    "room_number": room_number,
                    "created_date": datetime.datetime.now().isoformat()
                }

                patients.append(patient_data)
                save_data("patients", patients)
                success_message(f"Patient '{name}' added successfully with ID: {patient_data['id']}")
                st.rerun()
            else:
                error_message("Please fill in all required fields marked with *")

        if clear:
            st.rerun()

def show_search_patients():
    """Display patient search functionality"""

    st.markdown("### 🔍 Search Patients")

    patients = load_data("patients")

    if not patients:
        info_card("No Patients", "No patient records available for search.")
        return

    # Search filters
    col1, col2, col3 = st.columns(3)

    with col1:
        search_name = st.text_input("Search by Name", placeholder="Enter patient name")

    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Admitted", "Discharged", "Transferred", "Emergency"])

    with col3:
        filter_gender = st.selectbox("Filter by Gender", ["All", "Male", "Female", "Other"])

    # Apply filters
    filtered_patients = patients

    if search_name:
        filtered_patients = [p for p in filtered_patients if search_name.lower() in p.get('name', '').lower()]

    if filter_status != "All":
        filtered_patients = [p for p in filtered_patients if p.get('status') == filter_status]

    if filter_gender != "All":
        filtered_patients = [p for p in filtered_patients if p.get('gender') == filter_gender]

    # Display results
    st.markdown(f"### Search Results ({len(filtered_patients)} patients found)")

    if filtered_patients:
        df = pd.DataFrame(filtered_patients)

        # Select relevant columns
        display_columns = ['id', 'name', 'age', 'gender', 'phone', 'status', 'assigned_doctor', 'room_number']
        available_columns = [col for col in display_columns if col in df.columns]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        info_card("No Results", "No patients match your search criteria.")

# ----------------- DOCTOR MANAGEMENT ----------------------
def show_doctor_management():
    """Display doctor management interface"""

    st.markdown("## 👨‍⚕️ Doctor Management")
    st.markdown("Manage doctor profiles, specializations, and schedules")

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["👨‍⚕️ All Doctors", "➕ Add Doctor", "📅 Schedules"])

    with tab1:
        show_all_doctors()

    with tab2:
        show_add_doctor()

    with tab3:
        show_doctor_schedules()

def show_all_doctors():
    """Display all doctors"""

    st.markdown("### 👨‍⚕️ All Doctors")

    doctors = load_data("doctors")

    if not doctors:
        info_card("No Doctors", "No doctor records found. Add your first doctor using the 'Add Doctor' tab.")
        return

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Doctors", len(doctors))

    with col2:
        active = len([d for d in doctors if d.get('status') == 'Active'])
        metric_card("Active Doctors", active)

    with col3:
        specializations = len(set([d.get('specialization', '') for d in doctors]))
        metric_card("Specializations", specializations)

    with col4:
        avg_experience = sum([d.get('experience', 0) for d in doctors]) / len(doctors) if doctors else 0
        metric_card("Avg Experience", f"{avg_experience:.1f} years")

    st.markdown("---")

    # Display doctors in a table
    if doctors:
        df = pd.DataFrame(doctors)

        # Select relevant columns for display
        display_columns = ['id', 'name', 'specialization', 'experience', 'phone', 'consultation_fee', 'status']
        available_columns = [col for col in display_columns if col in df.columns]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )

def show_add_doctor():
    """Display add doctor form"""

    st.markdown("### ➕ Add New Doctor")

    with st.form("add_doctor_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Personal Information")
            name = st.text_input("Doctor Name *", placeholder="Enter doctor's full name")
            specialization = st.selectbox("Specialization *", [
                "Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology",
                "Psychiatry", "Radiology", "Anesthesiology", "Emergency Medicine",
                "Internal Medicine", "Surgery", "Gynecology", "Ophthalmology",
                "ENT", "Urology", "Oncology", "Other"
            ])
            department = st.selectbox("Department *", [
                "Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology",
                "Psychiatry", "Radiology", "Anesthesiology", "Emergency",
                "Internal Medicine", "Surgery", "Gynecology", "Ophthalmology",
                "ENT", "Urology", "Oncology", "General"
            ])
            experience = st.number_input("Experience (years) *", min_value=0, max_value=50, value=5)
            qualification = st.text_input("Qualification *", placeholder="e.g., MD, MBBS, MS")

        with col2:
            st.markdown("#### Contact & Professional Details")
            phone = st.text_input("Phone Number *", placeholder="+1-555-0123")
            email = st.text_input("Email *", placeholder="doctor@hospital.com")
            consultation_fee = st.number_input("Consultation Fee ($) *", min_value=0.0, value=200.0, step=10.0)

            st.markdown("#### Schedule")
            schedule = st.text_area("Schedule *",
                                  value="Mon-Fri: 9:00 AM - 5:00 PM",
                                  placeholder="Enter working hours and days")

            status = st.selectbox("Status", ["Active", "Inactive", "On Leave"])

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("💾 Add Doctor", type="primary", use_container_width=True)

        with col2:
            clear = st.form_submit_button("🔄 Clear Form", use_container_width=True)

        if submit:
            if name and specialization and department and phone and email and qualification:
                doctors = load_data("doctors")
                doctor_data = {
                    "id": generate_id("doctors"),
                    "name": name,
                    "specialization": specialization,
                    "department": department,
                    "experience": experience,
                    "qualification": qualification,
                    "phone": phone,
                    "email": email,
                    "consultation_fee": consultation_fee,
                    "schedule": schedule,
                    "status": status,
                    "created_date": datetime.datetime.now().isoformat()
                }

                doctors.append(doctor_data)
                save_data("doctors", doctors)
                success_message(f"Doctor '{name}' added successfully with ID: {doctor_data['id']}")
                st.rerun()
            else:
                error_message("Please fill in all required fields marked with *")

        if clear:
            st.rerun()

def show_doctor_schedules():
    """Display doctor schedules"""

    st.markdown("### 📅 Doctor Schedules & Availability")

    doctors = load_data("doctors")

    if not doctors:
        info_card("No Doctors", "No doctor records available.")
        return

    # Filter by department
    departments = list(set([d.get('department', 'Unknown') for d in doctors]))
    selected_dept = st.selectbox("Filter by Department", ["All"] + departments)

    filtered_doctors = doctors
    if selected_dept != "All":
        filtered_doctors = [d for d in doctors if d.get('department') == selected_dept]

    # Display schedules in a table format
    schedule_data = []
    for doctor in filtered_doctors:
        if doctor.get('status') == 'Active':
            schedule_data.append({
                "Doctor": doctor.get('name', 'Unknown'),
                "Specialization": doctor.get('specialization', 'Unknown'),
                "Department": doctor.get('department', 'Unknown'),
                "Schedule": doctor.get('schedule', 'Not specified'),
                "Consultation Fee": f"${doctor.get('consultation_fee', 0):.2f}",
                "Phone": doctor.get('phone', 'N/A'),
                "Status": doctor.get('status', 'Unknown')
            })

    if schedule_data:
        df = pd.DataFrame(schedule_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        info_card("No Active Doctors", "No active doctors found in the selected department.")

# ----------------- APPOINTMENTS ----------------------
def show_appointments():
    """Display appointments management interface"""

    st.markdown("## 📅 Appointment Management")
    st.markdown("Schedule, manage, and track patient appointments")

    # Check if we need to show a specific tab
    if st.session_state.get('appointment_tab') == 'Schedule Appointment':
        st.session_state.appointment_tab = None  # Reset after use

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["📅 All Appointments", "➕ Schedule Appointment", "📊 Calendar View"])

    with tab1:
        show_all_appointments()

    with tab2:
        show_schedule_appointment()

    with tab3:
        show_calendar_view()

def show_all_appointments():
    """Display all appointments"""

    st.markdown("### 📅 All Appointments")

    appointments = load_data("appointments")

    if not appointments:
        info_card("No Appointments", "No appointments found. Schedule your first appointment using the 'Schedule Appointment' tab.")
        return

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Appointments", len(appointments))

    with col2:
        scheduled = len([a for a in appointments if a.get('status') == 'Scheduled'])
        metric_card("Scheduled", scheduled)

    with col3:
        completed = len([a for a in appointments if a.get('status') == 'Completed'])
        metric_card("Completed", completed)

    with col4:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        today_appointments = len([a for a in appointments if a.get('appointment_date') == today])
        metric_card("Today", today_appointments)

    st.markdown("---")

    # Display appointments in a table
    if appointments:
        df = pd.DataFrame(appointments)

        # Select relevant columns for display
        display_columns = ['id', 'patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'type', 'status']
        available_columns = [col for col in display_columns if col in df.columns]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )

def show_schedule_appointment():
    """Display schedule appointment form"""

    st.markdown("### ➕ Schedule New Appointment")

    # Get patients and doctors for dropdowns
    patients = load_data("patients")
    doctors = load_data("doctors")

    if not patients or not doctors:
        error_message("Please ensure you have both patients and doctors in the system before scheduling appointments.")
        return

    with st.form("schedule_appointment_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Patient & Doctor Selection")

            # Patient selection
            patient_options = [f"{p.get('name', 'Unknown')} (ID: {p.get('id', 'N/A')})" for p in patients]
            selected_patient = st.selectbox("Select Patient *", patient_options)

            # Doctor selection
            active_doctors = [d for d in doctors if d.get('status') == 'Active']
            doctor_options = [f"{d.get('name', 'Unknown')} - {d.get('specialization', 'N/A')}" for d in active_doctors]
            selected_doctor = st.selectbox("Select Doctor *", doctor_options)

            # Appointment type
            appointment_type = st.selectbox("Appointment Type *", [
                "Consultation", "Follow-up", "Check-up", "Emergency",
                "Surgery", "Therapy", "Vaccination", "Diagnostic"
            ])

        with col2:
            st.markdown("#### Date & Time")

            # Date selection (minimum today)
            appointment_date = st.date_input("Appointment Date *",
                                           min_value=date.today(),
                                           value=date.today())

            # Time selection
            time_slots = [
                "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
                "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM", "02:00 PM", "02:30 PM",
                "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM"
            ]
            appointment_time = st.selectbox("Appointment Time *", time_slots)

            # Notes
            notes = st.text_area("Notes", placeholder="Additional notes or special instructions")

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("📅 Schedule", type="primary", use_container_width=True)

        with col2:
            clear = st.form_submit_button("🔄 Clear", use_container_width=True)

        if submit:
            if selected_patient and selected_doctor and appointment_date and appointment_time:
                # Extract patient and doctor information
                patient_id = selected_patient.split("ID: ")[1].split(")")[0]
                patient_name = selected_patient.split(" (ID:")[0]
                doctor_name = selected_doctor.split(" - ")[0]

                # Find doctor ID
                doctor_id = None
                for doctor in active_doctors:
                    if doctor.get('name') == doctor_name:
                        doctor_id = doctor.get('id')
                        break

                appointments = load_data("appointments")
                appointment_data = {
                    "id": generate_id("appointments"),
                    "patient_id": patient_id,
                    "patient_name": patient_name,
                    "doctor_id": doctor_id,
                    "doctor_name": doctor_name,
                    "appointment_date": str(appointment_date),
                    "appointment_time": appointment_time,
                    "type": appointment_type,
                    "status": "Scheduled",
                    "notes": notes,
                    "created_date": datetime.datetime.now().isoformat()
                }

                appointments.append(appointment_data)
                save_data("appointments", appointments)
                success_message(f"Appointment scheduled successfully! ID: {appointment_data['id']}")
                st.rerun()
            else:
                error_message("Please fill in all required fields marked with *")

        if clear:
            st.rerun()

def show_calendar_view():
    """Display calendar view of appointments"""

    st.markdown("### 📊 Calendar View")

    appointments = load_data("appointments")

    if not appointments:
        info_card("No Appointments", "No appointments to display in calendar view.")
        return

    # Date range selector
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", value=date.today())

    with col2:
        end_date = st.date_input("End Date", value=date.today() + timedelta(days=7))

    # Filter appointments by date range
    filtered_appointments = []
    for appointment in appointments:
        apt_date = appointment.get('appointment_date', '')
        if apt_date and start_date <= datetime.datetime.strptime(apt_date, '%Y-%m-%d').date() <= end_date:
            filtered_appointments.append(appointment)

    if filtered_appointments:
        # Group appointments by date
        appointments_by_date = {}
        for appointment in filtered_appointments:
            apt_date = appointment.get('appointment_date', '')
            if apt_date not in appointments_by_date:
                appointments_by_date[apt_date] = []
            appointments_by_date[apt_date].append(appointment)

        # Display appointments by date
        for apt_date in sorted(appointments_by_date.keys()):
            st.markdown(f"#### 📅 {apt_date}")

            daily_appointments = appointments_by_date[apt_date]
            daily_appointments.sort(key=lambda x: x.get('appointment_time', ''))

            for appointment in daily_appointments:
                badge = status_badge(appointment.get('status', 'Unknown'))
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                            border-left: 4px solid #F18F01;">
                    <strong>{appointment.get('appointment_time', 'N/A')}</strong> -
                    {appointment.get('patient_name', 'Unknown')} with {appointment.get('doctor_name', 'Unknown')}
                    {badge}
                    <br><small>{appointment.get('type', 'N/A')} | {appointment.get('notes', 'No notes')}</small>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
    else:
        info_card("No Appointments", f"No appointments found between {start_date} and {end_date}.")

# ----------------- BILLING ----------------------
def show_billing():
    """Display billing management interface"""

    st.markdown("## 💳 Billing Management")
    st.markdown("Manage patient bills, payments, and financial records")

    # Check if we need to show a specific tab
    if st.session_state.get('billing_tab') == 'Create Bill':
        st.session_state.billing_tab = None  # Reset after use

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["💳 All Bills", "➕ Create Bill", "📊 Financial Reports"])

    with tab1:
        show_all_bills()

    with tab2:
        show_create_bill()

    with tab3:
        show_financial_reports()

def show_all_bills():
    """Display all bills"""

    st.markdown("### 💳 All Bills")

    bills = load_data("billing")

    if not bills:
        info_card("No Bills", "No billing records found. Create your first bill using the 'Create Bill' tab.")
        return

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Bills", len(bills))

    with col2:
        total_revenue = sum([b.get('total', 0) for b in bills])
        metric_card("Total Revenue", f"${total_revenue:,.2f}")

    with col3:
        paid_bills = len([b for b in bills if b.get('payment_status') == 'Paid'])
        metric_card("Paid Bills", paid_bills)

    with col4:
        pending_bills = len([b for b in bills if b.get('payment_status') == 'Pending'])
        metric_card("Pending Bills", pending_bills)

    st.markdown("---")

    # Display bills in a table
    if bills:
        df = pd.DataFrame(bills)

        # Select relevant columns for display
        display_columns = ['id', 'patient_name', 'bill_date', 'total', 'payment_status', 'payment_method']
        available_columns = [col for col in display_columns if col in df.columns]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )

def show_create_bill():
    """Display create bill form"""

    st.markdown("### ➕ Create New Bill")

    patients = load_data("patients")

    if not patients:
        error_message("Please add patients to the system before creating bills.")
        return

    with st.form("create_bill_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Patient Information")

            # Patient selection
            patient_options = [f"{p.get('name', 'Unknown')} (ID: {p.get('id', 'N/A')})" for p in patients]
            selected_patient = st.selectbox("Select Patient *", patient_options)

            bill_date = st.date_input("Bill Date *", value=date.today())

            st.markdown("#### Bill Items")

            # Simple billing items
            consultation_fee = st.number_input("Consultation Fee ($)", min_value=0.0, value=200.0, step=10.0)
            room_charges = st.number_input("Room Charges ($)", min_value=0.0, value=0.0, step=10.0)
            medicine_charges = st.number_input("Medicine Charges ($)", min_value=0.0, value=0.0, step=5.0)
            lab_charges = st.number_input("Lab Test Charges ($)", min_value=0.0, value=0.0, step=10.0)
            other_charges = st.number_input("Other Charges ($)", min_value=0.0, value=0.0, step=5.0)

        with col2:
            st.markdown("#### Payment Details")

            # Calculate totals
            subtotal = consultation_fee + room_charges + medicine_charges + lab_charges + other_charges
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=50.0, value=10.0, step=0.5)
            tax_amount = subtotal * (tax_rate / 100)
            discount = st.number_input("Discount ($)", min_value=0.0, value=0.0, step=5.0)
            total = subtotal + tax_amount - discount

            st.markdown("#### Summary")
            st.write(f"**Subtotal:** ${subtotal:.2f}")
            st.write(f"**Tax ({tax_rate}%):** ${tax_amount:.2f}")
            st.write(f"**Discount:** ${discount:.2f}")
            st.write(f"**Total:** ${total:.2f}")

            payment_status = st.selectbox("Payment Status", ["Pending", "Paid", "Partial"])
            payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "Insurance", "Check"])

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("💾 Create Bill", type="primary", use_container_width=True)

        with col2:
            clear = st.form_submit_button("🔄 Clear", use_container_width=True)

        if submit:
            if selected_patient and total > 0:
                # Extract patient information
                patient_id = selected_patient.split("ID: ")[1].split(")")[0]
                patient_name = selected_patient.split(" (ID:")[0]

                bills = load_data("billing")

                # Create bill items
                items = []
                if consultation_fee > 0:
                    items.append({"description": "Consultation Fee", "quantity": 1, "rate": consultation_fee, "amount": consultation_fee})
                if room_charges > 0:
                    items.append({"description": "Room Charges", "quantity": 1, "rate": room_charges, "amount": room_charges})
                if medicine_charges > 0:
                    items.append({"description": "Medicine Charges", "quantity": 1, "rate": medicine_charges, "amount": medicine_charges})
                if lab_charges > 0:
                    items.append({"description": "Lab Test Charges", "quantity": 1, "rate": lab_charges, "amount": lab_charges})
                if other_charges > 0:
                    items.append({"description": "Other Charges", "quantity": 1, "rate": other_charges, "amount": other_charges})

                bill_data = {
                    "id": generate_id("billing"),
                    "patient_id": patient_id,
                    "patient_name": patient_name,
                    "bill_date": str(bill_date),
                    "items": items,
                    "subtotal": subtotal,
                    "tax": tax_amount,
                    "discount": discount,
                    "total": total,
                    "payment_status": payment_status,
                    "payment_method": payment_method,
                    "created_date": datetime.datetime.now().isoformat()
                }

                bills.append(bill_data)
                save_data("billing", bills)
                success_message(f"Bill created successfully! ID: {bill_data['id']} | Total: ${total:.2f}")
                st.rerun()
            else:
                error_message("Please select a patient and ensure the total amount is greater than 0")

        if clear:
            st.rerun()

def show_financial_reports():
    """Display financial reports"""

    st.markdown("### 📊 Financial Reports")

    bills = load_data("billing")

    if not bills:
        info_card("No Data", "No billing data available for financial reports.")
        return

    # Revenue analytics
    col1, col2 = st.columns(2)

    with col1:
        # Monthly revenue
        monthly_revenue = {}
        for bill in bills:
            date = bill.get('bill_date', '')
            if date:
                try:
                    month = date[:7]  # YYYY-MM format
                    monthly_revenue[month] = monthly_revenue.get(month, 0) + bill.get('total', 0)
                except:
                    continue

        if monthly_revenue:
            months = list(monthly_revenue.keys())
            revenues = list(monthly_revenue.values())

            fig_revenue = px.bar(
                x=months,
                y=revenues,
                title="Monthly Revenue",
                color_discrete_sequence=['#2E86AB']
            )
            fig_revenue.update_layout(
                xaxis_title="Month",
                yaxis_title="Revenue ($)"
            )
            st.plotly_chart(fig_revenue, use_container_width=True)

    with col2:
        # Payment status distribution
        payment_status = {}
        for bill in bills:
            status = bill.get('payment_status', 'Unknown')
            payment_status[status] = payment_status.get(status, 0) + 1

        if payment_status:
            fig_status = px.pie(
                values=list(payment_status.values()),
                names=list(payment_status.keys()),
                title="Payment Status Distribution",
                color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
            )
            st.plotly_chart(fig_status, use_container_width=True)

# ----------------- INVENTORY ----------------------
def show_inventory():
    """Display inventory management interface"""

    st.markdown("## 📦 Inventory Management")
    st.markdown("Manage medicines, equipment, and medical supplies")

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["📦 All Items", "➕ Add Item", "⚠️ Low Stock Alerts"])

    with tab1:
        show_all_inventory()

    with tab2:
        show_add_inventory()

    with tab3:
        show_low_stock_alerts()

def show_all_inventory():
    """Display all inventory items"""

    st.markdown("### 📦 All Inventory Items")

    inventory = load_data("inventory")

    if not inventory:
        info_card("No Items", "No inventory items found. Add your first item using the 'Add Item' tab.")
        return

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Items", len(inventory))

    with col2:
        in_stock = len([i for i in inventory if i.get('status') == 'In Stock'])
        metric_card("In Stock", in_stock)

    with col3:
        low_stock = len([i for i in inventory if i.get('quantity', 0) <= i.get('minimum_stock', 0)])
        metric_card("Low Stock", low_stock)

    with col4:
        total_value = sum([i.get('quantity', 0) * i.get('price_per_unit', 0) for i in inventory])
        metric_card("Total Value", f"${total_value:,.2f}")

    st.markdown("---")

    # Display inventory in a table
    if inventory:
        df = pd.DataFrame(inventory)

        # Select relevant columns for display
        display_columns = ['id', 'name', 'category', 'quantity', 'unit', 'price_per_unit', 'status']
        available_columns = [col for col in display_columns if col in df.columns]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )

def show_add_inventory():
    """Display add inventory form"""

    st.markdown("### ➕ Add New Inventory Item")

    with st.form("add_inventory_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Item Information")
            name = st.text_input("Item Name *", placeholder="Enter item name")
            category = st.selectbox("Category *", ["Medicine", "Equipment", "Supplies", "Other"])
            item_type = st.text_input("Type", placeholder="e.g., Tablet, Injection, Diagnostic")
            quantity = st.number_input("Quantity *", min_value=0, value=0)
            unit = st.text_input("Unit *", placeholder="e.g., Tablets, Pieces, Bottles")

        with col2:
            st.markdown("#### Pricing & Details")
            price_per_unit = st.number_input("Price per Unit ($) *", min_value=0.0, value=0.0, step=0.01)
            supplier = st.text_input("Supplier", placeholder="Supplier name")
            expiry_date = st.date_input("Expiry Date (if applicable)", value=None)
            minimum_stock = st.number_input("Minimum Stock Level *", min_value=0, value=10)
            status = st.selectbox("Status", ["In Stock", "Out of Stock", "Low Stock"])

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("💾 Add Item", type="primary", use_container_width=True)

        with col2:
            clear = st.form_submit_button("🔄 Clear", use_container_width=True)

        if submit:
            if name and category and quantity >= 0 and unit and price_per_unit >= 0:
                inventory = load_data("inventory")
                item_data = {
                    "id": generate_id("inventory"),
                    "name": name,
                    "category": category,
                    "type": item_type,
                    "quantity": quantity,
                    "unit": unit,
                    "price_per_unit": price_per_unit,
                    "supplier": supplier,
                    "expiry_date": str(expiry_date) if expiry_date else None,
                    "minimum_stock": minimum_stock,
                    "status": status,
                    "created_date": datetime.datetime.now().isoformat()
                }

                inventory.append(item_data)
                save_data("inventory", inventory)
                success_message(f"Item '{name}' added successfully with ID: {item_data['id']}")
                st.rerun()
            else:
                error_message("Please fill in all required fields marked with *")

        if clear:
            st.rerun()

def show_low_stock_alerts():
    """Display low stock alerts"""

    st.markdown("### ⚠️ Low Stock Alerts")

    inventory = load_data("inventory")

    if not inventory:
        info_card("No Items", "No inventory items available.")
        return

    # Find low stock items
    low_stock_items = [item for item in inventory if item.get('quantity', 0) <= item.get('minimum_stock', 0)]

    if low_stock_items:
        st.warning(f"⚠️ {len(low_stock_items)} items are running low on stock!")

        # Display low stock items
        for item in low_stock_items:
            st.markdown(f"""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                        border-left: 4px solid #ffc107;">
                <strong>{item.get('name', 'Unknown')}</strong> ({item.get('category', 'Unknown')})<br>
                <small>Current Stock: {item.get('quantity', 0)} {item.get('unit', '')} |
                Minimum Required: {item.get('minimum_stock', 0)} {item.get('unit', '')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        success_message("✅ All items are adequately stocked!")

# ----------------- REPORTS ----------------------
def show_reports():
    """Display reports and analytics"""

    st.markdown("## 📊 Reports & Analytics")
    st.markdown("Comprehensive reports and data analytics")

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "👥 Patient Reports", "💰 Financial Reports"])

    with tab1:
        show_overview_reports()

    with tab2:
        show_patient_reports()

    with tab3:
        show_financial_reports()

def show_overview_reports():
    """Display overview reports"""

    st.markdown("### 📈 System Overview")

    # Get all data
    patients = load_data("patients")
    doctors = load_data("doctors")
    appointments = load_data("appointments")
    inventory = load_data("inventory")
    billing = load_data("billing")

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Patients", len(patients))
        metric_card("Active Patients", len([p for p in patients if p.get('status') == 'Admitted']))

    with col2:
        metric_card("Total Doctors", len(doctors))
        metric_card("Active Doctors", len([d for d in doctors if d.get('status') == 'Active']))

    with col3:
        metric_card("Total Appointments", len(appointments))
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        metric_card("Today's Appointments", len([a for a in appointments if a.get('appointment_date') == today]))

    with col4:
        total_revenue = sum([b.get('total', 0) for b in billing])
        metric_card("Total Revenue", f"${total_revenue:,.2f}")
        metric_card("Inventory Items", len(inventory))

def show_patient_reports():
    """Display patient-specific reports"""

    st.markdown("### 👥 Patient Reports")

    patients = load_data("patients")

    if not patients:
        info_card("No Data", "No patient data available for reports.")
        return

    # Patient analytics
    col1, col2 = st.columns(2)

    with col1:
        # Gender distribution
        gender_data = {}
        for patient in patients:
            gender = patient.get('gender', 'Unknown')
            gender_data[gender] = gender_data.get(gender, 0) + 1

        if gender_data:
            fig_gender = px.pie(
                values=list(gender_data.values()),
                names=list(gender_data.keys()),
                title="Patient Gender Distribution",
                color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01']
            )
            st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        # Status distribution
        status_data = {}
        for patient in patients:
            status = patient.get('status', 'Unknown')
            status_data[status] = status_data.get(status, 0) + 1

        if status_data:
            fig_status = px.bar(
                x=list(status_data.keys()),
                y=list(status_data.values()),
                title="Patient Status Distribution",
                color_discrete_sequence=['#2E86AB']
            )
            st.plotly_chart(fig_status, use_container_width=True)

# ----------------- SETTINGS ----------------------
def show_settings():
    """Display settings and configuration"""

    st.markdown("## ⚙️ Settings & Configuration")
    st.markdown("System settings and user preferences")

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["👤 User Profile", "🏥 Hospital Info", "🔧 System Settings"])

    with tab1:
        show_user_profile()

    with tab2:
        show_hospital_info()

    with tab3:
        show_system_settings()

def show_user_profile():
    """Display user profile settings"""

    st.markdown("### 👤 User Profile")

    # Current user information
    st.markdown("#### Current User Information")
    st.write(f"**Username:** {st.session_state.get('username', 'Unknown')}")
    st.write(f"**Name:** {st.session_state.get('user_name', 'Unknown')}")
    st.write(f"**Role:** {st.session_state.get('user_role', 'Unknown')}")

    st.markdown("---")

    # Change password section
    st.markdown("#### Change Password")
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.form_submit_button("🔒 Change Password"):
            if new_password == confirm_password:
                success_message("Password change functionality will be implemented in future updates.")
            else:
                error_message("New passwords do not match!")

def show_hospital_info():
    """Display hospital information settings"""

    st.markdown("### 🏥 Hospital Information")

    # Hospital details form
    with st.form("hospital_info_form"):
        col1, col2 = st.columns(2)

        with col1:
            hospital_name = st.text_input("Hospital Name", value="City General Hospital")
            address = st.text_area("Address", value="123 Medical Center Drive\nCity, State 12345")
            phone = st.text_input("Phone", value="+1-555-HOSPITAL")
            email = st.text_input("Email", value="info@citygeneralhospital.com")

        with col2:
            website = st.text_input("Website", value="www.citygeneralhospital.com")
            license_number = st.text_input("License Number", value="HL-2024-001")
            established_year = st.number_input("Established Year", min_value=1800, max_value=2024, value=1985)
            bed_capacity = st.number_input("Bed Capacity", min_value=1, value=200)

        if st.form_submit_button("💾 Save Hospital Information"):
            success_message("Hospital information saved successfully!")

def show_system_settings():
    """Display system settings"""

    st.markdown("### 🔧 System Settings")

    # System preferences
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Display Settings")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French"])
        timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "CST"])

    with col2:
        st.markdown("#### Notification Settings")
        email_notifications = st.checkbox("Email Notifications", value=True)
        sms_notifications = st.checkbox("SMS Notifications", value=False)
        appointment_reminders = st.checkbox("Appointment Reminders", value=True)

    st.markdown("---")

    # Data management
    st.markdown("#### Data Management")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📤 Export Data", use_container_width=True):
            info_card("Export", "Data export functionality will be implemented.")

    with col2:
        if st.button("📥 Import Data", use_container_width=True):
            info_card("Import", "Data import functionality will be implemented.")

    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            info_card("Clear Data", "Data clearing functionality will be implemented with proper confirmation.")

# ----------------- MAIN APPLICATION ----------------------
def main():
    """Main application function"""

    load_css()
    initialize_sample_data()

    # Authentication check
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        show_login_page()
        return

    # Main header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #2E86AB, #A23B72); padding: 1rem;
                border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>🏥 Professional Hospital Management System</h1>
        <p>Comprehensive Healthcare Management Solution</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        # User welcome section with professional styling
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.15); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
            <h3 style="color: #ffffff; margin: 0; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.2rem;">🏥 Hospital Management</h3>
            <p style="color: #ffffff; margin: 0.8rem 0 0.3rem 0; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); font-size: 1rem;">Welcome, {st.session_state.get('user_name', 'User')}</p>
            <small style="color: #ffffff; font-weight: 400; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); font-size: 0.85rem;">{st.session_state.get('user_role', 'User')}</small>
        </div>
        """, unsafe_allow_html=True)

        # Navigation buttons
        st.markdown("### 🧭 Navigation")

        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.session_state.current_page = 'Home'
            st.rerun()

        if st.button("👥 Patient Management", use_container_width=True, key="nav_patients"):
            st.session_state.current_page = 'Patient Management'
            st.rerun()

        if st.button("👨‍⚕️ Doctor Management", use_container_width=True, key="nav_doctors"):
            st.session_state.current_page = 'Doctor Management'
            st.rerun()

        if st.button("📅 Appointments", use_container_width=True, key="nav_appointments"):
            st.session_state.current_page = 'Appointments'
            st.rerun()

        if st.button("💳 Billing", use_container_width=True, key="nav_billing"):
            st.session_state.current_page = 'Billing'
            st.rerun()

        if st.button("📦 Inventory", use_container_width=True, key="nav_inventory"):
            st.session_state.current_page = 'Inventory'
            st.rerun()

        if st.button("📊 Reports", use_container_width=True, key="nav_reports"):
            st.session_state.current_page = 'Reports'
            st.rerun()

        if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
            st.session_state.current_page = 'Settings'
            st.rerun()

        if st.button("📈 Dashboard", use_container_width=True, key="nav_dashboard"):
            st.session_state.current_page = 'Dashboard'
            st.rerun()

        st.markdown("---")

        # Quick Actions
        st.markdown("### ⚡ Quick Actions")

        if st.button("➕ Add Patient", use_container_width=True, key="quick_add_patient"):
            st.session_state.current_page = 'Patient Management'
            st.session_state.patient_tab = 'Add Patient'
            st.rerun()

        if st.button("📅 Schedule Appointment", use_container_width=True, key="quick_schedule"):
            st.session_state.current_page = 'Appointments'
            st.session_state.appointment_tab = 'Schedule Appointment'
            st.rerun()

        if st.button("💳 Create Bill", use_container_width=True, key="quick_bill"):
            st.session_state.current_page = 'Billing'
            st.session_state.billing_tab = 'Create Bill'
            st.rerun()

        st.markdown("---")

        # System Status
        st.markdown("### 📊 System Status")
        patients = load_data("patients")
        doctors = load_data("doctors")
        appointments = load_data("appointments")

        st.metric("Total Patients", len(patients))
        st.metric("Total Doctors", len(doctors))
        st.metric("Total Appointments", len(appointments))

        st.markdown("---")

        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.rerun()

        # Footer
        st.markdown("---")
        st.markdown("**Powered by Akhila ❤️**")

    # Route to appropriate page based on session state
    current_page = st.session_state.get('current_page', 'Home')

    if current_page == 'Home':
        show_home()
    elif current_page == 'Patient Management':
        show_patient_management()
    elif current_page == 'Doctor Management':
        show_doctor_management()
    elif current_page == 'Appointments':
        show_appointments()
    elif current_page == 'Billing':
        show_billing()
    elif current_page == 'Inventory':
        show_inventory()
    elif current_page == 'Reports':
        show_reports()
    elif current_page == 'Settings':
        show_settings()
    elif current_page == 'Dashboard':
        show_dashboard()

if __name__ == "__main__":
    main()
