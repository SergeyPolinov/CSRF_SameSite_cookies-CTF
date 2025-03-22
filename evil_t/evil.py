from flask import Flask, redirect, render_template

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("csrf.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
