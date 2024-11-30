from cs50 import SQL

#give value of (completed) goal id to get time difference for python calculations
#returns a dictionary!!
def timediff(value):
    timeDiff={}

    db = SQL("sqlite:///projectdata.db")
    timeEnd = db.execute("""SELECT julianday(timeEnd, 'localtime') AS end FROM goals WHERE goal_id = ?
                              """, value)
    timeStart = db.execute("""SELECT julianday(timeStart, 'localtime') AS start FROM goals WHERE goal_id = ?
                            """, value)

    # these are saved as integers in sqlite
    End = timeEnd[0]["end"]
    Start = timeStart[0]["start"]

    days = End - Start
    daysInt = int(days)
    timeDiff["days"] = daysInt

    hours = days - daysInt
    hours = hours * 24
    hoursInt = int(hours)
    timeDiff["hours"] = hoursInt

    minutes = hours - hoursInt
    minutes = minutes * 60
    minutesInt = int(minutes)
    timeDiff["minutes"] = minutesInt

    return timeDiff

def time_pending(value):
    timeDiff={}
    db = SQL("sqlite:///projectdata.db")
    timeDifference = db.execute("""SELECT (julianday('now', 'localtime') - julianday(timeStart)) AS difference FROM goals WHERE goal_id = ?
                            """, value)
    findTimediff = timeDifference[0]["difference"]
    daysInt = int(findTimediff)
    timeDiff["days"] = daysInt

    hours = findTimediff - daysInt
    hours = hours * 24
    hoursInt = int(hours)
    timeDiff["hours"] = hoursInt

    minutes = hours - hoursInt
    minutes = minutes * 60
    minutesInt = int(minutes)
    timeDiff["minutes"] = minutesInt
    return timeDiff
