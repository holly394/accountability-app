from cs50 import SQL
from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime

db = SQL("sqlite:///projectdata.db")

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

