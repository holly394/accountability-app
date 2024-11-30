from cs50 import SQL

def str_dec_comma(value):
    strWallet = str(value)
    euro = strWallet.replace(".",",")
    return euro

def total_income(value):
    timeHours = value*24
    income = timeHours*12.5
    return income

def find_wallet(value):
    db = SQL("sqlite:///projectdata.db")
    wallet = db.execute("""
                        SELECT wallet FROM accounts WHERE id = ?
                        """, value)
    wallet = float(wallet[0]["wallet"])

    return wallet;
