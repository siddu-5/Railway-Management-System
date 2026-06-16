from flask import Flask,render_template,request,session,redirect
from database.db import get_db_connection
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime
import random

app=Flask(__name__)
app.secret_key="railway_secret_key"
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=generate_password_hash(request.form['password'])
        
        conn=get_db_connection()
        cursor=conn.cursor()
        
        query="insert into users(name,email,password) values(%s,%s,%s)"
        cursor.execute(query,(name,email,password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return "Registration Successfull!"
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        
        query="select * from users where email=%s"
        cursor.execute(query,(email,))
        user=cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'],password):
            session['user_id']=user['user_id']
            session['name']=user['name']
            return redirect("/dashboard")
        return "Invalid Email or Password"
    return render_template("login.html")

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
        seats=int(request.form['seats'])
        if seats>train['available_seats']:
            return "Not enough seats available"
        pnr="PNR"+str(random.randint(100000,999999))
        cursor.execute("insert into bookings(pnr,user_id,train_id,seats_booked,booking_date)values(%s,%s,%s,%s,%s)",
                       (pnr,session['user_id'],train_id,seats,datetime.now()))
        cursor.execute("UPDATE trains SET available_seats=available_seats-%s WHERE train_id=%s",(seats, train_id))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("booking_success.html",pnr=pnr)
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
    cursor.execute("SELECT COUNT(*) AS total_trains FROM trains")
    trains=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) AS total_bookings FROM bookings")
    bookings=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users=cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template(
        'admin_dashboard.html',
        total_trains=trains['total_trains'],
        total_bookings=bookings['total_bookings'],
        total_users=users['total_users']
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

if __name__=="__main__":
    app.run(debug=True)