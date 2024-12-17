from cs50 import SQL
from datetime import datetime

db = SQL("sqlite:///projectdata.db")

def find_wallet(userid):
    wallet = db.execute("""
                        SELECT wallet FROM accounts WHERE id = ?
                        """, userid)
    wallet = float(wallet[0]["wallet"])
    wallet = round(wallet, 2)
    return wallet;

def transactions_total(userid):
    earnings = db.execute("""
                        SELECT SUM(amount) AS earned FROM transactions WHERE user_id = ? AND type = ?
                        """, userid, "EARNING")
    spendings = db.execute("""
                            SELECT SUM(amount) AS spent FROM transactions WHERE user_id = ? AND type = ?
                            """, userid, "SPENDING")
    earning = earnings[0]["earned"]
    spending = spendings[0]["spent"]
    #if there's no data for spending, just return earnings.
    if not spending:
        return earning
    #if no earnings, return 1 because everyone starts with 1 euro in their wallets
    if not earning:
        return 1
    transactionAll = earning - spending + 1
    return transactionAll

def add_transaction(userid, value, type):
    time_now = datetime.now()
    if type == "wishPurchase":
        db.execute("""
                    INSERT INTO transactions (user_id, amount, type, timestamp)
                   VALUES (?, ?, ?, ?)
                   """, userid, value, "SPENDING", time_now)
        return True
    elif type == "goalEarnings":
        db.execute("""
                    INSERT INTO transactions (user_id, amount, type, timestamp)
                   VALUES (?, ?, ?, ?)
                   """, userid, value, "EARNING", time_now)
        return True
    return False

