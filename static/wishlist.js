document.addEventListener("DOMContentLoaded", async function(){
    const newWishButton = document.getElementById("addNewWishButton");
    newWishButton.addEventListener("click", NewWishAdd);

    const myWishListHTML = document.querySelector('.myWishlist');
    const myWishesJSON = new Request("/wishlist-json");
    countWishes = 1;
    fetch(myWishesJSON)
        .then((response) => response.json())
        .then((data) => {
            for (wish of data) {
                const wishRow = document.createElement("tr");
                wishRow.appendChild(document.createElement("td")).textContent = countWishes;
                console.log(wish.wishDescription);
                wishRow.appendChild(document.createElement("td")).textContent = wish.wishDescription;
                wishRow.appendChild(document.createElement("td")).textContent = wish.price;
                wishRow.appendChild(document.createElement("td")).textContent = wish.wishStatus;

                //action column
                if (wish.wallet > wish.price && wish.wishStatus == "LISTED") {
                    purchaseButton = document.createElement("button");
                    purchaseButton.setAttribute("value", wish.wish_id);
                    purchaseButton.addEventListener("click", buttonPurchase);
                    purchaseButton.textContent = "Purchase item?";
                    wishRow.appendChild(document.createElement("td")).appendChild(purchaseButton);
                } else if (wish.wishStatus == "PURCHASED") {
                    wishRow.appendChild(document.createElement("td"))
                            .innerHTML = 'Purchased';
                } else {
                    wishRow.appendChild(document.createElement("td"))
                            .innerHTML = 'Not enough funds';
                }

            myWishListHTML.appendChild(wishRow);
            countWishes++;
            }
        });

async function buttonPurchase(){
    let actionButton = this;
    let purchaseId = actionButton.getAttribute("value");

    let response = await fetch("/purchaseitem", {
        method: 'POST',
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            "id": purchaseId,
            })
    });

    let serverAnswer = await response.json();
    if (serverAnswer.message == "item purchased") {
        window.location.replace(window.location.href);
    }
}

async function NewWishAdd() {
    let item = document.getElementById("newWishDesc").value;
    let price = document.getElementById("newwishprice").value;
    if (item == "") {
        alert("Must enter a wish");
        return false;
    }
    if (price == "") {
        alert("Must enter a price");
        return false;
    }

    let response = await fetch("/addwish", {
    method: 'POST',
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(
        {"item": item,
        "price": price})
    });

    let serverAnswer = await response.json();
    if (serverAnswer.message == "new wish added") {
        window.location.replace(window.location.href);
    }
}
});