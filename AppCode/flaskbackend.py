from flask import Flask, request, redirect, session, render_template
import base64
import secrets
import sqlite3
import bcrypt
import time
import sys
import signal
import os


app = Flask(__name__, 
            template_folder="../HTML", # Tells Flask to look in "../templates" for template files
            static_folder="../assets/", # Tells Flask to look in "../assets" for static files
            static_url_path="/assets" # This makes the URL look like /assets/styles/styles.css
            )

# Needed for flask sessions
app.secret_key = secrets.token_hex(32)


# Handles ctrl+c and closes cleanly
'''
import signal
import time
import sys 

# prints two messages on the screen when closing 
# the parent process (reloader) and child process (flask backend process)
def handleCtrlC(signum, frame):
    print("\nCtrl+C detected! Exiting Cleanly")
    sys.exit(0)

signal.signal(signal.SIGINT, handleCtrlC)
'''
def handleCtrlC(signum, frame):
    # Only print and exit explicitly if this is the active backend worker
    if os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
        print("\nCtrl+C detected! Exiting cleanly...")
    
    sys.exit(0)

# Register the handler for the SIGINT signal (Ctrl+C)
signal.signal(signal.SIGINT, handleCtrlC)


##### START DB #####
def initDB():
    # Connect to a database file (creates 'userDB.db' if its missing)
    connection = sqlite3.connect('userDB.db')
    
    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()
    
    # Execute query to create table and its attributes
    init = '''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL
    )'''

    cursor.execute(init)

    # Hardcoded admin creds
    admin = """
    INSERT INTO users(username,password)
    VALUES('admin','admin123')
    """
    cursor.execute(admin)

    # Saves changes made
    connection.commit()

    # Closes connection to prevent resource leaks
    connection.close()


def loginDB(name, passwd):
    connection = sqlite3.connect('userDB.db')

    cursor = connection.cursor()

    init = '''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL
        )'''
    cursor.execute(init)

    # SQLI ENTRY POINT
    usrLgn = f"""
    SELECT * FROM users WHERE username='{name}' AND password='{passwd}'
    """
    cursor.execute(usrLgn)

    # Fetches for a matching record
    usr = cursor.fetchone()

    connection.close()

    return usr is not None


def regUsr(name, passwd):
    connection = sqlite3.connect("userDB.db")
    cursor = connection.cursor()

    try:
        init = '''
              CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT UNIQUE NOT NULL, 
              password TEXT NOT NULL
        )'''
        
        cursor.execute(init)
        
        # Inserts values into the database
        userRgstr = f"""
        INSERT INTO users(username, password)
        VALUES('{name}','{passwd}')
        """
        
        cursor.execute(userRgstr)
        connection.commit()

        success = True
    
    except sqlite3.IntegrityError:
        err_msg = f"User <b>{name}</b> name is taken"
        success = False 
    
    finally:
        connection.close()
    
    return success

##### END DB #####



# creates login route
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])

#Defines the login functione
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password") # Captures the creds from the user
        
        b64Passwd = base64.b64encode(password.encode()).decode()

        if loginDB(name, b64Passwd):
            combinedCreds = f"{name}:{password}" #combines two variables for later B64 encoding
            encodedCreds = base64.b64encode(combinedCreds.encode()).decode()
            
            #Stores user sessions at the browser level 
            session["user"] = name
            session["auth"] = encodedCreds 
            
            return redirect("/dashboard")

        else:
            # XSS ENTRY POINT
            error_msg = f"User <b>{name}</b> was not found or invalid password."
            return render_template("login.html", error_msg=error_msg)
            
    return render_template("login.html")

    



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        b64Passwd = base64.b64encode(password.encode()).decode()

        if not password:
            return "Password required", 400
        
        if len(password) < 8:
            return "Password too short!", 400

        regUsr(name, b64Passwd)
        
        return redirect("/dashboard")

    return render_template("register.html")




@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")


    return render_template("dashboard.html")





@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")




# Check sessions that are on
@app.route("/sessions")
def sessions():
    return dict(session)

# send favicon out
# import os <--- needs
from flask import send_from_directory

@app.route("/Banner_2.png")
def favicon():
    # This sends favicon file from your assets/icons folder to the root /favicon.png
    return send_from_directory(os.path.join(app.root_path, '../assets/icons'), 
                              'Banner_2.png', 
                               mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)