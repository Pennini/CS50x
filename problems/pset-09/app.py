import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user = db.execute("SELECT cash FROM users WHERE id IN (?)", session["user_id"])[0]["cash"]
    portfolio = db.execute("SELECT symbol, shares FROM portfolio WHERE user_id IN (?)", session["user_id"])

    user_info = {"balance": 0}
    for stock in portfolio:
        stock["price"] = round(float(lookup(stock["symbol"])["price"]), 2)
        stock["value"] = round(float(lookup(stock["symbol"])["price"]) * float(stock["shares"]), 2)
        user_info["balance"] += stock["value"]

    user_info["total"] = round(user, 2)
    user_info["balance"] = round(user_info["balance"], 2)

    return render_template("index.html", portfolio=portfolio, user_info=user_info)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 403)
        elif not request.form.get("shares"):
            return apology("must provide a integer number of shares", 403)

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide a integer number of shares", 400)

        if shares < 1:
                return apology("must provide a integer number of shares", 400)

        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("stock doesn't exist", 400)

        rows = db.execute("SELECT * FROM users WHERE id IN (?)", session["user_id"])
        if float(rows[0]["cash"]) < float(stock["price"]) * shares:
            return apology("money not sufficient", 403)

        data = str(datetime.datetime.now())
        db.execute("INSERT INTO buy_history (user_id, symbol, shares, buy_price, year, month, day, hour, minute, seconds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], stock["symbol"], request.form.get("shares"), stock["price"], data[0:4], data[5:7], data[8:10], data[11:13], data[14:16], data[17:22])

        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id IN (?)", session["user_id"])
        have_stock = False
        for st in portfolio:
            if st["symbol"] == stock["symbol"]:
                have_stock = True
                st["shares"] += shares
                db.execute("UPDATE portfolio SET shares = ? WHERE id = ?", st["shares"], st["id"])
                break
        if not have_stock:
            db.execute("INSERT INTO portfolio (user_id, symbol, shares) VALUES (?, ?, ?)", session["user_id"], stock["symbol"], request.form.get("shares"))


        new_amount = float(rows[0]["cash"]) - float(stock["price"]) * float(request.form.get("shares"))
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_amount, session["user_id"])

        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    buy = db.execute("SELECT * FROM buy_history WHERE user_id IN (?)", session["user_id"])
    sell = db.execute("SELECT * FROM sell_history WHERE user_id IN (?)", session["user_id"])

    return render_template("history.html", buy=buy, sell=sell)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide stock", 400)

        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("this stock doesn't exist", 400)

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation don't match", 400)

        username = request.form.get("username")
        users = db.execute("SELECT * FROM users WHERE username = ?", username)

        if users:
            return apology("username already in use", 400)

        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT * FROM portfolio WHERE user_id IN (?)", session["user_id"])
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide a stock", 403)
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        for i in stocks:
            if  i["symbol"] == symbol and int(i["shares"]) < shares:
                    return apology("you don't have that many shares", 400)

        rows = db.execute("SELECT cash FROM users WHERE id IN (?)", session["user_id"])[0]["cash"]
        ticker = lookup(symbol)

        new_amount = rows + (shares * ticker["price"])
        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["shares"] == shares:
                    db.execute("DELETE FROM portfolio WHERE id = ?", stock["id"])
                else:
                    stock["shares"] -= shares
                    db.execute("UPDATE portfolio SET shares = ? WHERE id = ?", stock["shares"], stock["id"])
                break

        data = str(datetime.datetime.now())
        db.execute("INSERT INTO sell_history (user_id, symbol, shares, sell_price, year, month, day, hour, minute, seconds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], ticker["symbol"], request.form.get("shares"), ticker["price"], data[0:4], data[5:7], data[8:10], data[11:13], data[14:16], data[17:22])

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_amount, session["user_id"])

        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)

@app.route("/cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to the user"""
    if request.method == "POST":
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        try:
            amount = str(request.form.get("cash")).replace(",",".")
            amount = float(amount)
        except ValueError:
            return apology("must provide some cash", 400)
        print(amount)
        if amount < 1:
                return apology("must provide some cash", 400)

        amount += cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", amount, session["user_id"])

        return redirect("/")
    # Redirect user to login form
    return render_template("cash.html")