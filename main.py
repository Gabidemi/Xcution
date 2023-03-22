from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route("/")
def index():
    print("Xcution_Testing_Site")
    return render_template("home.html.jinja")