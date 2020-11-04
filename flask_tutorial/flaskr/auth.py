import functools
import csv
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
#A view function is the code you write to respond to requests to your application
#A Blueprint is a way to organize a group of related views and other code
#The url_prefix will be prepended to all the URLs associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

#global variable to track if delete button has been pressed
#delete = 0

#When the user visits the /auth/register URL, the register view will return HTML with a form for them to fill out.
# When they submit the form, it will validate their input and either show the form again with an error message or create 
#the new user and go to the login page.


#@bp.route associates the URL /register with the register view function. 
#When Flask receives a request to /auth/register, it will call the register view and use the return value as the response.
#If the user submitted the form, request.method will be 'POST'. In this case, start validating the input.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    
    if request.method == 'POST':
        print('in register up!', flush=True)
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            print('in register', flush=True)
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            bookssql()
            authorsql()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

def bookssql():
    db = get_db()
    f = open("books.csv", encoding="utf8")
    reader = csv.reader(f)

    for BookID, Title, Author, AverageRating,Description, PageNum, PublicationYear in reader:
        db.execute('INSERT INTO Book (BookID, Title,Author, AverageRating, descp, PageNum, PublicationYear) VALUES (?,?,?,?,?,?,?)',
            (BookID, Title, Author, AverageRating,Description, PageNum,PublicationYear )
            )
        #print(f"Added book {title}, {author}, {year} with gid = {gid}")
    print('inserted all books', flush=True)
    db.commit()
    print('error here', flush=True)

def authorsql():

    db = get_db()
    f = open("authors.csv", encoding="utf8")
    reader = csv.reader(f)

    for Name, workCount in reader:
        db.execute('INSERT INTO Author (Name, workCount) VALUES (?,?)',
            (Name, workCount )
            )
        #print(f"Added book {title}, {author}, {year} with gid = {gid}")
    print('inserted authors', flush=True)
    db.commit()

#called upon DELETE button being pressed
# def deletePressed():
#     delete = 1


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

#session is a dict that stores data across requests
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.welcome'))

        flash(error)

    return render_template('auth/login.html')


# @bp.route("/welcome", methods=["GET", "POST"])
# def welcome():
#    # if session.get("user_name") is None:
#     #    return redirect("index")
#     if request.method == "POST":
#         # Search the books
#         text = request.form.get("text")
#         results = db.execute(
#             "SELECT * FROM Book WHERE Title LIKE :text OR Author LIKE :text", {"text": "%{text}%"}).fetchall()
#         return render_template("auth/welcome.html", results=results, input_value=text, alert_message="No matches found")
#     else:
#         return render_template("auth/welcome.html")

@bp.route("/welcome", methods=["GET","POST"])
def welcome():
    if request.method == "POST":
        print('search pressed', flush=True)

        if request.form.get("delete"):
            print('delete pressed', flush=True)
            return redirect(url_for('auth.delete'))
        elif request.form.get("update"):
            print('update pressed', flush=True)
            return redirect(url_for('auth.update'))

        # Search the books
        db = get_db()
        text = request.form.get("text")
        results = db.execute(
            "SELECT * FROM Book WHERE Title LIKE :text LIMIT 100", {"text": f"%{text}%"}).fetchall()
        return render_template("auth/welcome.html", results=results, input_value=text, alert_message="No matches found")

    else:
        return render_template("auth/welcome.html")


@bp.route("/delete", methods=["GET","POST"])
def delete():
    if request.method == "POST":
        # delete the specified
        db = get_db()

        bookID = request.form.get("text")

        error = None

        bookid = db.execute(
            'SELECT * FROM Book WHERE BookID = ?', (bookID,)
        ).fetchone()

        if bookid is None:
            error = 'Book does not exist'

        if error is None:
        
            db.execute("DELETE FROM Book WHERE BookID = ?", (bookID,))
            db.commit()
            results = db.execute(
                "SELECT changes()")
            print('results: ', flush=True)
            print(results, flush=True)
            return render_template("auth/delete.html", results=results, input_value=bookID, alert_message="DELETE unsuccessful!")

        flash(error)
    
    return render_template("auth/delete.html")

@bp.route("/update", methods=["GET","POST"])
def update():
    if request.method == "POST":
        # delete the specified
        db = get_db()

        bookID = request.form.get('BookID')
        title = request.form.get('title')
        author = request.form.get('author')
        avgRating = request.form.get('avgrating')
        descp = request.form.get('descp')
        pageNum = request.form.get('pageNum')
        pubYr = request.form.get('PubYr')

        error = None

        bookid = db.execute(
            'SELECT * FROM Book WHERE BookID = ?', (bookID,)
        ).fetchone()
        
        if bookid is None:
            error = 'Book does not exist'

        if error is None: 

            # all of these are commented out because each if statement gives a syntax error
            # Purpose of these if statements is to only run Update command on fields that
            # a value was inserted for so we don't update with empty value

            # if title != ""
                #db.execute("UPDATE Book SET Title = ? WHERE BookID = ?", (title,bookID,))
                #db.commit()
        
            #if author != ""
                #db.execute("UPDATE Book SET Author = ? WHERE BookID = ?", (author,bookID,))
                #db.commit()
        
            #if avgRating != ""
                #db.execute("UPDATE Book SET AverageRating = ? WHERE BookID = ?", (avgRating,bookID,))
                #db.commit()
        
            #if descp != ""
                #db.execute("UPDATE Book SET descp = ? WHERE BookID = ?", (descp,bookID,))
                #db.commit()

            #if pageNum != ""
                #db.execute("UPDATE Book SET PageNum = ? WHERE BookID = ?", (pageNum,bookID,))
                #db.commit()

            #if pubYr != ""
                #db.execute("UPDATE Book SET PublicationYear = ? WHERE BookID = ?", (pubYr,bookID,))
                #db.commit()

            results = db.execute(
                "SELECT changes()")
            print('results: ', flush=True)
            print(results, flush=True)
            
            return render_template("auth/update.html", results=results, alert_message="UPDATE unsuccessful!")
        
        flash(error)
    
    return render_template("auth/update.html")

#bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
#load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database, storing it on g.user, 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#To log out, you need to remove the user id from the session. Then load_logged_in_user won’t load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




#This decorator returns a new view function that wraps 
#the original view it’s applied to. The new function checks if a user is loaded and redirects to the login page otherwise.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
