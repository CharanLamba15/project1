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
    # Make sure username != '1' and password != "1"
    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone()
    db.commit()
    if(user):
        session['id'] = user.id
    else:
        session['id'] = request.args.get('id')
    if(user and username != None and password != None):
        return redirect(url_for('home', username = username))
    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    rePassword = request.form.get("rePassword")
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    db.commit()
    if(user):
        title = "Account Exists"
        message = "This account already exists please try a different username"
        return render_template("error.html", title = title, message = message)
    if(password != rePassword):
        title = "Password's don't match"
        message = "Password and Re-enter password don't match"
        return render_template("error.html", title = title, message = message)
    if(username != None and username != '1' and password != None and password != '1' and not user):
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
        db.commit()
        return redirect(url_for('index'))
    return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if(session['id'] != None):
        isbn = request.form.get("sIsbn")
        title = request.form.get("sTitle")
        author = request.form.get("sAuthor")
        if(isbn or title or author):
            return redirect(url_for('results', isbn = isbn, title = title, author = author))
        return render_template("home.html", username = request.args.get('username'))
    else:
        return render_template("access_denied.html")

@app.route("/home/results", methods=["GET", "POST"])
def results():
    if(session['id'] != None):
        isbn = request.args.get('isbn')
        title = request.args.get('title')
        author = request.args.get('author')
        id = None
        if(isbn):
            isbnResults = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {'isbn': '%'+isbn+'%'} ).fetchall()
            db.commit()
        else:
            isbnResults = None
        if(title):
            titleResults = db.execute("SELECT * FROM books WHERE title LIKE :title", {'title': '%'+title+'%'} ).fetchall()
            db.commit()
        else:
            titleResults = None
        if(author):
            authorResults = db.execute("SELECT * FROM books WHERE author LIKE :author", {'author':'%'+author+'%'}).fetchall()
            db.commit()
        else:
            authorResults = None
        return render_template("results.html", isbnResults = isbnResults, titleResults = titleResults, authorResults = authorResults)
    else:
        return render_template("access_denied.html")

@app.route("/home/results/book", methods=["GET", "POST"])
def book():
    if(session['id'] != None):
        isbn = request.args.get('isbn')
        # review = requests.form.get('review')
        id = session["id"]
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        db.commit()
        # reviewExists = db.execute("SELECT * FROM reviews WHERE id = :id", {"id": id})
        # db.commit()
        return render_template("book.html", book = book)
    else:
        return render_template("access_denied.html")

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