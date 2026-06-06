# 🏥 Hospital Management System — DS Hospital

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)

**A full-stack, role-based Hospital Management Web Application** built with Flask and Supabase, enabling patients, doctors, pharmacists, receptionists, and admins to manage clinical workflows from a single unified portal.

---

### 📖 READ THE USAGE OF BUTTONS AND WEBSITE BEFORE CLICKING ON THE LINK FOR EASIER UNDERSTANDING

[![Click Here to Open 👉](https://img.shields.io/badge/Click%20Here%20to%20Open%20👉-Live%20Demo-FF6B6B?style=for-the-badge)](https://ds-hospital.onrender.com)
&nbsp;
[![📁 Repository](https://img.shields.io/badge/📁-View%20Repository-4ECDC4?style=for-the-badge)](https://github.com/D-Sarkar-2508/Hospital-Management-System)

</div>

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Role-Based Access](#role-based-access)
6. [🔐 Landing Page & Authentication](#-landing-page--authentication)
7. [💊 Usage & Button Functionality — All Roles](#-usage--button-functionality--all-roles)
   - [🧑‍⚕️ Patient Dashboard](#-patient-dashboard)
   - [👨‍⚕️ Doctor Dashboard](#-doctor-dashboard)
   - [💊 Pharmacist Dashboard](#-pharmacist-dashboard)
   - [📋 Receptionist Dashboard](#-receptionist-dashboard)
   - [🛡️ Admin Dashboard](#-admin-dashboard)
8. [Local Setup](#local-setup)
9. [Deployment](#deployment)
10. [Conclusion](#conclusion)

---

## Overview

**DS Hospital** is a sleek, responsive, and modern web application designed to streamline healthcare administration. It provides an intuitive, dark-themed interface for managing member profiles, tracking clinical data, scheduling appointments, handling OT requests, booking lab tests, and maintaining crucial health records — all in one place.

The platform uses **role-based authentication**, meaning every user type sees a completely different dashboard and set of actions tailored to their responsibilities.

---

## Features

- **Role-Based Access Control** — Five distinct roles: Patient, Doctor, Pharmacist, Receptionist, and Admin, each with a dedicated portal and permissions.
- **Comprehensive Records Management** — Track detailed member information including age, qualifications, and core medical details.
- **Dynamic Medical Tracking** — Real-time visibility into active health issues and specific blood groups for rapid clinical reference.
- **Appointment & OT Management** — Patients can book appointments; receptionists confirm them; OT requests flow between roles.
- **Lab Test & Report Workflow** — Patients request tests; pharmacists manage bookings, upload reports, and maintain the daily lab schedule.
- **Modern UI Design** — Clean, dark-themed container layout with a consistent blue-teal colour palette and interactive card-style components.
- **Fully Responsive** — Optimally styled to deliver a fluid experience across desktop monitors, tablets, and mobile smartphones.
- **Secure Registration & Login** — Input validation enforced on both client and server sides; email format rules and minimum password complexity applied.

---

## Tech Stack

| Layer            | Technology                                        |
|------------------|---------------------------------------------------|
| Backend          | Python (Flask 3.0)                                |
| Database         | Supabase (PostgreSQL)                             |
| Frontend         | HTML5, CSS3 (Modern Dark Theme Palette), Vanilla JavaScript |
| Containerisation | Docker                                            |
| Deployment       | Render                                            |
| Version Control  | Git & GitHub                                      |

---

## Project Structure

```
.
├── app.py                  # Flask application logic, routing & Supabase integration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container configuration for Render deployment
├── .gitignore
├── static/
│   ├── css/
│   │   └── style.css       # Modern dark-themed global styling & layout
│   └── js/
│       └── main.js         # Client-side dynamic handling & interactions
└── templates/
    └── index.html          # Main application dashboard interface (Jinja2 templated)
```

---

## Role-Based Access

DS Hospital supports **five user roles**, each with its own portal, visual dashboard, and set of permitted actions:

| Role         | Icon | Access Scope                                                         |
|--------------|------|----------------------------------------------------------------------|
| Patient      | 🧑‍⚕️   | Own health records, book tests, view appointments, request OT        |
| Doctor       | 👨‍⚕️   | View assigned patients, update credentials, manage clinical records  |
| Pharmacist   | 💊   | Manage test bookings, upload lab reports, view daily lab schedule    |
| Receptionist | 📋   | Confirm appointments, handle OT requests                             |
| Admin        | 🛡️   | Full hospital management, staff administration, all records          |

---

## 🔐 Landing Page & Authentication

### What You See on First Visit (`/`)

When you open `https://ds-hospital.onrender.com`, you land on the **DS Hospital Portal Home Page**. This page contains:

- A centered **hospital logo/icon** (⚕) and the heading **"DS Hospital — Hospital Management System"**.
- A subtitle: *"Welcome to Hospital Portal — Please select your role to continue."*
- **Five role selection cards**, each displaying an icon, role name, and brief description of what that role can do:

| Card         | Description shown                                              |
|--------------|----------------------------------------------------------------|
| 🧑‍⚕️ Patient    | Access your health records, book tests, appointments and OT   |
| 👨‍⚕️ Doctor     | View your patients, update credentials and manage records      |
| 💊 Pharmacist  | Manage test bookings, reports and daily lab schedule           |
| 📋 Receptionist| Handle OT requests and appointment confirmations              |
| 🛡️ Admin       | Full hospital management and staff administration              |

---

### Authentication Modal (Login / Register)

**Trigger:** Clicking any role card opens a centred **modal overlay** with two tabs: **Login** and **Register**.

#### Login Tab

| Field / Button          | What it does                                                                                                                          |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **Email or Contact Number** field | Text input. Accepts the user's registered email address or 10-digit contact number.                                      |
| **Password** field      | Masked text input. Accepts the user's password.                                                                                      |
| **Login** button        | Validates that both fields are non-empty on the client side, then sends credentials to Flask. Flask queries Supabase to verify the user. If credentials match the selected role, the user is redirected to their dashboard. If invalid, an error message appears within the modal. |
| **✕ (Close)** button    | Dismisses the modal without any action and returns to the role selection page.                                                       |
| **"Register"** tab/link | Switches the modal view to the Registration form.                                                                                    |

#### Register Tab

| Field / Button              | Validation rules & what it does                                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **Full Name** field *       | Required. Accepts alphabetical characters and spaces.                                                                            |
| **Address** field           | Optional. Free-text address field.                                                                                                |
| **Contact Number** field *  | Required. Must be exactly 10 digits; non-numeric characters are rejected.                                                        |
| **Date of Birth** field *   | Required. Date picker input.                                                                                                     |
| **Email** field *           | Required. Must be a `@gmail.com` address, all lowercase only. Any other domain or uppercase letters are rejected.                |
| **Password** field *        | Required. Minimum 8 characters, must include a mix of letters, digits, and at least one special character.                       |
| **Register** button         | Validates all fields client-side first. On passing, sends a POST request to Flask, which inserts a new user row into Supabase with the role inherited from the card that was clicked. On success, the user is auto-logged in and redirected to their role dashboard. On failure (e.g. duplicate email), an inline error message is shown. |
| **"Login"** tab/link        | Switches back to the Login form.                                                                                                  |

---

## 💊 Usage & Button Functionality — All Roles

---

### 🧑‍⚕️ Patient Dashboard

> **Route:** `/patient/dashboard`  
> **Who sees this:** Any user registered/logged in with the **Patient** role.

#### What is visible on this dashboard:

The dashboard displays the patient's **personal profile card** at the top with their name, contact info, date of birth, email, and address. Below it are three main functional panels:

1. **My Health Records** — Displays the patient's existing medical records (conditions, blood group, notes added by doctors).
2. **My Appointments** — Lists all upcoming and past appointments with their status (Pending / Confirmed / Cancelled).
3. **My Test Bookings** — Shows all lab tests booked, their status, and any uploaded reports.
4. **My OT Requests** — Shows Operation Theatre requests and their current status.

#### Buttons & their functions:

| Button / Element                   | When it appears                          | What it does                                                                                                           |
|------------------------------------|------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Book Appointment** button        | Always visible in the Appointments panel | Opens a modal form to fill in: preferred date, preferred time, and reason for visit. Submits a POST request to Flask to create a new appointment row in Supabase with status = "Pending". The new appointment immediately appears in the list. |
| **Cancel Appointment** button      | Next to each Pending appointment         | Triggers a confirmation prompt ("Are you sure you want to cancel?"). On confirmation, sends a DELETE/UPDATE request to Flask; the appointment status changes to "Cancelled" and the card updates visually in real time. |
| **Book Lab Test** button           | Always visible in the Test Bookings panel| Opens a modal form to select test type and preferred date. On submission, creates a new test booking row in Supabase with status = "Pending". The booking appears in the test list immediately. |
| **View Report** button             | Appears next to a test once report is uploaded by Pharmacist | Opens the uploaded lab report (PDF or image) in a new browser tab for the patient to view or download. |
| **Request OT** button              | Always visible in the OT Requests panel  | Opens a form to fill in: procedure name, preferred date, and notes. Submits to Flask; creates an OT request row in Supabase with status = "Pending". Receptionist must then confirm it. |
| **Logout** button (top-right/nav)  | Always visible                           | Clears the session cookie and redirects to the Landing Page (role selection).                                         |

---

### 👨‍⚕️ Doctor Dashboard

> **Route:** `/doctor/dashboard`  
> **Who sees this:** Any user registered/logged in with the **Doctor** role.

#### What is visible on this dashboard:

The dashboard shows the doctor's **own profile card** (name, specialisation, contact) and two main panels:

1. **My Patients** — A list of all patients assigned to this doctor, with their basic info cards.
2. **My Credentials / Profile** — The doctor's qualifications, department, and contact info, which they can update.

#### Buttons & their functions:

| Button / Element                        | When it appears                                | What it does                                                                                                                             |
|-----------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| **View Patient Details** button         | On each patient card in the "My Patients" list | Expands or opens a detail modal showing: patient's full name, age, blood group, active health issues, past records, and contact number.   |
| **Add Medical Record** button           | Inside the expanded patient detail view        | Opens an inline form with fields for: Diagnosis / Condition, Notes, Date. On submission, sends a POST request to Flask which inserts a new medical record row linked to that patient in Supabase. The record appears immediately in the patient's history. |
| **Edit Medical Record** button (✏️)     | Next to each existing record in the patient view| Opens the record's fields in an editable inline form pre-filled with existing data. On "Save", sends a PATCH/PUT request to Flask and updates the record in Supabase in real time. |
| **Delete Medical Record** button (🗑️)  | Next to each existing record in the patient view| Triggers a confirmation alert. On confirm, sends a DELETE request to Flask; the record is removed from Supabase and disappears from the UI instantly. |
| **Update My Credentials** button        | In the "My Credentials" panel                  | Opens an editable form pre-filled with the doctor's current qualifications, department, and contact info. On "Save Changes", sends a PATCH request to Flask and updates the doctor's row in Supabase. |
| **Logout** button                       | Always visible in navigation                   | Ends the session and redirects to the Landing Page.                                                                                      |

---

### 💊 Pharmacist Dashboard

> **Route:** `/pharmacist/dashboard`  
> **Who sees this:** Any user registered/logged in with the **Pharmacist** role.

#### What is visible on this dashboard:

The pharmacist sees three main panels:

1. **Pending Test Bookings** — All lab test requests from patients that are yet to be processed.
2. **Daily Lab Schedule** — A calendar/list view of all tests scheduled for today.
3. **Completed Reports** — Tests for which reports have already been uploaded.

#### Buttons & their functions:

| Button / Element                      | When it appears                                    | What it does                                                                                                                           |
|---------------------------------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| **Accept Booking** button             | Next to each Pending test booking                  | Confirms the test booking; updates its status to "Accepted/Scheduled" in Supabase. The booking moves from the Pending list to the Daily Lab Schedule panel. |
| **Reject Booking** button             | Next to each Pending test booking                  | Triggers a confirmation prompt. On confirm, updates the booking status to "Rejected" in Supabase. The record is removed from the Pending list. |
| **Upload Report** button              | On each Accepted/Scheduled test booking            | Opens a file upload modal. The pharmacist selects a report file (PDF or image). On submission, the file is stored and the report link is saved to Supabase. The booking status changes to "Report Ready". The patient can now see a "View Report" button on their end. |
| **View Schedule** / **Today's Tests** toggle | At the top of the Daily Lab Schedule panel  | Filters the test list to show only today's tests or the full upcoming schedule depending on the toggle state.                          |
| **Logout** button                     | Always visible in navigation                       | Ends the session and redirects to the Landing Page.                                                                                    |

---

### 📋 Receptionist Dashboard

> **Route:** `/receptionist/dashboard`  
> **Who sees this:** Any user registered/logged in with the **Receptionist** role.

#### What is visible on this dashboard:

The receptionist sees two main panels:

1. **Pending Appointments** — All appointment requests from patients awaiting confirmation.
2. **Pending OT Requests** — All Operation Theatre requests from patients awaiting confirmation.

#### Buttons & their functions:

| Button / Element                    | When it appears                                  | What it does                                                                                                                                 |
|-------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Confirm Appointment** button      | Next to each Pending appointment                 | Updates the appointment's status from "Pending" to "Confirmed" in Supabase. The patient sees the status change to "Confirmed" on their dashboard. The appointment card moves out of the pending list. |
| **Cancel Appointment** button       | Next to each Pending appointment                 | Triggers a confirmation prompt. On confirm, updates the appointment status to "Cancelled" in Supabase. Both the receptionist's and the patient's dashboards reflect this change. |
| **Confirm OT Request** button       | Next to each Pending OT request                  | Updates the OT request status to "Confirmed" in Supabase. The patient sees the update immediately on their OT Requests panel.               |
| **Reject OT Request** button        | Next to each Pending OT request                  | Triggers a confirmation prompt. On confirm, sets the OT request status to "Rejected" in Supabase.                                           |
| **Logout** button                   | Always visible in navigation                     | Ends the session and redirects to the Landing Page.                                                                                          |

---

### 🛡️ Admin Dashboard

> **Route:** `/admin/dashboard`  
> **Who sees this:** Any user registered/logged in with the **Admin** role.

#### What is visible on this dashboard:

The admin has the most comprehensive view, with access to all data in the system:

1. **All Members / Staff** — A full grid of every registered user (patients, doctors, pharmacists, receptionists) displayed as profile cards.
2. **All Appointments** — A master list of every appointment in the system, across all patients.
3. **All Records** — Every medical record logged in the system.
4. **System Stats** — High-level counts (total patients, total appointments, pending items, etc.).

#### Buttons & their functions:

| Button / Element                        | When it appears                                          | What it does                                                                                                                                     |
|-----------------------------------------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **+ Add Record** button                 | Always visible at the top of the Members/Records panels  | Opens a centred modal overlay with blank input fields (Name, Role, Contact, Email, etc.). Resets any previously entered data. Ready to accept new entries. |
| **Submit / Save** button (inside modal) | Inside the Add Record / Edit form modal                  | Validates all input fields on the client side. On passing, compiles a JSON object and sends a POST request to Flask, which registers a new row in the appropriate Supabase table. The new card/record appears on the dashboard instantly without a page reload. |
| **Edit** button (✏️)                   | On every member/record card                              | Opens the same modal overlay pre-populated with that record's existing data. All fields are editable. On "Save", sends a PATCH request to Flask to update the row in Supabase. |
| **Delete** button (🗑️)                | On every member/record card                              | Triggers a browser confirmation alert prompt. On confirm, sends a DELETE request to Flask, which removes the record from Supabase. The card element is then stripped from the dashboard grid by client-side JavaScript — no page reload required. |
| **View All Appointments** button        | In the Appointments overview panel                       | Expands the appointments list to show all records (past, current, upcoming) for every patient in the system.                                     |
| **Manage Roles** / **Assign Role** (if present) | On a user card                                | Allows the admin to change a user's system role (e.g. from Patient to Doctor) by updating the `role` field in Supabase.                          |
| **Logout** button                       | Always visible in navigation                             | Ends the admin session and redirects to the Landing Page.                                                                                        |

---

## Local Setup

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project with the required tables
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/D-Sarkar-2508/Hospital-Management-System.git
cd Hospital-Management-System

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
# Create a .env file with your Supabase credentials:
# SUPABASE_URL=your_supabase_project_url
# SUPABASE_KEY=your_supabase_anon_key
# SECRET_KEY=your_flask_secret_key

# 5. Run the application
python app.py
```

Open your browser and navigate to `http://localhost:5000`.

---

## Deployment

The application is containerised using **Docker** and deployed on **[Render](https://render.com)**.

**Live URL:** [https://ds-hospital.onrender.com](https://ds-hospital.onrender.com)

> ⚠️ **Note:** The application is hosted on Render's free tier. The server may spin down after periods of inactivity. The first request after a cold start may take 30–60 seconds to respond.

### Docker

```bash
# Build the image
docker build -t ds-hospital .

# Run the container
docker run -p 5000:5000 ds-hospital
```

---

## Conclusion

The **DS Hospital Management System** successfully coordinates a high-performance Flask backend with a reactive, role-aware frontend. By coupling **Flask with Supabase**, the application delivers secure, atomic CRUD operations over healthcare datasets with sub-second delivery.

The fluid, role-based single-page dashboard layout drastically lowers administrative friction — giving patients, doctors, pharmacists, receptionists, and admins exactly the tools they need, nothing more, nothing less. It acts as an optimal framework for expanding scalable health-tech records infrastructure.

---

<div align="center">

**Designed with focus on Healthcare Efficiency 🏥**

*If this repository assisted your workflow, feel free to give it a ⭐*

**Author:** [Ditipriya Sarkar](https://github.com/D-Sarkar-2508)

</div>
