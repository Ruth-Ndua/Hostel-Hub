### 🏠 HostelHub – Grace Apartments Management System

HostelHub is a simple web-based hostel management system built with Django for managing one specific hostel: Grace Apartments.

This system helps the landlord/caretaker manage tenants, rooms, payments, maintenance requests, and announcements — while tenants can view their room details, submit rent payments, and report maintenance issues.

No Airbnb madness. No multi-hostel chaos.
One hostel. One system. Clean and intentional.

### 🎯 Project Purpose

Grace Apartments previously relied on WhatsApp messages, paper records, and verbal communication, which led to:

Lost payment confirmations

Missed maintenance requests

Repeated tenant questions

Poor tracking of vacant rooms and unpaid rent

HostelHub centralizes all this into one place.

## 👥 User Roles
1️⃣ Visitors (Not logged in)

View hostel details

See available rooms

Get caretaker contact information

2️⃣ Tenants

Log in to their dashboard

View room and rent status

Submit rent payments (M-Pesa code)

Report maintenance issues

View announcements from management

3️⃣ Admin (Caretaker / Landlord)

View hostel overview

Manage rooms and tenants

Approve rent payments

View and resolve maintenance issues

Post announcements

### ⚙️ Features Implemented
## 🏠 General

Landing page for Grace Apartments

Available rooms page

# 👤 Tenant Features

Tenant dashboard

Rent payment submission

Maintenance request form

Announcements view

# 🛠 Admin Features

Admin dashboard overview

Room management

Tenant management

Maintenance management

Payment approval workflow

Announcements posting

### 🧠 Why a Website and Not WhatsApp?

Short answer for panelists:
WhatsApp is communication. HostelHub is management.

Long answer (still sane):

WhatsApp messages get buried

No rent tracking

No proof history

No maintenance status

No structured data

This system:

Keeps records

Improves accountability

Reduces repeated questions

Scales better as tenants increase

### 🌍 SDG Alignment
## ✅ SDG 11 – Sustainable Cities and Communities

HostelHub promotes:

Better housing management

Improved living conditions

Efficient resource use

Digital record keeping

It directly supports safer, more organized urban housing systems.

### 🛠 Technologies Used

Python

Django

HTML & CSS

### SQLite (default Django DB)

No JavaScript frameworks.
No unnecessary complexity.
Beginner-friendly by design.

### 📁 Project Structure (Simplified)
myproject/
│
├── myapp/
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── sign_up.html
│   │   ├── tenant_dashboard.html
│   │   ├── payments.html
│   │   ├── maintenance.html
│   │   ├── admin_dashboard.html
│   │   └── ...
│   │
│   ├── static/
│   │   ├── styles.css
│   │   └── hostel.jpg
│   │
│   ├── views.py
│   ├── models.py
│   └── urls.py
│
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── manage.py

### ▶️ How to Run the Project
## Requirements

Python 3.10+

Django installed

Virtual environment (recommended)

### Steps
# clone or download project
cd myproject

# activate virtual environment (if used)
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# run migrations
python manage.py migrate

# start server
python manage.py runserver


Then open your browser and visit:

http://127.0.0.1:8000/

### 🧪 Dummy Data

This project uses sample data displayed in templates for demonstration:

Sample rooms

Sample tenants

Sample payments and announcements

This keeps the project simple and beginner-friendly while still realistic.

### 🚧 Limitations (Yes, we own them)

Single-hostel system (by design)

No real M-Pesa API integration

Authentication simplified for learning purposes

These can be improved in future versions.

### 📌 Conclusion

HostelHub is a practical, beginner-friendly Django project that solves a real-world housing management problem for a single hostel.

It focuses on:

Simplicity

Real use cases

Clear user roles

Clean separation of responsibilities
