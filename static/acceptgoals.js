document.addEventListener("DOMContentLoaded", async function() {
    const ListSectionHTML = document.querySelector('.partnerGoalList');
    const partnerGoalsJSON = new Request ("/seePartnerGoals-json");

    countGoals = 1;

    fetch(partnerGoalsJSON)
    .then((response) => response.json())
    .then((data) => {
        for (goal of data) {
            const goalRow = document.createElement("tr");
            goalRow.appendChild(document.createElement("td")).textContent = countGoals;
            goalRow.appendChild(document.createElement("td")).textContent = goal.username;
            goalRow.appendChild(document.createElement("td")).textContent = goal.goalDescription;
            goalRow.appendChild(document.createElement("td")).textContent = goal.completionStatus;

            //time taken
            if (goal.completionStatus == "IN PROGRESS") {
                goalTimeStart = goal.timeStart;
                goaltimedifference = TimeFromNow(goalTimeStart);
                goalRow.appendChild(document.createElement("td"))
                    .innerHTML = goaltimedifference.days +" days "
                    + goaltimedifference.hours + " hours "
                    + goaltimedifference.minutes + " minutes";
            } else if (goal.completionStatus == "COMPLETED") {
                goalTimeStart = goal.timeStart;
                goalTimeEnd = goal.timeEnd;
                completetimediff = TimeDifference(goalTimeStart, goalTimeEnd);
                goalRow.appendChild(document.createElement("td"))
                    .innerHTML = completetimediff.days + " days "
                        + completetimediff.hours + " hours "
                        + completetimediff.minutes + " minutes";
            } else {
                goalRow.appendChild(document.createElement("td"))
                .innerHTML = '';
            }

            //acceptance status
            goalRow.appendChild(document.createElement("td")).textContent = goal.acceptanceStatus;

            if (goal.acceptanceStatus == "NOT ACCEPTED" && goal.completionStatus == "COMPLETED") {
                //action to accept
                acceptButton = document.createElement("button");
                acceptButton.setAttribute("value", goal.goal_id);
                acceptButton.textContent = "ACCEPT?";
                goalRow.appendChild(document.createElement("td"))
                    .appendChild(acceptButton);
                acceptButton.addEventListener("click", buttonAccept);

                //action to reject
                rejectButton = document.createElement("button");
                rejectButton.setAttribute("value", goal.goal_id);
                rejectButton.textContent = "REJECT?";
                goalRow.appendChild(document.createElement("td"))
                    .appendChild(rejectButton);
                rejectButton.addEventListener("click", buttonReject);
            } else {
                goalRow.appendChild(document.createElement("td"));
                goalRow.appendChild(document.createElement("td"));
            }

            ListSectionHTML.appendChild(goalRow);
            countGoals++;
        }
    });

    async function buttonAccept(){
        let actionButton = this;
        let goalId = actionButton.getAttribute("value");

        let response = await fetch("/partnergoalaction", {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(
                {"id": goalId,
                "aim": "accept"})
        });

        let serverAnswer = await response.json();
        if (serverAnswer.status == "accepted") {
            window.location.replace(window.location.href);
        }
    }

    async function buttonReject(){
        let actionButton = this;
        let goalId = actionButton.getAttribute("value");

        let response = await fetch("/partnergoalaction", {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(
                {"id": goalId,
                "aim": "reject"})
        });

        let serverAnswer = await response.json();
        if (serverAnswer.status == "rejected") {
            window.location.replace(window.location.href);
        }
    }
});
