# 🏥 Hospital Management System (CLI-Based)

A **Python + MySQL based Hospital Management System** built during **12th grade**, focused on understanding database design, role-based access, and menu-driven programs.  
This is a **terminal-based application** and was created for learning purposes.

---

## 📌 Overview

This project simulates basic hospital operations such as:
- Patient registration
- Doctor management
- Appointment handling
- Billing system
- Admin control

It uses **MySQL** as the backend database and a **menu-driven CLI** interface written in Python.

---

## 🧩 User Roles

### 👑 Admin
- Manage admin accounts
- Add / edit / delete doctors
- Add / edit / delete users (patients)
- Manage bill items
- Reset doctor and billing data

### 🧑‍⚕️ Doctor
- Login securely
- View and update profile
- Accept or reject appointments
- Manage assigned patients
- Update bills and discharge patients
- Send notifications to patients

### 🧑‍💼 Patient (User)
- Create account
- Login and update profile
- Request appointments with doctors
- View notifications
- View and print bill
- Delete account

---

## 🗄 Database Design

- `admin_login`
- `doctor_login`
- `user_login`
- `doctor_list`
- `patient_list`
- `bill_list`
- Dynamic tables:
  - `<doctor_id>_patient_list`
  - `<doctor_id>_appointment_request`
  - `<patient_id>_bill`

All tables are created automatically at runtime if they do not exist.

---

## ⚙️ Features

- 🔐 Role-based authentication
- 📋 Menu-driven CLI interface
- 🧠 Dynamic table creation per doctor/patient
- 🧾 Billing system with itemized costs
- 🔔 Patient notification system
- 🕒 Activity logging with timestamps
- 🛠 Admin-level full system control

---

## 🛠 Tech Stack

- 🐍 Python
- 🗄 MySQL
- 📊 tabulate (for table display)
- ⏱ time & datetime modules

---

## 🚀 How to Run

1. Install MySQL and start the MySQL server
2. Install required Python modules:
   ```bash
   pip install mysql-connector-python tabulate

Update MySQL credentials in the code:
host='localhost'
user='root'
password='your_password'


Run the program: python main.py


⚠️ Limitations

-CLI-based (no GUI)
-Plain-text password storage
-No input sanitization (SQL injection possible)
-Monolithic script structure
-Not production-ready
