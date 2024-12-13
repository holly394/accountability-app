from cs50 import SQL

db = SQL("sqlite:///projectdata.db")

def str_dec_comma(value):
    strWallet = str(value)
    euro = strWallet.replace(".",",")
    return euro

def all_approved_task_ids(userid):
    approvedTaskIds = db.execute("""
                    SELECT goal_id FROM goals WHERE user_id = ? AND acceptanceStatus = ?
                    """, userid, "ACCEPTED")
    finalTaskList = []
    for task in approvedTaskIds:
        taskid = task["goal_id"]
        finalTaskList.append(taskid)

    return finalTaskList

def total_purchase_history(userid):
    purchases = db.execute("""
                               SELECT price FROM wishlist WHERE user_id = ?
                               AND wishStatus = ?
                               """, userid, "PURCHASED")
    priceList=[]
    totalCost = 0
    for item in purchases:
        price = item["price"]
        priceList.append(price)
    for buy in priceList:
        totalCost = totalCost + buy
    return totalCost

def find_wallet(userid):
    wallet = db.execute("""
                        SELECT wallet FROM accounts WHERE id = ?
                        """, userid)
    wallet = float(wallet[0]["wallet"])
    wallet = round(wallet, 2)
    return wallet;


