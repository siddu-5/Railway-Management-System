from flask import Flask,render_template,request,session,redirect
from database.db import get_db_connection
from werkzeug.security import check_password_hash,generate_password_hash

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

if __name__=="__main__":
    app.run(debug=True)