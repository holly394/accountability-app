from cs50 import SQL

db = SQL("sqlite:///projectdata.db")
#give value of (completed) goal id to get time difference for python calculations
#returns a dictionary!!
def timediff(value):
    timeEnd = db.execute("""SELECT julianday(timeEnd, 'localtime') AS end FROM goals WHERE goal_id = ?
                              """, value)
    timeStart = db.execute("""SELECT julianday(timeStart, 'localtime') AS start FROM goals WHERE goal_id = ?
                            """, value)

    # these are saved as integers in sqlite
    End = timeEnd[0]["end"]
    Start = timeStart[0]["start"]

    days = End - Start
    daysInt = int(days)

    hours = days - daysInt
    hours = hours * 24
    hoursInt = int(hours)

    minutes = hours - hoursInt
    minutes = minutes * 60
    minutesInt = int(minutes)

    timeDiff = {'days': daysInt, 'hours': hoursInt, 'minutes': minutesInt}
    return timeDiff

def timediffinHours(id):
    timeEnd = db.execute("""SELECT julianday(timeEnd, 'localtime') AS end FROM goals WHERE goal_id = ?
                               """, id)
    timeStart = db.execute("""SELECT julianday(timeStart, 'localtime') AS start FROM goals WHERE goal_id = ?
                             """, id)
    End = timeEnd[0]["end"]
    Start = timeStart[0]["start"]
    timeinDays = End - Start
    timeinHours = timeinDays*24
    timeinHours = int(timeinHours)
    return timeinHours

def time_pending(goalid):
    db = SQL("sqlite:///projectdata.db")
    timeDifference = db.execute("""SELECT (julianday('now', 'localtime') - julianday(timeStart)) AS difference FROM goals WHERE goal_id = ?
                            """, goalid)
    findTimediff = timeDifference[0]["difference"]
    daysInt = int(findTimediff)

    hours = findTimediff - daysInt
    hours = hours * 24
    hoursInt = int(hours)

    minutes = hours - hoursInt
    minutes = minutes * 60
    minutesInt = int(minutes)

    timeDiff={'days':daysInt,'hours':hoursInt,'minutes':minutesInt}
    return timeDiff
