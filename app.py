import os
from xml.etree.ElementTree import tostring

from cs50 import SQL
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, find_username, find_idNumber
from wallets import find_wallet, str_dec_comma, total_income
from timecalc import timediff, time_pending
from goals import find_goals, add_goal
from partners import accepted_partner_list, requested_partners, acceptee_partners, search_by_username, search_requester_acceptee, partner_message
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["find_username"] = find_username
app.jinja_env.filters["timediff"] = timediff
app.jinja_env.filters["time_pending"] = time_pending
app.jinja_env.filters["total_income"] = total_income
app.jinja_env.filters["find_wallet"] = find_wallet

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///projectdata.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Show home page"""
    return render_template("home.html")

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
        rows = db.execute(
            "SELECT * FROM accounts WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
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
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("Must provide username", 400)
        db_result = db.execute("""SELECT * FROM accounts""")
        for name in db_result:
            if name.get("username") == username:
                return apology("Username already exists", 400)
            continue
        if not password:
            return apology("Must provide password", 400)
        if not confirmation:
            return apology("Must confirm password", 400)
        if password != confirmation:
            return apology("Passwords must match", 400)
        db.execute("""
            INSERT INTO accounts (username, hash)
            VALUES(?, ?)
                """, username, generate_password_hash(password))
        return redirect("/login")
    return render_template("register.html")

@app.route("/makegoal", methods=["GET", "POST"])
@login_required
def makegoal():
    """Make a goal for yourself"""
    goalList = find_goals(session["user_id"])
    if request.method == "POST":
        goalDescription = request.form.get("goalDescription")
        if not goalDescription:
            return apology("Must provide a goal", 400)
        add_goal(session["user_id"], goalDescription)
        return redirect("/managegoals")
    return render_template("makegoal.html", goals = goalList)

@app.route("/managegoals")
@login_required
def managegoal():
    goalList = find_goals(session["user_id"])
    return render_template("managegoals.html", goals = goalList)

@app.route("/startgoal", methods=["GET", "POST"])
@login_required
def startgoal():
    if request.method == "POST":
        startbutton = request.form.get("startbutton")
        if not startbutton:
            return redirect("/managegoals")
        goalId = request.form.get("task_id")
        timeNow = datetime.now()
        db.execute("""
                UPDATE goals SET completionStatus = ?, timeStart = ? WHERE goal_id = ?
                """, "IN PROGRESS", timeNow, goalId)
    return redirect("/managegoals")


@app.route("/endgoal", methods=["GET", "POST"])
@login_required
def endgoal():
    if request.method == "POST":
        endbutton = request.form.get("endbutton")
        if not endbutton:
            return redirect("/managegoals")
        goalId = request.form.get("task_id")
        timeNow = datetime.now()
        db.execute("""
                UPDATE goals SET completionStatus = ?, timeEnd = ? WHERE goal_id = ?
                """, "COMPLETED", timeNow, goalId)
    return redirect("/managegoals")

@app.route("/tryagain", methods=["GET", "POST"])
@login_required
def tryagain():
    if request.method == "POST":
        redo = request.form.get("redo")
        if not redo:
            return redirect("/managegoals")
        goalId = request.form.get("task_id")
        db.execute("""
                    UPDATE goals SET completionStatus = ?, acceptanceStatus = ?, timeStart = ?, timeEnd = ? 
                    WHERE goal_id = ?
                   """, "PLANNED", "NOT ACCEPTED", 0, 0, goalId)
    return redirect("/managegoals")

@app.route("/deletegoal", methods=["POST"])
@login_required
def deletegoal():
    if request.method == "POST":
        delete = request.form.get("delete")
        if not delete:
            return redirect("/managegoals")
        goalId = request.form.get("task_id")
        db.execute("""
                    DELETE FROM goals WHERE goal_id = ?
                   """, goalId)
    return redirect("/managegoals")

@app.route("/findpartner")
@login_required
def findpartner():
    return render_template("/findpartner.html")

@app.route("/searchpartner")
def search():
    SearchName = request.args.get("searchname")
    if SearchName:
        partners = db.execute("""SELECT * FROM accounts WHERE username LIKE ?
                                    AND NOT (username IN (?)) """,
                              "%" + str(SearchName) + "%", session["user_name"])
    else:
        partners = []
    return jsonify(partners)

@app.route("/addpartner-json", methods=["POST"])
@login_required
def addpartnerJson():
    content = request.get_json()
    foundPartner = content["id"]

    if not foundPartner:
        return redirect("/findpartner")

    # check if there is an existing request or partnership
    existingRequest = search_requester_acceptee(session["user_id"], foundPartner)
    if existingRequest:
        existingRelationship = existingRequest[0]
        return jsonify({
            "status": existingRelationship["status"],
            "message": partner_message(existingRelationship["status"], 0)
        })

    requestToRespond = search_requester_acceptee(foundPartner, session["user_id"])
    if requestToRespond:
        responder = requestToRespond[0]
        return jsonify({
            "status": responder["status"],
            "message": partner_message(responder["status"], 1)
        })

    db.execute("""INSERT INTO partnerships (requester, acceptee, status) 
                VALUES (?, ?, ?)""",
               session["user_id"], foundPartner, "REQUESTED")

    return jsonify({
        "status": "REQUESTED",
        "message": "Partnership requested."
    })

@app.route("/partnerlist")
@login_required
def partnerlist():
    return render_template("partnerlist.html")

@app.route("/requestedpartnerlist-json")
@login_required
def requestedpartnerlistjson():
    requestedPartnerships = requested_partners(session["user_id"])
    return jsonify(requestedPartnerships)

@app.route("/acceptedpartnerlist-json")
@login_required
def accepteepartnerlistjson():
    toAcceptPartnerships = acceptee_partners(session["user_id"])
    return jsonify(toAcceptPartnerships)

@app.route("/acceptpartnershiprequest-json", methods=["POST"])
@login_required
def acceptpartnershiprequestjson():
    response = request.get_json()
    acceptRequest = response["id"]
    if not acceptRequest:
        return redirect("/partnerlist")
    db.execute("""
                UPDATE partnerships SET status = ? WHERE requester = ? AND acceptee = ?
                """, "ACCEPTED", acceptRequest, session["user_id"])
    return jsonify({
        "message": "Accepted partnership."
    })
@app.route("/denypartnershiprequest-json", methods=["GET", "POST"])
@login_required
def denypartnershiprequestjson():
    response = request.get_json()
    denyRequest = response["id"]
    if not denyRequest:
        return redirect("/partnerlist")
    db.execute("""
                UPDATE partnerships SET status = ? WHERE requester = ? AND acceptee = ?
                """, "DENIED", denyRequest, session["user_id"])
    return jsonify({
        "message": "Denied partnership."
    })

@app.route("/undopartnershipdenial-json", methods=["GET", "POST"])
@login_required
def undopartnershipdenialjson():
    response = request.get_json()
    undoDenial = response["id"]
    if not undoDenial:
        return redirect("/partnerlist")
    db.execute("""
                DELETE FROM partnerships WHERE requester = ? AND acceptee = ?
               """, undoDenial, session["user_id"])
    return jsonify({
        "message": "Erased denial."
    })

@app.route("/seePartnerGoals", methods=["GET", "POST"])
@login_required
def seePartnerGoals():
    # find partners
    partnerList = accepted_partner_list(session["user_id"])
    # make list of goals from accepted partners
    fullGoalList=[]
    # timetaken is in seconds!
    goalList = db.execute("""
                        SELECT * FROM goals
                        """)
    for partner in partnerList:
        for goal in goalList:
            if partner == goal["user_id"]:
                fullGoalList.append(goal)
                continue
    return render_template("seePartnerGoals.html", fullGoalList = fullGoalList)

@app.route("/acceptpartnergoals", methods=["GET","POST"])
@login_required
def acceptpartnergoals():
    if request.method == "POST":
        goalId = request.form.get("goal_id")
        db.execute("""
                    UPDATE goals SET acceptanceStatus = ? WHERE goal_id = ?
                   """, "ACCEPTED", goalId)
    return redirect("/seePartnerGoals")


@app.route("/rejectpartnergoals", methods=["GET", "POST"])
@login_required
def rejectpartnergoals():
    if request.method == "POST":
        goalId = request.form.get("goal_id")
        db.execute("""
                    UPDATE goals SET acceptanceStatus = ? WHERE goal_id = ?
                   """, "REJECTED", goalId)
    return redirect("/seePartnerGoals")

@app.route("/wallet", methods=["GET", "POST"])
@login_required
def wallet():
    """See how much you've made so far"""
    sumWallet=0

    userGoals = db.execute("""
                SELECT goal_id,
                (julianday(timeEnd) - julianday(timeStart)) AS daysTaken
                FROM goals WHERE user_id = ? AND acceptanceStatus = "ACCEPTED"
               """, session["user_id"])

    for goal in userGoals:
        days = goal["daysTaken"]
        income = total_income(days)
        sumWallet = sumWallet + income

    sumWallet = round(sumWallet, 2)

    db.execute("""
                UPDATE accounts SET wallet = ? WHERE id = ?
               """, sumWallet, session["user_id"])

    #change . to , for euro format
    wallet = str_dec_comma(sumWallet)
    return render_template("wallet.html", wallet = wallet)

@app.route("/seewallets")
@login_required
def see_wallets():
    partnerList = accepted_partner_list(session["user_id"])
    return render_template("seewallets.html", partnerList = partnerList)

@app.route("/wishlist")
@login_required
def your_wishlist():
    wishes = db.execute("""
                SELECT * FROM wishlist WHERE user_id = ?
                """, session["user_id"])
    wallet = find_wallet(session["user_id"])
    return render_template("wishlist.html", wishes = wishes, wallet = wallet)

@app.route("/addwish", methods=["GET", "POST"])
@login_required
def addwish():
    if request.method == "POST":
        newWish = request.form.get("newWish")
        wishPrice = request.form.get("wishprice")
        if not newWish:
            return apology("must enter a wish", 403)
        if not wishPrice:
            return apology("must enter a price", 403)
        db.execute("""
                    INSERT INTO wishlist (user_id, wishDescription, price, wishStatus)
                   VALUES (?, ?, ?, ?)
                   """, session["user_id"], newWish, wishPrice, "LISTED")
        return redirect("/wishlist")
    return redirect("/wishlist")

@app.route("/purchaseitem", methods=["GET", "POST"])
@login_required
def purchaseitem():
    if request.method == "POST":
        wishId = request.form.get("wishId")
        wishPrice = request.form.get("wishPrice")
        wallet = find_wallet(session["user_id"])
        newWallet = float(wallet) - float(wishPrice)
        db.execute("""
                    UPDATE accounts SET wallet = ? WHERE id = ?
                   """, newWallet, session["user_id"])
        #db.execute("""
                 #   UPDATE wishlist SET wishStatus = ? WHERE wish_id = ?
                  # """, "PURCHASED", wishId)
    return redirect("/wishlist")



