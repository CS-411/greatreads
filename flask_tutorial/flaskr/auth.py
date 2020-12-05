import functools
import csv
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pymongo
import numpy as np


bp = Blueprint('auth', __name__, url_prefix='/auth')
myclient = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)
mydb = myclient["mydatabase"]
mycol = mydb["reviews"]

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
            mongo()
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
        elif request.form.get("insert"):
            print('insert pressed', flush=True)
            return redirect(url_for('auth.insert'))
        elif request.form.get("review"):
            print('review pressed', flush=True)
            return redirect(url_for('auth.review'))
        elif request.form.get("searchAuthors"):
            print('searchAuthors pressed', flush=True)
            return redirect(url_for('auth.searchAuthors'))
        elif request.form.get("searchWorkCount"):
            print('searchWorkCount pressed', flush=True)
            return redirect(url_for('auth.searchWorkCount'))
        elif request.form.get("recommendation"):
            print('recommendation pressed', flush=True)
            return redirect(url_for('auth.bookRecommendation'))

        # Search the books
        db = get_db()
        text = request.form.get("text")
        print('text', text)
        results = db.execute(
            "SELECT * FROM Book WHERE Title LIKE :text LIMIT 100", {"text": f"%{text}%"}).fetchall()
        return render_template("auth/welcome.html", results=results, input_value=text, alert_message="No matches found")

    else:
        return render_template("auth/welcome.html")




def mongo():
    #myclient = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)
    #mydb = myclient["mydatabase"]
    #mycol = mydb["reviews"]
    #if request.method == 'GET':

    #if request.method == 'POST':
    print('in mongo up!', flush=True)
    csvfile = open(os.path.join(os.path.dirname(__file__), 'review.csv'), 'r',  encoding='utf-8')
    reader = csv.reader( csvfile )
    header= [ "BookId", "Review1", "Review2", "Review3", "Review4", "Review5"]
    mycol.remove( { } )
    
    i = 0
    n = 0
    doc = {}
    for row in reader:
        #for field in header:
        if i == 0:
            doc = {}
            doc[header[n]] = row[0]
            n= n+1
        if i < 5 :
            doc[header[n]] = row[1]      
        if i == 4:
            x = mycol.insert_one(doc)
            print('okay inserted into doc')
            i = 0
            n = 0
        else:
            i = i+1
            n = n +1

    csvfile.close()
        #print(x, flush= True)
    
    #results = {BookId : "Nope", Review: "Bad"}
    #for one_result in results:
    #    print('one result', one_result)
    #print('results', results)
    #print('names', myclient.list_database_names(), flush=True)
    #print(mydb.list_collection_names(), flush = True)

@bp.route('/review', methods=["GET", "POST"])
def review():
    
    if request.method == "POST":
        db = get_db()

        bookID = request.form.get("text")

        error = None

        bookid = db.execute(
            'SELECT * FROM Book WHERE BookID = ?', (bookID,)
        ).fetchone()

        if bookid is None:
            error = 'Book does not exist'

        if error is None:
            text = request.form.get("text")
            results = mycol.find({"BookId": text}).limit(1)
            return render_template("auth/review.html", results=results, input_value=text, alert_message="No reviews found")

        flash(error)
    
    return render_template("auth/review.html")


@bp.route("/delete", methods=["GET","POST"])
def delete():
    if request.method == "POST":
        # delete the specified book
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
        # update the specified book
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

            if title != "":
                db.execute("UPDATE Book SET Title = ? WHERE BookID = ?", (title,bookID,))
                db.commit()
        
            if author != "":
                db.execute("UPDATE Book SET Author = ? WHERE BookID = ?", (author,bookID,))
                db.commit()
        
            if avgRating != "":
                db.execute("UPDATE Book SET AverageRating = ? WHERE BookID = ?", (avgRating,bookID,))
                db.commit()
        
            if descp != "":
                db.execute("UPDATE Book SET descp = ? WHERE BookID = ?", (descp,bookID,))
                db.commit()

            if pageNum != "":
                db.execute("UPDATE Book SET PageNum = ? WHERE BookID = ?", (pageNum,bookID,))
                db.commit()

            if pubYr != "":
                db.execute("UPDATE Book SET PublicationYear = ? WHERE BookID = ?", (pubYr,bookID,))
                db.commit()

            results = db.execute(
                "SELECT changes()")
            print('results: ', flush=True)
            print(results, flush=True)
            
            return render_template("auth/update.html", results=results, alert_message="UPDATE unsuccessful!")
        
        flash(error)
    
    return render_template("auth/update.html")

@bp.route("/insert", methods=["GET","POST"])
def insert():
    if request.method == "POST":
        # insert the new book
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

        maxBookId = db.execute(
            'SELECT MAX(BookID) FROM Book'
        ).fetchone()

        print('maxBookid: ', flush=True)
        print(maxBookId, flush=True)
        
        if bookid is not None:
            error = ''
            error = 'Book already exists. BookID must be > {}' .format(maxBookId[0])

        if error is None: 

            db.execute(
                "INSERT INTO Book (BookID, Title, Author, AverageRating, descp, PageNum, PublicationYear) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (bookID,title,author,avgRating,descp,pageNum,pubYr,))
            db.commit()

            results = db.execute(
                "SELECT changes()")
            
            return render_template("auth/insert.html", results=results, alert_message="INSERT unsuccessful!")
        
        flash(error)
    
    return render_template("auth/insert.html")

@bp.route("/searchAuthors", methods=["GET","POST"])
def searchAuthors():
    if request.method == "POST":
        # delete the specified book
        db = get_db()

        author1 = request.form.get("author1")
        author2 = request.form.get("author2")

        error = None

        if author1 == "" and author2 == "":
              error = 'Must enter at least one author'

        if error is None:

            if author1 != "" and author2 == "":
                results = db.execute(
                    "SELECT workCount, BookID, Title, Author, AverageRating, descp, PageNum, PublicationYear FROM Book JOIN Author ON Book.Author=Author.Name WHERE Book.Author LIKE :author1", {"author1": f"%{author1}%"}).fetchall()
            elif author1 == "" and author2 != "":
                results = db.execute(
                    "SELECT workCount, BookID, Title, Author, AverageRating, descp, PageNum, PublicationYear FROM Book JOIN Author ON Book.Author=Author.Name WHERE Book.Author LIKE :author2", {"author2": f"%{author2}%"}).fetchall()
            else:
                results = db.execute(
                    "SELECT workCount, BookID, Title, Author, AverageRating, descp, PageNum, PublicationYear FROM Book JOIN Author ON Book.Author=Author.Name WHERE Book.Author LIKE :author1 UNION SELECT workCount, BookID, Title, Author, AverageRating, descp, PageNum, PublicationYear FROM Book JOIN Author ON Book.Author=Author.Name WHERE Book.Author LIKE :author2", {"author1": f"%{author1}%", "author2": f"%{author2}%"}).fetchall()

            print('results: ', flush=True)
            #print(results, flush=True)
            return render_template("auth/searchAuthors.html", results=results, input_value1=author1, input_value2=author2, alert_message="No matches found!")

        flash(error)
    
    return render_template("auth/searchAuthors.html")


@bp.route("/searchWorkCount", methods=["GET","POST"])
def searchWorkCount():
    if request.method == "POST":
        # delete the specified book
        db = get_db()

        userWorkCount = request.form.get("workCount")

        error = None

        if error is None:

            results = db.execute(
                "SELECT workCount, BookID, Title, Author, AverageRating, descp, PageNum, PublicationYear FROM Book JOIN Author ON Book.Author=Author.Name WHERE workCount = ? GROUP BY Author ORDER BY Author ASC", (userWorkCount,)).fetchall()

            print('results: ', flush=True)
            #print(results, flush=True)
            return render_template("auth/searchWorkCount.html", results=results, input_value=userWorkCount, alert_message="No matches found for that work count amount!")

        flash(error)
    
    return render_template("auth/searchWorkCount.html")


@bp.route("/bookRecommendation", methods=["GET","POST"])
def bookRecommendation():
    if request.method == "POST":
        # delete the specified book
        db = get_db()

        key1 = request.form.get("key1")
        key2 = request.form.get("key2")
        key3 = request.form.get("key3")

        error = None

        if error is None:

            #query = mycol.find({'$and': [{'Review1': {'$regex': ".*{}.*".format(key1), '$options': 'i'} }, {'Review2': {'$regex': ".*{}.*".format(key2), '$options': 'i'} }]})
                          
            myquery = {"$and": [{"$or": [{"Review1": {'$regex': ".*{}.*".format(key1), '$options': 'i'}},{"Review2": {'$regex': ".*{}.*".format(key1), '$options': 'i'}},{"Review3": {'$regex': ".*{}.*".format(key1), '$options': 'i'}},{"Review4": {'$regex': ".*{}.*".format(key1), '$options': 'i'}},{"Review5": {'$regex': ".*{}.*".format(key1), '$options': 'i'}}]}, {"$or": [{"Review1": {'$regex': ".*{}.*".format(key2), '$options': 'i'}},{"Review2": {'$regex': ".*{}.*".format(key2), '$options': 'i'}},{"Review3": {'$regex': ".*{}.*".format(key2), '$options': 'i'}},{"Review4": {'$regex': ".*{}.*".format(key2), '$options': 'i'}},{"Review5": {'$regex': ".*{}.*".format(key2), '$options': 'i'}}]}, {"$or": [{"Review1": {'$regex': ".*{}.*".format(key3), '$options': 'i'}},{"Review2": {'$regex': ".*{}.*".format(key3), '$options': 'i'}},{"Review3": {'$regex': ".*{}.*".format(key3), '$options': 'i'}},{"Review4": {'$regex': ".*{}.*".format(key3), '$options': 'i'}},{"Review5": {'$regex': ".*{}.*".format(key3), '$options': 'i'}}]} ]}

            print(key1)

            bookIDs = []

            mongoResults = mycol.find(myquery)

            print("!!!!!!!!!!mongo query done")

            n = mongoResults.count()/6

            for x in mongoResults:
                if n > 0:
                    bookIDs.append(x['BookId'])
                    n = n-1

            print(len(bookIDs))
            print(bookIDs)

            bookRatings = []

            for x in bookIDs:
                results = db.execute('SELECT BookID,AverageRating FROM Book WHERE BookID = ?', (x,)).fetchone()
                bookRatings.append([results['BookID'],results['AverageRating']])

            bookRatings.sort(key=lambda x:x[1],reverse=True)

            print(bookRatings)

            top5 = bookRatings[0:5][0:5]

            print(top5)

            top5IDs = []

            for x in top5:
                top5IDs.append(x[0])

            print(top5IDs)

            titles = []

            for x in top5IDs:
                results = db.execute('SELECT Title FROM Book WHERE BookID = ?', (x,)).fetchone()
                titles.append(results['Title'])

            print('results: ', flush=True)
            print(titles, flush=True)
            return render_template("auth/bookRecommendation.html", results=titles, input_value1=key1, input_value2=key2, input_value3=key3, alert_message="No matches found!")

        flash(error)
    
    return render_template("auth/bookRecommendation.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
