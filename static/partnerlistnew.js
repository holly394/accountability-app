document.addEventListener("DOMContentLoaded", async function(){
    const myResults = document.querySelector('.results');
    const responseRequester = new Request('/requestedpartnerlist-json');
    const responseAcceptee = new Request('/acceptedpartnerlist-json');
    countPartner = 1;

    fetch(responseRequester)
        .then((response) => response.json())
        .then((data) => {
            for (partner of data) {
                action = "";
                if (partner.status === "REQUESTED") {
                  action = "Wait for response.";
                } else {
                  action = "None.";
                }
                const listRequest = document.createElement("tr")
                listRequest.appendChild(document.createElement("td")).textContent = countPartner;
                listRequest.appendChild(document.createElement("td")).textContent = partner.username;
                listRequest.appendChild(document.createElement("td")).textContent = partner.status;
                listRequest.appendChild(document.createElement("td")).textContent = action;

                myResults.appendChild(listRequest);
                countPartner++;
            }
        });

    fetch(responseAcceptee)
        .then((response) => response.json())
        .then((data) => {
            for (partner of data) {
                const listAccept = document.createElement("tr")
                listAccept.appendChild(document.createElement("td")).textContent = countPartner;
                listAccept.appendChild(document.createElement("td")).textContent = partner.username;
                listAccept.appendChild(document.createElement("td")).textContent = partner.status;

                if (partner.status === "REQUESTED") {
                    acceptButton = document.createElement("button");
                    acceptButton.setAttribute("class", "accept-partner-action");
                    acceptButton.setAttribute("value", partner.id);
                    acceptButton.addEventListener("click", buttonAccept);
                    acceptButton.textContent = "Accept request?";
                    listAccept.appendChild(acceptButton);

                    denyButton = document.createElement("button");
                    denyButton.setAttribute("class", "deny-partner-action");
                    denyButton.setAttribute("value", partner.id);
                    denyButton.addEventListener("click", buttonDeny);
                    denyButton.textContent = "Deny request?";
                    listAccept.appendChild(denyButton);

                } else if (partner.status === "DENIED") {
                    undoButton = document.createElement("button");
                    undoButton.setAttribute("class", "undo-partner-action");
                    undoButton.setAttribute("value", partner.id);
                    undoButton.addEventListener("click", buttonUndo);
                    undoButton.textContent = "Undo denial?";
                    listAccept.appendChild(undoButton);

                } else {
                  action = "None.";
                  listAccept.appendChild(document.createElement("td")).innerHTML = action;
                }

                myResults.appendChild(listAccept);
                countPartner++;
            }
        });


async function buttonAccept() {
    let actionButton = this;
    let partnerId = actionButton.getAttribute('value');

    let response = await fetch('/acceptpartnershiprequest-json', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "id": partnerId,
                })
    });

    let serverJson = await response.json();
    actionButton.innerHTML = serverJson.message;
    actionButton.disabled = true;
    document.querySelector(".deny-partner-action").remove()
    }

async function buttonDeny() {
    let actionButton = this;
    let partnerId = actionButton.getAttribute('value');

    let response = await fetch('/denypartnershiprequest-json', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "id": partnerId,
                })
    });

    let serverJson = await response.json();
    actionButton.innerHTML = serverJson.message;
    actionButton.disabled = true;
    document.querySelector(".accept-partner-action").remove()
    }

async function buttonUndo() {
    let actionButton = this;
    let partnerId = actionButton.getAttribute('value');

    let response = await fetch('/undopartnershipdenial-json', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "id": partnerId,
                })
    });

    let serverJson = await response.json();
    actionButton.innerHTML = serverJson.message;
    actionButton.disabled = true;
    }

});
