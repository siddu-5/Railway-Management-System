from flask import Flask,render_template,request
from database.db import get_db_connection
app=Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form['password']
        
        conn=get_db_connection()
        cursor=conn.cursor()
        
        query="insert into users(name,email,password) values(%s,%s,%s)"
        cursor.execute(query,(name,email,password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return "Registration Successfull!"
    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)