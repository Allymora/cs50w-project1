import os
import requests

from flask import Flask, session,url_for,render_template, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from help import apology, login_required,lookup

app = Flask(__name__)

#Check for environment variable
#if not os.getenv("DATABASE_URL"):
#raise RuntimeError("DATABASE_URL is not set")

#Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(("postgresql://umozvxqmncpnfb:560c3a8415c5a26fe6237f95deab2825dcb36d43e3cafd376fd9b4d866e6a0e3@ec2-54-91-223-99.compute-1.amazonaws.com:5432/d4ct3t7ojueffn"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
@login_required
def index():
    return render_template("/search") 


@app.route("/register", methods=["GET", "POST"])
def register(): 
    error=''
    cat=''
    #insersion en la tabla user
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirmation =request.form.get('confirmation')
    
        if password != confirmation:
            error ="Password not mathched"
        else:
            try: 
                db.execute('insert into users(user_name, user_pass, user_mail) values(:user, :password, :email)', {"user":user, "password":generate_password_hash(password), "email":email})
                db.commit()
                confirm = db.execute("SELECT user_name FROM users WHERE username = :usern", {"usern":user}).fetchall()
                if(len(confirm) != 0):
                    return apology("Username is not available")
            
                cat=db.execute("Select * from users where user_name = :username", {"username":user}).fetchone()
                cat = dict(cat)
                print(cat) 
                session["user_id"] = cat["id_user"]
            except:  
                error = "Username exist!"    
        return render_template('login.html')
    else:
        return render_template('index.html')    

@app.route("/login", methods=["GET", "POST"])
def login(): 

    if request.method == "POST":
        username= request.form.get('username')
        # Ensure username was submitted
        if not request.form.get("username"):
           return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        lol= db.execute("SELECT * FROM users WHERE user_name = :username",{"username":request.form.get("username")}).fetchone()
        # db.commit x3
        lol = dict(lol)
        print(lol["user_pass"])

        print(len(lol["user_name"]))
        if len(lol) == 0 or not check_password_hash(lol["user_pass"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        print(lol)
        session ["user_id"] = lol["id_user"]

        return redirect("/search")
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")     