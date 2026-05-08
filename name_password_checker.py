from flask import Flask, request
import base64

app = Flask(__name__)
@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        
        if not password:
            return "Password required", 400
        
        if len(password) < 8:
            return "Password too short!", 400
        
        combinedCreds = f"{name}:{password}"
        encodedCreds = base64.b46encode(combinedCreds.encode())
        
        return f"welcome {name}"

        session["user"] = name

    return """
    <form method="POST">
    <input type="text" name="name" placeholder="name">
    <input type="password" name="password" placeholder="password">
    <button type="submit">Login</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)