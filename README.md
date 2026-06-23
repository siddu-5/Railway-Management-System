#  Railway Management System
A modern **Railway Management System** developed using **Flask**, **SQLite**, **HTML**, **CSS**, and **Bootstrap**. The application provides a complete railway ticket booking experience with secure user authentication, train management, ticket booking, PDF ticket generation, and an admin dashboard.

## Live Demo
https://railway-management-system-lf1i.onrender.com

---
## Features
### User Module
- User Registration
- Secure Login (Password Hashing)
- Dashboard
- Search Available Trains
- Book Train Tickets
- Automatic PNR Generation
- Seat Availability Management
- View My Bookings
- Cancel Bookings
- Download PDF E-Ticket
- User Profile Management
- Edit Profile
- Logout
---
### Admin Module
- Admin Login
- Dashboard
- View Statistics
- Add New Train
- Edit Train Details
- Delete Train
- Manage Available Trains
---
## Technologies Used

| Technology | Purpose |
|------------|---------|
| Flask | Backend Framework |
| SQLite | Database |
| HTML5 | Frontend Structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| Python | Backend Programming |
| ReportLab | PDF Ticket Generation |
| Werkzeug | Password Hashing |

---
## Project Structure
```
Railway-Management-System/
│
├── app.py
├── create_db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   └── db.py
│
├── static/
│   ├── css/
│   ├── images/
│   └── favicon.ico
│
├── templates/
│
├── railway.db
│
└── venv/
```
---
## Installation
### 1.Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Railway-Management-System.git
```
---
### 2.Navigate to Project
```bash
cd Railway-Management-System
```
---
### 3.Create Virtual Environment

```bash
python -m venv venv
```
---
### 4.Activate Virtual Environment
**Windows**
```bash
venv\Scripts\activate
```
**Linux / macOS**
```bash
source venv/bin/activate
```
---
### 5.Install Dependencies
```bash
pip install -r requirements.txt
```
---
### 6.Run the Application
```bash
python app.py
```
---
Open your browser and visit
```
http://127.0.0.1:5000
```
---
## Default Admin Credentials
Username
```
admin
```
Password
```
admin123
```
---
## Application Screenshots
### Home Page
<img width="1917" height="971" alt="Screenshot 2026-06-17 185607" src="https://github.com/user-attachments/assets/074443b7-0f65-4f57-bd79-bc74dc8e1064" />

---

### Login Page
<img width="1917" height="963" alt="Screenshot 2026-06-17 185708" src="https://github.com/user-attachments/assets/48bfc784-6c7c-44bc-b232-bb37e9ea3737" />

---

### User Dashboard
<img width="1918" height="963" alt="Screenshot 2026-06-17 185749" src="https://github.com/user-attachments/assets/0edacac9-d698-4ccd-b4ae-c708f429249e" />

---

### Search Trains
<img width="1918" height="533" alt="Screenshot 2026-06-17 185830" src="https://github.com/user-attachments/assets/fb43ec3c-16d0-40f5-87a9-c8a5fc267017" />

---

###  Book Ticket
<img width="1918" height="867" alt="Screenshot 2026-06-17 185944" src="https://github.com/user-attachments/assets/df5d2fa2-a6d7-4768-8888-974400c4357e" />

---

###  PDF Ticket
<img width="877" height="497" alt="Screenshot 2026-06-17 190039" src="https://github.com/user-attachments/assets/c64dc1ab-b702-4be3-a492-cc3e44dafd84" />

---

###  Admin Dashboard
<img width="1918" height="968" alt="Screenshot 2026-06-17 190147" src="https://github.com/user-attachments/assets/395a7e2c-308d-42f5-979b-d5df1e698f1f" />

---

###  Manage Trains
<img width="1201" height="952" alt="Screenshot 2026-06-17 190231" src="https://github.com/user-attachments/assets/d3268faa-0c8c-48fa-8656-7239cbc5e4c0" />

---

##  Database Tables

- Users
- Admins
- Trains
- Bookings

---

## Security Features

- Password Hashing using Werkzeug
- Session Management
- Authentication
- Admin Authorization
- SQL Parameterized Queries

---

##  Key Functionalities

- User Authentication
- Train Search
- Ticket Booking
- Seat Availability Management
- PNR Generation
- Booking Cancellation
- PDF Ticket Download
- Train CRUD Operations
- Admin Dashboard

---

##  Future Improvements

- Online Payment Gateway
- Email Ticket Confirmation
- SMS Notifications
- Live Train Status
- Train Delay Prediction
- QR Code E-Ticket
- Passenger Seat Selection
- Forgot Password
- OTP Verification

---

##  If you like this project

Give this repository a ⭐ on GitHub.

---

## License
This project is developed for educational and portfolio purposes.
