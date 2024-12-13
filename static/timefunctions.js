function TimeDifference (timeStart,timeEnd) {
    const timediff = new Object();
    const sqlStart = timeStart;
    const sqlEnd = timeEnd;
    jsStart = new Date(sqlStart);
    jsEnd = new Date(sqlEnd);

    allTimeDiffInDaysFloat = (jsEnd - jsStart) / 86400000;
    finalDays = Math.floor(allTimeDiffInDaysFloat);
    remainingHoursInDayFormat = allTimeDiffInDaysFloat - finalDays;
    allHoursFloat = remainingHoursInDayFormat*24;
    finalHours = Math.floor(allHoursFloat);
    remainingMinutesInHoursFormat = allHoursFloat - finalHours;
    finalMinutes = Math.floor(remainingMinutesInHoursFormat*60);

    timediff.minutes = finalMinutes;
    timediff.hours = finalHours;
    timediff.days = finalDays;
    return timediff;
}

function TimeFromNow (timeStart) {
    const timediff = new Object();
    const sqlStart = timeStart;
    jsStart = new Date(sqlStart.replace(' ', 'T'));
    timeNow = Date.now();

    allTimeDiffInDaysFloat = (timeNow - jsStart) / 86400000;
    finalDays = Math.floor(allTimeDiffInDaysFloat);
    remainingHoursInDayFormat = allTimeDiffInDaysFloat - finalDays;
    allHoursFloat = remainingHoursInDayFormat*24;
    finalHours = Math.floor(allHoursFloat);
    remainingMinutesInHoursFormat = allHoursFloat - finalHours;
    finalMinutes = Math.floor(remainingMinutesInHoursFormat*60);

    timediff.minutes = finalMinutes;
    timediff.hours = finalHours;
    timediff.days = finalDays;
    return timediff;
}
