# Accountability App
### Video Demo:  <URL HERE>
### Description: 
This app was designed to help keep yourself and your friends hold each other accountable for goals you 
want to reach by keeping track of each other's goals and adding a competitive element to it. For partnership 
requests, you can send a request by searching for an existing username. You can also choose to reject 
a request as well as undo a rejection if it was a mistake or if you change your mind. 
For each goal that you set as complete, it must be accepted by one of your partners in the app in order to be 
fully approved. Once your goal is approved, the time taken to complete the goal is calculated by the minimum wage 
and added to your wallet. Each user has their own wallet as well as a wishlist of items that they would like 
to purchase. If you "earn" enough with each completed and approved task, you can purchase an item on your wishlist. 
Completed goals can also be rejected by partners if they believe that the time taken to complete the goal seems 
unrealistic or if they know you haven't actually completed the goal, and you have the choice to try taking on 
the goal again. 

#### Tables:
There are 5 tables: accounts, partnerships, goals, wishlist, transactions. The accounts table keeps track of user
information such as id, username, password, as well as the amount stored in their personal wallets. The partnership
table keeps track of partnerships between two users at a time as well as the status of their relationship
("ACCEPTED", "REQUESTED", "DENIED"). The goals table keeps track of individual goals, times of when each goal
starts and ends, which user this goal belongs to as well as the completion status ("PLANNED", "IN PROGRESS", "COMPLETED")
and acceptance status ("ACCEPTED", "NOT ACCEPTED") of each goal. The wishlist table keeps track of each item added to 
a wishlist, which user it belongs to, the price of the item, and the status of each item ("PURCHASED", "LISTED").
The transactions table keeps track of actions taken that affect users' wallets with a unique transaction id, the 
amount earned or spent, which user this action belongs to, the type of action ("EARNING", "SPENDING"), as well as
a timestamp.

#### Dockerfile and docker-compose-dev.yaml: 
The Dockerfile describes how a new image is built from the common Python image for version 3.12.
The source code of the entire project is copied into the image, and sessions and other unnecessary files are deleted.
It has instructions to install dependencies described in `requirements.txt` and to set up a working environment in `/app`.
Then, it instructs Flask to be used to start the web server.

Then, `docker-compose.yml` is run to build the image described in the Dockerfile and runs an actual container, specifying
which port it is run in. When changes are pushed to GitHub, GitHub Actions for building Docker images are used to 
build a new version of that image, so anyone who wishes to do so may spin up a container.

#### layout.html, apology.html, login.html and register.html: 
I created this app using some files that were used in the CS50 finance problem set as a base and built on top of those. 
As such, `layout.html` is where we can make the navigation bar so users can navigate between different pages. 
Similarly, the apology page `apology.html` uses Jinja to extend `layout.html` and inserts code into specific blocks.
`login.html` has a form for login that connects to `app.py("/login")` with a post request checking the user id 
and password information. `register.html` has a form for registering a new user which connects to 
`app.py("/register")` with a post request inserting the new user data and checking that the password is
correctly entered both times.

#### home.html: 
This is an introductory page accessible to both registered and non-registered people. This also extends `layout.html`.

### app.py and helpers.py, partners.py, timecalc.py, wallet.py

#### app.py: 
`app.py` is run by Flask to start the web server. It contains all the routes/endpoints used in the accountability app.
Some endpoints accept simple `GET` requests and render HTML, but most only accept and return different value objects in JSON format.
Other files like `helpers.py, goals.py, partners.py, timecalc.py, wallet.py` provide helper functions.

#### helpers.py 
This includes some original files from the CS50 finance project, such as the apology function that includes a 
function to replace special characters if needed. Similarly, there is the route for requiring logins. 
On top of these, there is a function for finding usernames and IDs to make things easier when 
having to find user information for SQL queries. There are also added functions to find the list of goals 
based on user id and adding new goals to the right user.

#### partners.py: 
Here, there are functions that will find a user's partners (this would mean that the request has 
been accepted). To differentiate between who has requested and who has answered the request (accept or deny), 
there are two functions that will provide two different lists of partnerships. One list is where the user is 
the requester and another is where the user is the acceptee. 
As well, there are helper methods to help find account information by username, partnership information by requester 
and acceptee user id numbers, and printing the right messages for when a user requests a partnership with 
another user.

#### timecalc.py: 
This contains functions to help calculate the time taken for a goal based on the goal id. One function is for 
completed goals and another is for if a goal is still in progress. There is also another function to calculate the 
time difference in hours to make it easier to calculate the income received for a completed task.

#### wallet.py: 
This has helper functions to find the current wallet value based on user id, the total sum of a user's wallet based on
total earnings and spending history, as well as a function to add new purchases or earnings into the transactions 
table. 

#### projectdata.db and log.sql: 
This is the sqlite3 database and a file to store schema to easily look back to when needed.

### In /static directory: javascript files
This directory has some files from the CS50 finance project (such as fav icon, I-heart-validator, styles.css).
Alongside it, it has pictures for the home page (2 jpg files that are freely accessible stock photo images) and 
javascript files `acceptgoals.js`, `goals.js`, `partnerlistnew.js`, `timefunctions.js`, and `wishlist.js`.

### In /templates directory: html files

#### findpartner.html: 
This page is where a user can find other users of the app by searching their usernames. This has input for searching 
for users to request a partnership with and script that connects to javascript file `static/findpartner.js`.

##### findpartner.js: 
This has an event listener for the input that fetches json data from `app.py("/searchpartner")` to find matching 
usernames to search result and inserts a button with class `add-partner-action` for each search result. It also 
has an event listener function for the buttons that fetch json data from `app.py("/addpartner-json")` to see if 
partnership can be requested, added to the database, and receive a response message for each relationship.

#### partnerlist.html: 
This page is where the user can see the status of their partnerships. This has a table and script that connects 
to file `/static/partnerlistnew.js`.

##### partnerlistnew.js: 
This fetches json data from `app.py("/requestedpartnerlist-json")` and `app.py("/acceptedpartnerlist-json")`. It 
makes a table that automatically updates the current user's partnerships (for all cases: requested, to respond, 
denied, accepted). There are buttons created based on the status of the partnership. Based on the status, the 
user has the option to either accept or deny a request for partnership they receive from another user. They 
also have the option to undo the status of a partnership that they've previously denied. These buttons are 
connected to `app.py("/answerpartnerrequest")` that sends the user id of the partnership and which action 
to take. Based on this, it will return the right message that will replace the message inside the button and disable 
the button once selected. 
  
#### seepartnergoals.html: 
This page allows the user to see the goals of their accepted partners. This has a table and 2 scripts. 
One script for calling time functions from `"/static/timefunctions.js"` and another connecting to 
`"/static/acceptgoals.js"`. 

##### timefunctions.js: 
This has a function for calculating the time difference based on inserted start and end time. There is also another 
function for calculating the time difference from start time and current time. 

##### acceptgoals.js: 
This updates the table of user's partners' goals. Based on the completion status of each goal, it 
shows the time taken for each goal (in progress or completed). The user can also choose to accept or deny a completed 
goal of their partners. These buttons are connected to functions that sends and fetches json data to and from 
`app.py("/partnergoalaction")`. It sends the id of the goal as well as which action to take for each goal.

#### maingoalpage.html: 
This page shows a table of the current user's goals. This has a table and 2 scripts, one script for calling 
time functions from `"/static/timefunctions.js"` and another connecting to `"/static/goals.js"`.
It also has an input and button for adding new goals.

##### timefunctions.js: 
This has a function for calculating the time difference based on inserted start and end time. It also has another 
function for calculating the time difference from start time and current time.

##### goals.js: 
Based on the completion status, a button with either a start or finish button are available. This will 
set a start or end time for the chosen goal as well as show the time difference for started and completed goals. 
There are also buttons for deleting a goal or redoing a goal that had been rejected by a partner. The `NewGoalAdd()`
function sends data in JSON format to `app.py("/addgoal")` to add a new goal from the input section of the site. The other 
button functions sends data in JSON format to `app.py("/goalaction")` which sends the goal id and the action to take 
for the chosen goal.

#### seewallets.html: 
This page has a table showing the user's partners' wallets alongside the user's own wallet. This information is 
simply updated using jinja and jinja environment functions defined in `helpers.py` (`find_username` and `find_wallet`).

#### wishlist.html: 
This page has a table showing a list of items in the current user's wishlist and their corresponding 
prices, a script connecting to `"/static/wishlist.js"`, and 2 inputs and one button for adding new items and their 
prices to the current user's wishlist.

##### wishlist.js: 
This updates the wishlist table with the current items on the user's wishlist by getting data with a requested 
to `app.py("/wishlist-json")`. Depending on the current user's wallet value, it will provide a button next
to each item for purchasing an item. If the wallet value is lower than the price of the item, it will show a message
saying that there are not enough funds. For the purchase button, there is a function `buttonPurchase()` that sends 
the item id to `app.py("/purchaseitem")` and updates the wishlist table in the database as well as the user's wallet 
value. There is also a function `NewWishAdd()` that sends information from the input fields (description and price) for a 
newly added item when the add button is clicked. this information is sent to `app.py("/addwish")` and inserts 
information on the new item to the wishlist database.



