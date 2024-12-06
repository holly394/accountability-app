

from cs50 import SQL

db = SQL("sqlite:///projectdata.db")


def accepted_partner_list(value):
    partnerList = []
    accepteePartner = db.execute("""
                                SELECT * FROM partnerships WHERE status = ? AND acceptee = ?
                                 """, "ACCEPTED", value)
    requesterPartner = db.execute("""
                                SELECT * FROM partnerships WHERE status = ? AND requester = ?
                                 """, "ACCEPTED", value)
    for partner in accepteePartner:
        partnerList.append(partner["requester"])
    for partner in requesterPartner:
        partnerList.append(partner["acceptee"])
    return partnerList

def requested_partners(userid):
    requestedPartnerships = db.execute("""
                                    SELECT * FROM partnerships JOIN accounts
                                    ON partnerships.acceptee = accounts.id
                                    WHERE requester = ?
                                      """, userid)
    return requestedPartnerships

def acceptee_partners(userid):
    acceptedPartnerships = db.execute("""
                                SELECT * FROM partnerships JOIN accounts
                                ON partnerships.requester = accounts.id
                                WHERE acceptee = ?
                                """, userid)
    return acceptedPartnerships

def search_by_username(username):
    person = db.execute("SELECT * FROM accounts WHERE username = ?", username)
    return person

def search_requester_acceptee(requester, acceptee):
    relationship = db.execute("""
                SELECT * FROM partnerships WHERE requester = ? AND acceptee = ?
                """, requester, acceptee)
    return relationship

def partner_message(status, position):
    message=""
    if status == "REQUESTED":
        if position == 0: #if requester
            message = "You have already requested a partnership with this person."
        if position == 1: #if responder
            message = "This person has already requested a partnership with you."
    if status == "DENIED":
        if position == 0:
            message = "Partnership was denied."
        if position == 1:
            message = "You have already denied this partnership."
    if status == "ACCEPTED":
            message = "Partnership already exists."
    return message
