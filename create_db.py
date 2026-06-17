import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("railway.db")
cursor = conn.cursor()

# ==========================
# USERS TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    gender TEXT,
    dob TEXT,
    address TEXT
)
""")

# ==========================
# ADMINS TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# ==========================
# TRAINS TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS trains(
    train_id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL
)
""")

# ==========================
# BOOKINGS TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pnr TEXT,
    user_id INTEGER,
    train_id INTEGER,
    passenger_name TEXT,
    age INTEGER,
    gender TEXT,
    seats_booked INTEGER,
    booking_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(train_id) REFERENCES trains(train_id)
)
""")

# ==========================
# INSERT DEFAULT ADMIN
# ==========================

cursor.execute(
    "SELECT * FROM admins WHERE username=?",
    ("admin",)
)

admin = cursor.fetchone()

if admin is None:

    hashed_password = generate_password_hash("admin123")

    cursor.execute(
        """
        INSERT INTO admins(username,password)
        VALUES(?,?)
        """,
        (
            "admin",
            hashed_password
        )
    )

# ==========================
# INSERT SAMPLE TRAINS
# ==========================

cursor.execute("SELECT COUNT(*) FROM trains")

count = cursor.fetchone()[0]

if count == 0:

    trains = [

        ("Godavari Express","Hyderabad","Visakhapatnam","17:15","05:30",500,500),

        ("Charminar Express","Hyderabad","Chennai","18:00","08:15",450,450),

        ("Falaknuma Express","Hyderabad","Bengaluru","21:30","07:00",400,400),

        ("Rajdhani Express","Delhi","Mumbai","16:00","08:00",700,700),

        ("Duronto Express","Delhi","Hyderabad","20:00","10:30",600,600),

        ("Shatabdi Express","Hyderabad","Vijayawada","06:00","10:00",300,300),

        ("Vande Bharat Express","Secunderabad","Visakhapatnam","05:45","14:30",550,550),

        ("AP Express","Hyderabad","New Delhi","18:50","20:45",650,650),

        ("Garib Rath","Hyderabad","Delhi","19:00","21:00",700,700),

        ("Konark Express","Mumbai","Bhubaneswar","15:20","17:00",650,650),

        ("Sampark Kranti","Delhi","Bengaluru","08:00","18:00",600,600),

        ("Jan Shatabdi","Hyderabad","Warangal","07:15","10:00",300,300),

        ("Intercity Express","Vijayawada","Visakhapatnam","09:00","14:00",450,450),

        ("Telangana Express","Hyderabad","New Delhi","18:00","20:15",650,650),

        ("East Coast Express","Hyderabad","Bhubaneswar","16:45","09:30",550,550)

    ]

    cursor.executemany(
        """
        INSERT INTO trains(
            train_name,
            source,
            destination,
            departure_time,
            arrival_time,
            total_seats,
            available_seats
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        trains
    )

conn.commit()
conn.close()

print("========================================")
print("Database created successfully!")
print("Admin Username : admin")
print("Admin Password : admin123")
print("Sample trains inserted successfully!")
print("========================================")