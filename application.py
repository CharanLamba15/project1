import os
import requests

from flask import Flask, session, render_template, jsonify, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET", "POST"])
def index():
    username = request.form.get("username")
    password = request.form.get("password")
    if(username == "kinggoony"):
        return redirect(url_for('home'))
    else:
        return render_template("index.html")

@app.route("/register")
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    rePassword = request.form.get("rePassword")
    return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    isbn = request.form.get("sIsbn")
    title = request.form.get("sTitle")
    author = request.form.get("sAuthor")
    if isbn:
        isbnResults = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": isbn}).fetchall()
        db.commit()
    if title:
        titleResults = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title": title}).fetchall()
        db.commit()
    if author:
        authorResults = db.execute("SELECT * FROM books WHERE author LIKE :author", {"author": author}).fetchall()
        db.commit()
    return render_template("home.html")

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"KISYPCm0YztL3wFFE49rQ", "isbns": isbn})
    data = res.json()
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html")
    db.commit()
    return jsonify({
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": data['books'][0]['work_ratings_count'],
                "average_score": data['books'][0]['average_rating']
          })