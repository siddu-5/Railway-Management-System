from flask import Flask,render_template,request,session,redirect,flash,send_file
from database.db import get_db_connection
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime
import random
from reportlab.pdfgen import canvas

app=Flask(__name__)
app.secret_key="railway_secret_key"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        existing=cursor.fetchone()
        if existing:
            flash("Email already registered","warning")
            cursor.close()
            conn.close()
            return redirect('/register')
        hashed_password=generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users(name,email,password)
            VALUES(%s,%s,%s)
            """,
            (name,email,hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration Successful!","success")
        return redirect('/login')
    return render_template('register.html')

from werkzeug.security import check_password_hash

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user=cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user['password'],password):
            session['user_id']=user['user_id']
            session['name']=user['name']
            flash("Login Successful","success")
            return redirect('/dashboard')
        flash("Invalid Email or Password","danger")
        return redirect('/login')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect("/login")
    return render_template(
        "dashboard.html",
        name=session["name"]
    )
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route('/search',methods=["GET","POST"])
def search_train():
    if request.method=="POST":
        source=request.form['source']
        destination=request.form['destination']
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        
        query="select * from trains where lower(source)=lower(%s) and lower(destination)=lower(%s)"
        cursor.execute(query,(source,destination))
        
        trains=cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template("train_results.html",trains=trains)
    return render_template("search_train.html")

@app.route("/book/<int:train_id>",methods=['GET','POST'])
def book_ticket(train_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select *from trains where train_id=%s",(train_id,))
    train=cursor.fetchone()
    if request.method=="POST":
        passenger_name=request.form['passenger_name']
        age=request.form['age']
        gender=request.form['gender']
        seats=int(request.form['seats'])
        if seats>train['available_seats']:
            return "Not enough seats available"
        pnr="PNR"+str(random.randint(100000,999999))
        cursor.execute("""INSERT INTO bookings(pnr,user_id,train_id,passenger_name,age,gender,seats_booked,booking_date)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",(pnr,session['user_id'],train_id,passenger_name,age,gender,seats,datetime.now()))
        booking_id=cursor.lastrowid
        cursor.execute("UPDATE trains SET available_seats=available_seats-%s WHERE train_id=%s",(seats, train_id))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("booking_success.html",pnr=pnr,booking_id=booking_id)
    cursor.close()
    conn.close()
    return render_template("book_ticket.html",train=train)

@app.route('/my_bookings')
def my_bookings():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    query="""
    SELECT b.*, t.train_name
    FROM bookings b
    JOIN trains t
    ON b.train_id = t.train_id
    WHERE b.user_id = %s
    """

    cursor.execute(
        query,
        (session['user_id'],)
    )

    bookings=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'my_bookings.html',
        bookings=bookings
    )
    
@app.route('/admin/login',methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("select *from admins where username=%s",(username,))
        admin=cursor.fetchone()
        cursor.close()
        conn.close()
        if admin and admin['password']==password:
            session['admin']=username
            return redirect('/admin/dashboard')
        return "Invalid Credentials"
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin/login')
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users=cursor.fetchone()['total_users']
    cursor.execute("SELECT COUNT(*) AS total_trains FROM trains")
    total_trains=cursor.fetchone()['total_trains']
    cursor.execute("SELECT COUNT(*) AS total_bookings FROM bookings")
    total_bookings=cursor.fetchone()['total_bookings']
    cursor.close()
    conn.close()
    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_trains=total_trains,
        total_bookings=total_bookings
    )

@app.route('/admin/add_train',methods=['GET','POST'])
def add_train():
    if 'admin' not in session:
        return redirect('/admin/login')
    if request.method=="POST":
        train_name=request.form['train_name']
        source=request.form['source']
        destination=request.form['destination']
        departure_time=request.form['departure_time']
        arrival_time=request.form['arrival_time']
        total_seats=request.form['total_seats']
        
        conn=get_db_connection()
        cursor=conn.cursor()
        
        cursor.execute("""insert into trains(train_name,source,destination,departure_time,arrival_time,total_seats,available_seats)
                       values(%s,%s,%s,%s,%s,%s,%s)""",(train_name,source,destination,departure_time,arrival_time,total_seats,total_seats))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin/trains')
    return render_template('add_train.html')

@app.route('/admin/trains')
def admin_trains():
    if 'admin' not in session:
        return redirect('/admin/login')
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select *from trains")
    trains=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_trains.html',trains=trains)

@app.route('/admin/delete_train/<int:id>')
def delete_train(id):
    if 'admin' not in session:
        return redirect('/admin/login')
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM trains WHERE train_id=%s",(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin/trains')

@app.route('/admin/edit_train/<int:train_id>',methods=['GET','POST'])
def edit_train(train_id):
    if 'admin' not in session:
        return redirect('/admin/login')
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    if request.method=="POST":
        train_name=request.form['train_name']
        source=request.form['source']
        destination=request.form['destination']
        departure_time=request.form['departure_time']
        arrival_time=request.form['arrival_time']
        cursor.execute("""update trains set train_name=%s,source=%s,destination=%s,departure_time=%s,
                       arrival_time=%s where train_id=%s""",(train_name,source,destination,departure_time,arrival_time,train_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin/trains')
    cursor.execute("select *from trains where train_id=%s",(train_id,))
    train=cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_train.html',train=train)

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select *from bookings where booking_id=%s",(booking_id,))
    booking=cursor.fetchone()
    if booking:
        cursor.execute("update trains set available_seats=avaliable_seats+%s where train_id=%s",(booking['seats_booked'],booking['train_id']))
        cursor.execute("delete from bookings where booking_id=%s",(booking_id,))
        conn.commit()
    cursor.close()
    conn.close()
    return redirect('/my_bookings')

@app.route('/ticket/<int:booking_id>')
def generate_ticket(booking_id):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    query="""
    SELECT b.*, u.name, t.train_name,
           t.source, t.destination
    FROM bookings b
    JOIN users u
        ON b.user_id = u.user_id
    JOIN trains t
        ON b.train_id = t.train_id
    WHERE b.booking_id=%s
    """
    cursor.execute(query,(booking_id,))
    booking=cursor.fetchone()
    cursor.close()
    conn.close()
    filename = f"ticket_{booking_id}.pdf"
    c=canvas.Canvas(filename)
    c.setFont("Helvetica-Bold",18)
    c.drawString(150,800,"Railway E-Ticket")
    c.setFont("Helvetica",12)
    c.drawString(100,740,f"Passenger: {booking['name']}")
    c.drawString(100,710,f"PNR: {booking['pnr']}")
    c.drawString(100,680,f"Train: {booking['train_name']}")
    c.drawString(100,650,f"Route: {booking['source']} -> {booking['destination']}")
    c.drawString(100,620,f"Seats Booked: {booking['seats_booked']}")
    c.drawString(100,590,f"Booking Date: {booking['booking_date']}")
    c.save()
    return send_file(filename,as_attachment=True)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id=%s",(session['user_id'],))
    user=cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('profile.html',user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    if request.method=='POST':
        name=request.form['name']
        phone=request.form['phone']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']

        cursor.execute("UPDATE users SET name=%s,phone=%s,gender=%s,dob=%s,address=%s WHERE user_id=%s",
            (name,phone,gender,dob,address,session['user_id']))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Profile Updated Successfully","success")
        return redirect('/profile')

    cursor.execute(
        "SELECT * FROM users WHERE user_id=%s",
        (session['user_id'],)
    )
    user=cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template(
        'edit_profile.html',
        user=user
    )

if __name__=="__main__":
    app.run(debug=True)