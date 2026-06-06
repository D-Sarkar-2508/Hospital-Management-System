# 🏥 Hospital Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white" alt="Render">
  

A sleek, responsive, and modern web application designed to streamline healthcare administration. This platform provides an intuitive interface for managing member profiles, tracking clinical data, and maintaining crucial health records efficiently.

---

### 📖 READ THE USAGE OF BUTTONS AND WEBSITE BEFORE CLICKING ON THE LINK FOR EASIER UNDERSTANDING
 
[![Click Here to Open 👉](https://img.shields.io/badge/Click%20Here%20to%20Open%20👉-Live%20Demo-FF6B6B?style=for-the-badge)](https://ds-hospital.onrender.com)
&nbsp;
[![📁 Repository](https://img.shields.io/badge/📁-View%20Repository-4ECDC4?style=for-the-badge)](https://github.com/D-Sarkar-2508/Hospital-Management-System)
 
</div>

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [💡 Usage & Button Functionality](#-usage--button-functionality)
- [🎯 Conclusion](#-conclusion)

---

## ✨ Features

- **Comprehensive Records Management:** Easily track detailed member information, including age, qualifications, and core medical details.
- **Dynamic Medical Tracking:** Real-time visibility into active health issues and specific blood groups for rapid clinical reference.
- **Modern UI Design:** Crafted with a clean, modern dark-themed container layout featuring a consistent blue-teal color palette and interactive card-style buttons.
- **Fully Responsive:** Optimally styled to deliver a fluid experience across desktop monitors, tablets, and mobile smartphones.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python (Flask) |
| **Database** | Supabase (PostgreSQL) |
| **Frontend** | HTML5, CSS3 (Modern Dark Theme Palette), Vanilla JavaScript |
| **Deployment** | Render |
| **Version Control** | Git & GitHub |

---
---

## 💡 Usage & Button Functionality

This single-page administrative panel lets you orchestrate full database lifecycle actions interactively. The tables below map out exactly what each visual interface element does on a click-by-click basis.

### ⚙️ Main Dashboard Control Elements

| Dashboard Button | UI Interaction / Trigger | System Backend Functionality |
| :--- | :--- | :--- |
| **`+ Add Record`** | Opens a centered modal overlay window. | Resets internal state keys and displays clear text input fields ready to accept new data strings. |
| **`Submit` / `Save`** *(Inside form)* | Validates input structures on the client side. | Compiles parameters into a JSON object, makes a POST request to Flask, and registers a new row in **Supabase**. |

---

### 🗂️ Core Profile Card Parameter Fields

Every registered profile card visually presents four explicit database parameters captured via the system:

| Data Field Indicator | Captured Parameter | Real-World Administrative Purpose |
| :--- | :--- | :--- |
| 🔢 **Age** | Numerical individual age. | Provides instant age tracking for record verification. |
| 🎓 **Degree** | Educational credentials / qualifications. | Documents professional backgrounds or academic status. |
| 🩺 **Health Issue** | Dynamic active medical condition string. | Instantly flags critical active cases or symptoms needing immediate attention. |
| 🩸 **Blood Group** | Validated clinical blood type. | Offers a high-visibility indicator for priority matching during emergencies. |

---

### ⚡ Individual Profile Action Triggers

| Action Link / Button | Client Interface State Trigger | System Backend Functionality |
| :--- | :--- | :--- |
| **`👁️ View Details`** | Launches a read-only floating modal window. | Pulls cached attributes from the client-side state machine to show extensive history records safely. |
| **`✏️ Edit Record`** | Opens an editable operational modal view. | Targets the card's unique database index row and pre-fills the input forms with its current text values. |
| **`Update`** *(Inside form)* | Closes the editing modal automatically. | Dispatches an asynchronous request to Flask, executing an atomic write update across the **Supabase** dataset. |
| **`🗑️ Delete`** | Displays a secondary confirmation alert prompt. | Drops the specified record key out of **Supabase**, then uses JavaScript to seamlessly strip the HTML element from the dashboard grid. |

---
## 🎯 Conclusion

In summary, the **Hospital Management System** successfully coordinates a high-performance backend with a highly reactive user experience. By coupling **Flask** with **Supabase**, the application delivers secure, atomic CRUD operations over healthcare datasets with sub-second delivery states. 

The fluid, unified single-page dashboard layout drastically lowers administrative friction, offering clinical environments an efficient data tracking module that is robust, visually engaging, and completely scale-ready. It acts as an optimal framework for expanding scalable health-tech records infrastructure.

<p align="center">
  <b>Designed with focus on Healthcare Efficiency 🏥</b><br>
  If this repository assisted your workflow, feel free to give it a ⭐
</p>
## 📁 Project Structure

```text
.
├── app.py                  # Flask Application logic & routing
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Modern dark-themed styling & layout
│   └── js/
│       └── main.js         # Client-side dynamic handling & interactions
└── templates/
    └── index.html          # Main application dashboard interface
