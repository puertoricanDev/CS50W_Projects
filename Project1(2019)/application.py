import os
import requests

from flask import Flask, session, jsonify, json, render_template, request, redirect
from flask import *
from flask_session import Session
from sqlalchemy import create_engine, literal
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = os.urandom(24)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    mail = request.form.get("email")
    passwd = request.form.get("password")
    try:
        usr = db.execute("SELECT * FROM users WHERE email =:email AND password =:password", {"email":mail,"password":passwd}).fetchone()
    except ValueError:
        return render_template("index.html", errtxt="Error Try again.")
    if usr is None:
        return render_template("index.html", errtxt="Email or password wrong, try again.")
    session['USERNAME']=str(usr.name)
    session['EMAIL']=str(usr.email)
    session['ID']=int(usr.id)
    user=str(session.get('USERNAME'))
    urid=session.get('ID')
    return render_template("search.html", User=user, Id=urid)


@app.route("/logout")
def logout():
    session.clear()
    txterr="Thanks come again soon."
    return render_template("index.html", errtxt=txterr)

@app.route("/back")
def back():
    user=str(session.get('USERNAME'))
    return render_template("search.html", User=user)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/new", methods=["POST"])
def new():
    name = request.form.get("name")
    last = request.form.get("last")
    mail = request.form.get("email")
    passwd1 = request.form.get("pass1")
    passwd2 = request.form.get("pass2")
    if passwd1 == passwd2:
        try:
            txterr = "Register Succesful please Login"
            db.execute("INSERT INTO users(name,last,email,password)VALUES(:name, :last, :email, :password)",{"name":name, "last":last, "email":mail, "password":passwd1})
            db.commit()
            return render_template("index.html", errtxt=txterr)
        except:
            txterr = "Something went wrong please Try Again"
            return render_template("index.html", errtxt=txterr)
    else:
        txterr = "Passwords did not match please Try Again"
        return render_template("register.html", errtxt=txterr)

@app.route("/search", methods=["POST"])
def search():
    srch = request.form.get("mysearch")
    srch = "%"+srch+"%"
    Results= db.execute("SELECT * FROM books WHERE LOWER(author) LIKE LOWER(:search) OR LOWER(isbn) LIKE LOWER(:search) OR LOWER(title) LIKE LOWER(:search)",{"search":srch})
    usr = str(session.get('USERNAME'))
    urid = session.get('ID')
    return render_template("books.html", Results=Results, User=usr, Id=urid)


@app.route("/mybook/<string:isbn>", methods=["GET","POST"])
def mybook(isbn):
    session['ISBN']= isbn
    usr = str(session.get('USERNAME'))
    email = str(session.get('EMAIL'))
    urid = session.get('ID')
    bk = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "a5F9dbdXx6FKqEbrfEPkwg", "isbns":isbn})
    apibook=bk.json()
    reviews = (apibook['books'][0]['reviews_count'])
    rating = (apibook['books'][0]['average_rating'])
    book= db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    review = db.execute("SELECT * FROM review WHERE isbn=:isbn AND user_id=:urid",{"isbn":isbn, "urid":urid}).fetchone()
    prevrev = db.execute("SELECT myreview, stars FROM review WHERE isbn=:isbn",{"isbn":isbn})
    if review is None:
        display="block"
    else:
        display="none"
    return render_template("mybook.html", User=usr, email=email, book=book, Id=urid, display=display,  prevrev=prevrev, isbn=isbn, rating=rating, reviews=reviews)

@app.route("/myreview", methods=["POST"])
def myreview():
    stars = int(request.form.get("stars"))
    isbn = str(session.get('ISBN'))
    urid = session.get('ID')
    usr = str(session.get('USERNAME'))
    email = str(session.get('EMAIL'))
    cmnt = str(request.form.get("comment"))
    comment = usr + " Comment: "+ cmnt
    bk = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "a5F9dbdXx6FKqEbrfEPkwg", "isbns":isbn})
    apibook=bk.json()
    reviews = (apibook['books'][0]['reviews_count'])
    rating = (apibook['books'][0]['average_rating'])
    try:
        db.execute("INSERT INTO review(isbn,myreview,stars,user_id)VALUES(:isbn, :myreview, :stars, :user_id)",{"isbn":isbn, "myreview":comment, "stars":int(stars), "user_id":urid})
        db.commit()
        Results= db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
        prevrev = db.execute("SELECT myreview, stars FROM review WHERE isbn=:isbn",{"isbn":isbn})
        return render_template("mybook.html", User=usr, email=email, book=Results, Id=urid, display="none", prevrev=prevrev, isbn=isbn, rating=rating, reviews=reviews)
    except:
        txterr = "Something went wrong please Try Again"
        return render_template("index.html", errtxt=txterr)


@app.route("/api/<string:isbn>", methods=["GET"])
def isbn(isbn):
    book= db.execute("SELECT * FROM books where isbn=:isbn", {"isbn":isbn}).fetchone()
    if book is None:
        return jsonify({"Error": "Book not found."}),404
    else:
        bk = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "a5F9dbdXx6FKqEbrfEPkwg", "isbns":isbn})
        if bk.status_code !=200:
            raise Exception ("ERROR: API request unsuccesful.")
        apibook=bk.json()
        reviews = (apibook['books'][0]['reviews_count'])
        rating = (apibook['books'][0]['average_rating'])
        return jsonify({
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": isbn,
                "review_count": reviews,
                "average_score": rating
                })
