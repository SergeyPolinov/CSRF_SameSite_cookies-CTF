import os
from flask import Flask, request, redirect, render_template, session, make_response

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Устанавливаем SameSite для cookies
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",  # Используем SameSite=Lax
    SESSION_COOKIE_SECURE=False
)

@app.after_request
def after_request(response):
    # Разрешаем запросы только с http://evil:5005
    response.headers.add('Access-Control-Allow-Origin', 'http://evil:5005')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Флаг загружается из переменной окружения
FLAG = os.getenv("FLAG", "practice{default_flag}")

# Фейковая база данных
users = {
    "admin": {"password": "admin123", "flag_visible": False},
    "user": {"password": "user123", "flag_visible": False},
}

def is_logged_in():
    return session.get("username") in users

@app.route("/")
def index():
    return redirect("/login")

@app.route("/welcome")
def welcome():
    if not is_logged_in():
        print(f"[DEBUG] Проверяем, вошел ли пользователь: {session.get('username')}", flush=True)
        return redirect("/login")

    username = session["username"]
    flag = FLAG if username == "admin" and users[username]["flag_visible"] else None

    return f"Welcome, {session['username']}! <a href='/change'>Change Password</a><br>{flag if flag else ''}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["username"] = username
            print(f"[DEBUG] Пользователь {username} вошел в систему, пароль {password}", flush=True)
            return redirect("/welcome")
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/change", methods=["GET", "POST"])
def change():
    if not is_logged_in():
        print(f"[DEBUG] User not logged in", flush=True)
        return redirect("/login")

    if request.method == "GET":
        print(f"[DEBUG] Получен запрос на смену пароля: {request.args}", flush=True)
        new_password = request.args.get("password")
        users[session["username"]]["password"] = new_password

        if session["username"] == "admin":
            users["admin"]["flag_visible"] = True
            session.clear()
            print(f"[DEBUG] Пароль изменен: {users['admin']['password']}", flush=True)
            return f"Password changed! New password: {users['admin']['password']}"

    return render_template("change.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
