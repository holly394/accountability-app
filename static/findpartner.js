document.addEventListener("DOMContentLoaded", async function(){

let name = document.querySelector('.typedName');
name.addEventListener('input', async function() {
    let response = await fetch('/searchpartner?searchname=' + name.value);
    let partners = await response.json();
    let html = '';
    for (let id in partners) {
        let username = partners[id].username;
        let idvalue = partners[id].id;

        html += 'Found ' + username + '.' + '<br>'
        + '<button class="add-partner-action"' + 'partner-id=' + '"' + idvalue + '"' + '>'
        + 'Request partnership?' + '</button>'
        + '<br>';
    }
    document.querySelector('p').innerHTML = html;
    createButtonClickListeners()
});

function createButtonClickListeners() {
    document
    .querySelectorAll('.add-partner-action')
    .forEach(button => {
        button.addEventListener('click', async function(event) {
            let actionButton = this;
            let partnerId = actionButton.getAttribute('partner-id');

            let response = await fetch('/addpartner-json', {
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
        });
    });
}
});