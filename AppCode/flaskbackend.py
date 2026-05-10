from flask import Flask, request, redirect, session, render_template
import base64
import secrets

app = Flask(__name__, template_folder="../templates")

# Needed for flask sessions
app.secret_key = secrets.token_hex(32)

@app.route("/login", methods=["GET", "POST"])


#Defines the login request/response
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password") #Captures the creds from the user
        
        if not password:
            return "Password required", 400
        
        if len(password) < 8:
            return "Password too short!", 400
        
        combinedCreds = f"{name}:{password}" #combines two variables for later B64 encoding
        encodedCreds = base64.b64encode(combinedCreds.encode()).decode()

        #Stores user sessions at the browser level 
        session["user"] = name
        session["auth"] = encodedCreds 

        return redirect("/dashboard")

    #Creates the form
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return "Unauthorized", 401


    return render_template("/dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return "Logged out"


#Check sessions that are on
@app.route("/sessions")
def sessions():
    return dict(session)   

if __name__ == "__main__":
    app.run(debug=True)