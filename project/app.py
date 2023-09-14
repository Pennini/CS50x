from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import random
import pyttsx3

from helpers import apology, login_required, write_envelope, search_db

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show envelope"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = search_db(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print(request.form.get("password"), request.form.get("username"), rows)
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("email"):
            return apology("must provide email", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)

        elif not request.form.get("fullname"):
            return apology("must provide full name", 400)

        elif not request.form.get("birthdate"):
            return apology("must provide birth date", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation don't match", 400)

        username = request.form.get("username")
        users = search_db("SELECT * FROM users WHERE username = ?", username)
        emails = search_db(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )

        if users:
            return apology("username already in use", 400)
        if emails:
            return apology("e-mail already in use", 400)

        password = generate_password_hash(request.form.get("password"))
        search_db(
            "INSERT INTO users (username, password, email, fullname, birth_date) VALUES (?, ?, ?, ?, ?)",
            username,
            password,
            request.form.get("email"),
            request.form.get("fullname"),
            request.form.get("birthdate"),
        )

        rows = search_db("SELECT id FROM users WHERE username = ?", username)[0]

        # Remember which user has logged in
        session["user_id"] = rows["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add phrases to the database"""
    if request.method == "POST":
        author = request.form.get("author")
        if not request.form.get("phrase"):
            return apology("must provide a phrase", 400)
        elif not request.form.get("author"):
            author = "Unknown"

        date = str(datetime.datetime.today())[0:10]
        search_db(
            "INSERT INTO user_phrases (user_id, date, phrase, author) VALUES (?, ?, ?, ?)",
            session["user_id"],
            date,
            request.form.get("phrase"),
            author,
        )

        return redirect("/add")

    phrases = search_db(
        "SELECT * FROM user_phrases WHERE user_id = ? AND status = 'active'",
        session["user_id"],
    )
    return render_template("add.html", phrases=phrases)


@app.route("/history")
@login_required
def history():
    """Show all the phrases that already appeared"""
    phrases = search_db(
        "SELECT date, phrase, author FROM phrases AS ph JOIN history AS h ON ph.id = h.phrase_id WHERE h.user_id = ? ORDER BY date DESC",
        session["user_id"],
    )
    user_phrases = search_db(
        "SELECT h.date, phrase, author FROM user_phrases AS uph JOIN history AS h ON uph.id = h.my_phrase_id WHERE h.user_id = ? ORDER BY h.date DESC",
        session["user_id"],
    )
    phrases.extend(user_phrases)
    phrases = sorted(phrases, key=lambda dicionario: dicionario["date"], reverse=True)
    return render_template("history.html", phrases=phrases)


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove phrases from the database"""
    if request.method == "POST":
        phrase_id = request.form.get("phrase_id")
        search_db(
            "UPDATE user_phrases SET status = 'dead' WHERE user_id = ? AND id = ?",
            session["user_id"],
            phrase_id,
        )
        return redirect("/add")

    return redirect("/add")


@app.route("/change_image", methods=["POST"])
@login_required
def change_image():
    """Change the the envelope state"""
    action = request.json.get("action")
    new_image = ""
    today = str(datetime.datetime.today())[0:10]

    phrases_today = search_db(
        "SELECT * FROM history WHERE user_id = ? AND date = ?",
        session["user_id"],
        today,
    )

    phrases_hist = search_db(
        "SELECT * FROM phrases WHERE id IN (SELECT phrase_id FROM history WHERE user_id = ?)",
        session["user_id"],
    )

    count_phrases = search_db("SELECT COUNT(id) AS count FROM phrases")[0]["count"]
    

    phrases = search_db(
        "SELECT * FROM phrases WHERE id NOT IN (SELECT phrase_id FROM history WHERE user_id = ? AND phrase_id IS NOT NULL)",
        session["user_id"],
    )

    user_phrases = search_db(
        "SELECT * FROM user_phrases WHERE id NOT IN (SELECT my_phrase_id FROM history WHERE user_id = ? AND my_phrase_id IS NOT NULL) AND user_id = ? AND status = 'active'",
        session["user_id"],
        session["user_id"],
    )
    phrases.extend(user_phrases)
    if action == "open":
        if not phrases_today:
            phrase = random.choice(phrases)
            if "status" in phrase:
                search_db(
                    "INSERT INTO history (date, user_id, my_phrase_id) VALUES (?, ?, ?)",
                    today,
                    session["user_id"],
                    phrase["id"],
                )
            else:
                search_db(
                    "INSERT INTO history (date, user_id, phrase_id) VALUES (?, ?, ?)",
                    today,
                    session["user_id"],
                    phrase["id"],
                )
            write_envelope(phrase["phrase"], phrase["author"])
        elif count_phrases + len(user_phrases) == len(phrases_hist):
            phrase = {
                "phrase": 'Congratulations! You already got all the motivation necessary to do great in life! You can add more by going to "Add a phrase"',
                "author": "InspireVerse",
            }
            write_envelope(phrase["phrase"], phrase["author"])
        else:
            if phrases_today[0]["phrase_id"]:
                phrase = search_db(
                    "SELECT * FROM phrases WHERE id IN (SELECT phrase_id FROM history WHERE phrase_id = ?)",
                    phrases_today[0]["phrase_id"],
                )[0]
                write_envelope(phrase["phrase"], phrase["author"])
            elif phrases_today[0]["my_phrase_id"]:
                phrase = search_db(
                    "SELECT * FROM user_phrases WHERE id IN (SELECT my_phrase_id FROM history WHERE my_phrase_id = ?)",
                    phrases_today[0]["my_phrase_id"],
                )[0]
                write_envelope(phrase["phrase"], phrase["author"])
        new_image = "./static/envelope_escrito.png"
    elif action == "close":
        new_image = "./static/envelope_fechado.png"

    return jsonify({"new_image": new_image})


@app.route("/speak", methods=["POST"])
@login_required
def speak():
    """Change the the envelope state"""
    today = str(datetime.datetime.today())[0:10]
    phrases_today = search_db(
        "SELECT * FROM history WHERE user_id = ? AND date = ?",
        session["user_id"],
        today,
    )[0]
    if phrases_today["phrase_id"]:
        phrase = search_db(
            "SELECT * FROM phrases WHERE id IN (SELECT phrase_id FROM history WHERE phrase_id = ?)",
            phrases_today["phrase_id"],
        )[0]
    elif phrases_today["my_phrase_id"]:
        phrase = search_db(
            "SELECT * FROM user_phrases WHERE id IN (SELECT my_phrase_id FROM history WHERE my_phrase_id = ?)",
            phrases_today["my_phrase_id"],
        )[0]
    ph = '"' + phrase["phrase"] + '" -' + phrase["author"]
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(ph)
    engine.runAndWait()
    return jsonify({"speak": "speak"})
