# Nursing Home Management System

A Flask-based web application designed to efficiently manage nursing home operations, including resident data, staff roles, medical risk profiles, and account administration. The system supports role-based access to ensure secure management of sensitive information.

---

## 🚀 Features

### 1. User & Role Management
- Multiple user roles:
  - Admin
  - Doctor
  - Nurse
  - Patient
- Admin can:
  - View all accounts
  - Update user roles (except other Admins)
- Secure login authentication with hashed passwords
- Profile editing (name, DOB, gender, contact)

---

### 2. Patient Profile Management
- Each patient has a dedicated medical profile
- Includes:
  - Cultural & dietary needs
  - Allergens
  - Medical history
  - Risk level
- Profiles editable by staff with correct permissions

---

### 3. Patient Log Tracking System
- Staff can log:
  - Medical condition
  - Emotional condition
  - Additional notes
- Patients can add personal notes to logs
- Logs editable by authorized users

---

### 4. Appointment Scheduling System
- Patients can request appointments with doctors
- Appointment status flow:
  - Pending → Scheduled → Completed
  - Can also be Cancelled
- Doctors are assigned upon approval
- All activity recorded in database

---

### 5. Feedback Management System
- Integrated Sheety API feedback form
- Rating and feedback type collected
- Anonymous or identified submissions
- Admin dashboard to view feedback list

---

## Security and Validation
- Password hashing using werkzeug.security
- Form validation using WTForms
- Access restricted using Flask-Login and role-based checks

---

## 🛠️ Tech Stack

| Area | Technology |
|------|------------|
| Backend | Flask, SQLAlchemy |
| ORM | Flask SQLAlchemy |
| Authentication | Flask-Login |
| Forms | Flask-WTF |
| Database | SQLite / (compatible with others) |
| Frontend | Jinja2 Templates, Bootstrap |

---

## 📂 Project Structure
```
CareLog/
├─ app/
│ ├─ init.py
│ ├─ admin_manager.py
│ ├─ appointment_manager.py
│ ├─ auth_manager.py
│ ├─ forms.py
│ ├─ models.py
│ ├─ profile_manager.py
│ ├─ staff_manager.py
│ └─ validators.py
│
├─ instance/
│ └─ data.db # System database
│
├─ routes/ # Website routes
│
├─ static/
│ ├─ assets/ # Website assets
│
├─ templates/ # Website html files
│
├─ tests/ # Unit tests
│
├─ .env 
├─ .gitignore
├─ faker_tool.py # Faker for sample data
├─ main.py # Main entry point
└─ requirements.txt
```
---

## 🔧 Setup Instructions

### 1️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 2️⃣ Run the Server
```
cd CareLog
python main.py
```
