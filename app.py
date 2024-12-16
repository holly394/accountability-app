from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, find_username, find_goals, add_goal
from wallets import str_dec_comma, total_purchase_history, find_wallet, all_approved_task_ids
from timecalc import timediff, time_pending, timediffinHours
from partners import accepted_partner_list, requested_partners, acceptee_partners, search_requester_acceptee, partner_message
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["find_username"] = find_username
app.jinja_env.filters["timediff"] = timediff
app.jinja_env.filters["time_pending"] = time_pending
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

@app.route("/maingoalpage")
@login_required
def makegoal():
    return render_template("maingoalpage.html")

@app.route("/mygoals-json")
@login_required
def mygoalsjson():
    goal_list = find_goals(session["user_id"])
    return jsonify(goal_list)

@app.route("/addgoal", methods=["POST"])
@login_required
def addgoal():
    content = request.get_json()
    new_goal = content["newgoal"]
    add_goal(session["user_id"], new_goal)
    return jsonify({"message":"new added"})

@app.route("/goalaction", methods=["GET", "POST"])
@login_required
def goalaction():
    content = request.get_json()
    goal_id = content["id"]
    purpose = content["aim"]
    time_now = datetime.now()
    if purpose == "start":
        db.execute("""
                UPDATE goals SET completionStatus = ?, timeStart = ? WHERE goal_id = ?
                """, "IN PROGRESS", time_now, goal_id)
        return jsonify({"status":"started"})

    elif purpose == "end":
        db.execute("""
                    UPDATE goals SET completionStatus = ?, timeEnd = ? WHERE goal_id = ?
                    """, "COMPLETED", time_now, goal_id)
        return jsonify({"status": "ended"})

    elif purpose == "redo":
        db.execute("""
                    UPDATE goals SET completionStatus = ?, acceptanceStatus = ?, timeStart = ?, timeEnd = ? 
                    WHERE goal_id = ?
                   """, "PLANNED", "NOT ACCEPTED", 0, 0, goal_id)
        return jsonify({"status": "reset"})

    elif purpose == "delete":
        db.execute("""
                    DELETE FROM goals WHERE goal_id = ?
                   """, goal_id)
        return jsonify({"status": "deleted"})
    else:
        return jsonify({"status":"action not taken"})

@app.route("/findpartner")
@login_required
def findpartner():
    return render_template("/findpartner.html")

@app.route("/searchpartner")
def search():
    search_name = request.args.get("searchname")
    if search_name:
        partners = db.execute("""SELECT * FROM accounts WHERE username LIKE ?
                                    AND NOT (username IN (?)) """,
                              "%" + str(search_name) + "%", session["user_name"])
    else:
        partners = []
    return jsonify(partners)

@app.route("/addpartner-json", methods=["POST"])
@login_required
def addpartner_json():
    content = request.get_json()
    found_partner = content["id"]

    if not found_partner:
        return redirect("/findpartner")

    # check if there is an existing request or partnership
    existing_request = search_requester_acceptee(session["user_id"], found_partner)
    if existing_request:
        existing_relationship = existing_request[0]
        return jsonify({
            "status": existing_relationship["status"],
            "message": partner_message(existing_relationship["status"], 0)
        })

    request_to_respond = search_requester_acceptee(found_partner, session["user_id"])
    if request_to_respond:
        responder = request_to_respond[0]
        return jsonify({
            "status": responder["status"],
            "message": partner_message(responder["status"], 1)
        })

    db.execute("""INSERT INTO partnerships (requester, acceptee, status) 
                VALUES (?, ?, ?)""",
               session["user_id"], found_partner, "REQUESTED")

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
    requested_partnerships = requested_partners(session["user_id"])
    return jsonify(requested_partnerships)

@app.route("/acceptedpartnerlist-json")
@login_required
def accepteepartnerlistjson():
    to_accept_partnerships = acceptee_partners(session["user_id"])
    return jsonify(to_accept_partnerships)

@app.route("/answerpartnerrequest", methods=["POST", ])
@login_required
def answerpartnerrequest():
    response = request.get_json()
    requester = response["id"]
    answer = response["answer"]

    if answer == "accept":
        db.execute("""
                    UPDATE partnerships SET status = ? WHERE requester = ? AND acceptee = ?
                    """, "ACCEPTED", requester, session["user_id"])
        return jsonify({
            "message": "Accepted partnership."
        })
    elif answer == "deny":
        db.execute("""
                    UPDATE partnerships SET status = ? WHERE requester = ? AND acceptee = ?
                    """, "DENIED", requester, session["user_id"])
        return jsonify({
            "message": "Denied partnership."
        })
    elif answer == "undo":
        db.execute("""
                    DELETE FROM partnerships WHERE requester = ? AND acceptee = ?
                   """, requester, session["user_id"])
        return jsonify({
            "message": "Undid denial."
        })
    else:
        return jsonify({
            "message": "No action taken."
        })

@app.route("/seePartnerGoals-json", methods=["GET", "POST"])
@login_required
def see_partner_goalsjson():
    # find partners
    partner_list = accepted_partner_list(session["user_id"])
    # make list of goals from accepted partners
    full_goal_list=[]
    goals = db.execute("""
                        SELECT * FROM goals
                        JOIN accounts ON goals.user_id=accounts.id
                        """)
    for goal in goals:
        goaluserid = goal["user_id"]
        for partner in partner_list:
            if partner == goaluserid:
                full_goal_list.append(goal)
    return jsonify(full_goal_list)

@app.route("/seePartnerGoals")
@login_required
def see_partner_goals():
    return render_template("seePartnerGoals.html")

@app.route("/partnergoalaction", methods=["GET", "POST"])
@login_required
def partnergoalaction():
    content = request.get_json()
    goal_id = content["id"]
    purpose = content["aim"]
    if purpose == "accept":
        #update goal status
        db.execute("""
                    UPDATE goals SET acceptanceStatus = ? WHERE goal_id = ?
                   """, "ACCEPTED", goal_id)
        #update partner's wallet
        partnerid = db.execute("""
                    SELECT user_id FROM goals WHERE goal_id = ?
                   """,goal_id)
        partneridnumber = partnerid["user_id"]
        totalincome = 0
        all_approved_task_list = all_approved_task_ids(partneridnumber)
        for task in all_approved_task_list:
            work_hours = timediffinHours(task)
            income = work_hours * 12.5
            totalincome = totalincome + income
        totalpurchases = total_purchase_history(partnerid)
        wallet = totalincome - totalpurchases
        db.execute("""
                        UPDATE accounts SET wallet = ? WHERE id = ?
                       """, wallet, partnerid)
        return jsonify({"status":"accepted"})
    elif purpose == "reject":
        db.execute("""
                    UPDATE goals SET acceptanceStatus = ? WHERE goal_id = ?
                   """, "REJECTED", goal_id)
        return jsonify({"status":"rejected"})
    else:
        return jsonify({"status":"action not taken"})

@app.route("/wishlist")
@login_required
def wishlist():
    return render_template("wishlist.html")

@app.route("/wishlist-json", methods=["GET", "POST"])
@login_required
def wishlist_json():
    full_wish_list = []
    wishes = db.execute("""
                SELECT * FROM wishlist 
                JOIN accounts ON wishlist.user_id=accounts.id
                """)
    for wish in wishes:
        wish_user_id = wish["user_id"]
        if wish_user_id == session["user_id"]:
            full_wish_list.append(wish)
    return jsonify(full_wish_list)

@app.route("/purchaseitem", methods=["GET", "POST"])
@login_required
def purchaseitem():
    content = request.get_json()
    wish_id = content["id"]
    db.execute("""
                 UPDATE wishlist SET wishStatus = ? WHERE wish_id = ?
                  """, "PURCHASED", wish_id)
    totalincome = 0
    all_approved_task_list = all_approved_task_ids(session["user_id"])

    for task in all_approved_task_list:
        work_hours = timediffinHours(task)
        income = work_hours*12.5
        totalincome = totalincome + income

    totalpurchases = total_purchase_history(session["user_id"])
    wallet = totalincome - totalpurchases
    db.execute("""
                    UPDATE accounts SET wallet = ? WHERE id = ?
                   """, wallet, session["user_id"])
    return jsonify({"message":"item purchased"})

@app.route("/addwish", methods=["GET", "POST"])
@login_required
def addwish():
    content = request.get_json()
    wish_item = content["item"]
    wish_price = content["price"]
    db.execute("""
                INSERT INTO wishlist (user_id, wishDescription, price, wishStatus)
               VALUES (?, ?, ?, ?)
               """, session["user_id"], wish_item, wish_price, "LISTED")
    return jsonify({"message":"new wish added"})

@app.route("/seewallets")
@login_required
def see_wallets():
    partner_list = accepted_partner_list(session["user_id"])
    my_wallet = find_wallet(session["user_id"])
    # change . to , for euro format
    wallet = str_dec_comma(my_wallet)
    return render_template("seewallets.html", partnerList=partner_list, wallet=wallet)
