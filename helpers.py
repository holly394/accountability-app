from cs50 import SQL
from flask import redirect, render_template, session
from functools import wraps

db = SQL("sqlite:///projectdata.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def find_username(value):
    names = db.execute("""
                        SELECT username FROM accounts WHERE id=?
                          """, value)
    person = ""
    for name in names:
        person = name["username"]
    return person

def find_idNumber(f):
    idNumbers = db.execute("""
                            SELECT id FROM accounts WHERE username = ?
                            """, f)
    number = 0
    for account in idNumbers:
        number = account["id"]
    return number

def find_goals(value):
    goalList = db.execute("""
                        SELECT * FROM goals WHERE user_id = ?
                          """, value)
    return goalList

def add_goal(id, goal):
    db.execute("""
                INSERT INTO goals (user_id, goalDescription, completionStatus, acceptanceStatus, timeStart, timeEnd)
                VALUES (?, ?, ?, ?, ?, ?)
                """, id, goal, "PLANNED", "NOT ACCEPTED", 0, 0)
    return True
