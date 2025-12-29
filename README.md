# 🕉️ Vedic-Book: Digital Priest Booking Platform

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=render)](https://vedic-book.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

> **Bridging Tradition with Technology.** > A full-stack web application designed to digitize the scheduling of the 16 Vedic Sanskars, making spiritual services accessible and organized.

---

## 🚀 Live Demo
**Check out the live application here:** 👉 **[https://vedic-book.onrender.com](https://vedic-book.onrender.com)**

---

## 📖 About The Project

Vedic-Book is a centralized platform that connects users with Vedic priests for traditional ceremonies. In an era where finding authentic spiritual guidance can be difficult, this platform simplifies the process with real-time availability checks and instant booking confirmations.

**Key Goals:**
* **Digitization:** preserving cultural heritage by providing detailed information on **16 Sanskars**.
* **Efficiency:** Automating the scheduling process to handle **100+ daily bookings**.
* **Accessibility:** Fully responsive design that works natively on iOS and Android devices.

---

## ✨ Key Features

### 👤 User Features
* **16 Sanskars Information:** Detailed educational cards for ceremonies like *Vivaha*, *Upanayana*, and *Antyeshti*.
* **Real-Time Availability:** Checks priest schedules instantly to prevent double bookings.
* **Smart Booking Form:** Captures essential details (Date, Time, Email, Phone) with validation.
* **Mobile-First Design:** Optimized UI with touch-friendly buttons and native app-like feel.

### 🛡️ Admin Features (Secure)
* **Dashboard:** Centralized view of all client bookings and priest statuses.
* **Session Authentication:** Protected `/admin` route requiring secure login.
* **Contact Management:** View client email and phone details for coordination.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Gunicorn
* **Database:** SQLAlchemy ORM, SQLite (Development)
* **Frontend:** HTML5, CSS3 (Responsive Grid), JavaScript (Fetch API)
* **Deployment:** Render (Cloud Hosting)

---

## 📸 Screenshots

| Home Page (Desktop) | Mobile View | Booking System |
|:---:|:---:|:---:|
| ![Home](https://via.placeholder.com/300x150?text=Home+Page) | ![Mobile](https://via.placeholder.com/150x300?text=Mobile+UI) | ![Booking](https://via.placeholder.com/300x150?text=Booking+Form) |

*(Note: Replace these placeholders with actual screenshots of your app for a better portfolio impact)*

---

## ⚙️ Local Installation & Setup

If you want to run this project locally on your machine:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Mriidul2508/Vedic-Book.git](https://github.com/Mriidul2508/Vedic-Book.git)
    cd Vedic-Book
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python app.py
    ```

5.  **Access the App**
    * Open your browser and go to: `http://127.0.0.1:5000`
    * To access Admin Panel: `http://127.0.0.1:5000/login`
    * **Default Credentials:**
        * Username: `admin`
        * Password: `admin123`

---

## 📂 Project Structure

```text
Vedic-Book/
├── app.py              # Main Flask Application & Routes
├── requirements.txt    # Python Dependencies
├── instance/           # SQLite Database
├── static/             # CSS, JS, and Images
│   ├── style.css       # Responsive Styling
│   ├── script.js       # Modal & API Logic
│   └── images/         # Sanskar Images & Icons
└── templates/          # HTML Templates
    ├── base.html       # Master Layout (Navbar/Footer)
    ├── index.html      # Homepage
    ├── book.html       # Booking Form
    ├── admin.html      # Dashboard
    └── login.html      # Admin Auth
