document.addEventListener("DOMContentLoaded", async function(){

    const newGoalButton = document.getElementById("addNewGoalButton");
    newGoalButton.addEventListener("click", NewGoalAdd);

    const myGoalListHTML = document.querySelector('.mygoals');
    const myGoalsJSON = new Request("/mygoals-json");
    countGoals = 1;

    fetch(myGoalsJSON)
        .then((response) => response.json())
        .then((data) => {
            for (goal of data) {
                const goalRow = document.createElement("tr");
                goalRow.appendChild(document.createElement("td")).textContent = countGoals;
                goalRow.appendChild(document.createElement("td")).textContent = goal.goalDescription;
                goalRow.appendChild(document.createElement("td")).textContent = goal.completionStatus;
                goalRow.appendChild(document.createElement("td")).textContent = goal.acceptanceStatus;
                goalRow.appendChild(document.createElement("td")).textContent = goal.timeStart;
                goalRow.appendChild(document.createElement("td")).textContent = goal.timeEnd;
                //Action button & time difference
                if (goal.completionStatus == "PLANNED") {
                    startTaskButton = document.createElement("button");
                    startTaskButton.setAttribute("value", goal.goal_id);
                    goalRow.appendChild(document.createElement("td"))
                        .appendChild(startTaskButton);
                    startTaskButton.addEventListener("click", buttonStart);
                    startTaskButton.textContent = "Start goal?";
                    goalRow.appendChild(document.createElement("td")).innerHTML = '';
                } else if (goal.completionStatus == "IN PROGRESS") {
                    endTaskButton = document.createElement("button");
                    endTaskButton.setAttribute("value", goal.goal_id);
                    goalRow.appendChild(document.createElement("td")).appendChild(endTaskButton);
                    endTaskButton.addEventListener("click", buttonEnd);
                    endTaskButton.textContent = "Finished goal?";
                    goalTimeStart = goal.timeStart;
                    goaltimedifference = TimeFromNow(goalTimeStart);
                    goalRow.appendChild(document.createElement("td"))
                        .innerHTML = goaltimedifference.days +" days "
                        + goaltimedifference.hours + " hours "
                        + goaltimedifference.minutes + " minutes";
                } else if (goal.completionStatus == "COMPLETED") {
                    if (goal.acceptanceStatus == "REJECTED") {
                        tryagainButton = document.createElement("button");
                        goalRow.appendChild(document.createElement("td")).appendChild(tryagainButton);
                        tryagainButton.setAttribute("value", goal.goal_id);
                        tryagainButton.addEventListener("click", buttonRedo);
                        tryagainButton.textContent = "Try again?";
                    } else {
                        goalRow.appendChild(document.createElement("td"))
                        .innerHTML = '';
                    }
                        goalTimeStart = goal.timeStart;
                        goalTimeEnd = goal.timeEnd;
                        completetimediff = TimeDifference(goalTimeStart, goalTimeEnd);

                        goalRow.appendChild(document.createElement("td"))
                            .innerHTML = completetimediff.days + " days "
                                + completetimediff.hours + " hours "
                                + completetimediff.minutes + " minutes";
                }
                //delete task button
                if (goal.acceptanceStatus != "ACCEPTED") {
                    deleteTaskButton = document.createElement("button");
                    goalRow.appendChild(document.createElement("td")).appendChild(deleteTaskButton);
                    deleteTaskButton.setAttribute("value", goal.goal_id);
                    deleteTaskButton.addEventListener("click", buttonDelete);
                    deleteTaskButton.textContent = "Delete task?";
                }

                //add everything into the row
                myGoalListHTML.appendChild(goalRow);
                countGoals++;
            }
        });

async function NewGoalAdd() {
    let x = document.getElementById("newGoalDescription").value;
    if (x == "") {
        alert("Must enter a goal");
        return false;
    }

    let response = await fetch("/addgoal", {
    method: 'POST',
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(
        {"newgoal": x})
    });

    let serverAnswer = await response.json();
    if (serverAnswer.message == "new added") {
        window.location.replace(window.location.href);
    }
}

async function buttonStart(){
    let actionButton = this;
    let goalId = actionButton.getAttribute("value");

    let response = await fetch("/goalaction", {
        method: 'POST',
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(
            {"id": goalId,
            "aim": "start"})
    });

    let serverAnswer = await response.json();
    if (serverAnswer.status == "started") {
        window.location.replace(window.location.href);
    }
}

async function buttonEnd(){
    let actionButton = this;
    let goalId = actionButton.getAttribute("value");

    let response = await fetch("/goalaction", {
        method: 'POST',
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(
            {"id": goalId,
            "aim": "end"}
        )
    });

    let serverAnswer = await response.json();
    if (serverAnswer.status == "ended") {
        window.location.replace(window.location.href);
    }
}

async function buttonRedo(){
    let actionButton = this;
    let goalId = actionButton.getAttribute("value");

    let response = await fetch("/goalaction", {
        method: 'POST',
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(
            {"id": goalId,
            "aim": "redo"}
        )
    });

    let serverAnswer = await response.json();
    if (serverAnswer.status == "reset") {
        window.location.replace(window.location.href);
    }
}

async function buttonDelete(){
    let actionButton = this;
    let goalId = actionButton.getAttribute("value");

    let response = await fetch("/goalaction", {
        method: 'POST',
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(
            {"id": goalId,
            "aim": "delete"}
        )
    });

    let serverAnswer = await response.json();
    if (serverAnswer.status == "deleted") {
        window.location.replace(window.location.href);
    }
}

});