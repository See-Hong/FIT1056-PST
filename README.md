<center><h1 align="center">🩺 CareLog — Nursing Home Management System</h1></center>


![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-green?logo=flask)
![HTML+CSS+JS](https://img.shields.io/badge/HTML+CSS+JS-Frontend-red?logo=html)
![License](https://img.shields.io/badge/License-Academic-orange)
![Status](https://img.shields.io/badge/Status-MVP_Complete-success)

> **Culturally Aware, Reflective, Empathetic Logging (CareLog)**  
> A **Flask-based web application** designed to streamline nursing home operations, focusing on patient well-being, empathetic care, and efficient staff collaboration.

![alt text](/FIT1056-PST/static/assets/display.png)
---

## 📖 Table of Contents
- [🌟 Overview](#-overview)
- [🚀 Key Features](#-key-features)
  - [👥 User & Role Management](#-1-user--role-management)
  - [🧬 Patient Profile Management](#-2-patient-profile-management)
  - [📝 Patient Log Tracking System](#-3-patient-log-tracking-system)
  - [🗓️ Appointment Scheduling System](#-4-appointment-scheduling-system)
  - [💬 Feedback Management System](#-5-feedback-management-system)
- [🔐 Security & Validation](#-security--validation)
- [🧰 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Setup & Installation](#️-setup--installation)
- [🧪 Testing](#-testing)
- [🧠 Design Principles](#-design-principles)
- [🧑‍⚕️ Contributors](#-contributors)
- [🧾 License](#-license)
- [📬 Contact](#-contact)

---

## 🌟 Overview
CareLog enables **secure, role-based management** of patient data, staff workflows, and medical records.  
Built with a **human-centred design philosophy**, it integrates cultural and emotional insights into clinical records to promote **empathetic healthcare** and improve **staff-patient communication**.

---

## 🚀 Key Features

### 👥 1. User & Role Management
- Four distinct user roles:
  - 👑 **Admin**
  - 🩺 **Doctor**
  - 💉 **Nurse**
  - 🧑‍⚕️ **Receptionist**
  - 👤 **Patient**
- **Admin Functions:**
  - View all user accounts
  - Update roles (excluding other Admins)
- **Security:**
  - Hashed passwords via `werkzeug.security`
  - Flask-Login authentication and session handling
  - Role-based access control for sensitive data
- **Profile Management:**
  - Editable details: Name, DOB, gender, contact info

---

### 🧬 2. Patient Profile Management
- Comprehensive **medical and cultural profile** per patient
- Includes:
  - Dietary and allergen information
  - Medical history and diagnoses
  - Cultural needs and personal preferences
  - Risk-level categorization
- Editable only by authorized medical staff

---

### 📝 3. Patient Log Tracking System
- Daily logs for each patient with:
  - Physical and emotional condition tracking
  - Notes and staff observations
  - Optional patient self-input for personal reflections
- Logs are **timestamped**, **editable by authorized users**, and securely stored in the database

---

### 🗓️ 4. Appointment Scheduling System
- Patients can request doctor appointments
- Appointment lifecycle:
- Doctors assigned automatically upon approval
- All appointment actions recorded for traceability

---

### 💬 5. Feedback Management System
- Integrated **Sheety API** for real-time feedback
- Features:
- Anonymous or identified submissions
- Ratings, feedback type, and comments
- **Admin Dashboard:** centralized feedback view and export

---

## 🔐 Security & Validation
| Aspect | Implementation |
|--------|----------------|
| Passwords | SHA-256 Hashing via `werkzeug.security` |
| Authentication | `Flask-Login` with role-based access control |
| Forms | `WTForms` validation |
| Sessions | Auto-logout after 10 minutes of inactivity |
| Database | SQLAlchemy ORM with secure schema |

---

## 🧰 Tech Stack
| Layer | Technology |
|-------|-------------|
| **Backend** | Flask |
| **ORM** | SQLAlchemy |
| **Authentication** | Flask-Login |
| **Forms** | Flask-WTF |
| **Frontend** | HTML + CSS + JS + Jinja2 + Bootstrap |
| **Database** | SQLite |

---
## 🧠 Design Principles

- **Empathy-Driven**: Captures cultural, emotional, and personal aspects of patient care

- **Security-First**: Strong password hashing, access control, and audit-ready logs

- **Scalable Architecture**: Modular Flask design with reusable blueprints

- **Maintainable Codebase**: Clear separation of concerns across app layers
---
## 🖥 Screenshots

![Home Page](/FIT1056-PST/static/assets/Homepage.png)
![Staff Page](/FIT1056-PST/static/assets/staff_dashboard.png)
![Admin Page](/FIT1056-PST/static/assets/admin_panel.png)
![Appointment Page](/FIT1056-PST/static/assets/Appointments.png)

---
## 📁 Project Structure
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

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/See-Hong/FIT1056-PST.git
cd FIT1056-PST
```

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Initialize the Database
```
python
>>> from app.models import db
>>> from main import app
>>> with app.app_context():
...     db.create_all()
```

### 4️⃣ Run the Server
```
python main.py
```

### 5️⃣ Access the App
  Visit: http://127.0.0.1:5000/

---
### 📬 Contact
For queries or feedback:  
Primary developor: `TEO SEE HONG`  
GitHUb: [Teo See Hong](https://github.com/See-Hong)  
Email: steo0033@student.monash.edu  
Secondary developor: `WONG KAI HENG`  
GitHub: [Wong Kai Heng](https://github.com/WongKH1010)  
Email: kwon0175@student.monash.edu  

---
### 🧾 License
Copyright © 2025 MA-Tue4-6-G02 (CareLog Team)  
Licensed under MIT.
