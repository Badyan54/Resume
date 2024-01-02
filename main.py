from flask import Flask, render_template, url_for, request, flash, get_flashed_messages
from flask import session, redirect, abort, g, make_response
from db import FDataBase
import sqlite3, os, secrets

DATABASE = "coments.db"
DEBUG = False
SECRET_KEY = secrets.token_hex(16)

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE = os.path.join(app.root_path, "coments.db")))


@app.route("/registration", methods = ["POST", "GET"])
def registration():
    db = get_db()
    dbase = FDataBase(db)

    if "userLogged" in session:
        return redirect(url_for('resume'))
    elif request.method == "POST":
        session["userLogged"] = request.form["NickName"]
        res = dbase.addUser(request.form.get("NickName"), request.form.get("password"), request.form.get("Rang"))
        return redirect(url_for('resume'))

    return render_template("registration.html", title = 'registration')

@app.errorhandler(401)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code = error.code), error.code


@app.route("/resume/", methods = ["POST", "GET"])
def resume():
    if "userLogged" not in session:
        abort(401)
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        res = dbase.addPost(request.form.get("commentar"), session["userLogged"])
        return redirect(url_for('resume'))

    return render_template("resume.html", comment = dbase.get_comment())



@app.route("/login", methods =["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if "userLogged" in session:
        return redirect(url_for('resume'))
    elif request.method == "POST":
        if dbase.get_user(request.form["NickName"], request.form["password"]):
            session["userLogged"] = request.form["NickName"]
            return redirect(url_for('resume'))
    
    return render_template("login.html", title = "login")


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

if __name__ == "__main__":
    app.run(debug = True)#debug = True