# Accountability App
### Video Demo:  <URL HERE>
### Description: 
This app was designed to help keep yourself and your friends hold each other accountable for goals you 
want to reach by keeping track of each other's goals and adding a competitive element to it. For each goal that
you set as complete, it must be accepted by one of your partners in the app in order to be fully approved. Once 
your goal is approved, the time taken to complete the goal is calculated by the minimum wage and added to your wallet. 
Each user has their own wallet as well as a wishlist of items that they would like to purchase. If you "earn" enough
with each completed and approved task, you can purchase an item on your wishlist. Completed goals can also be rejected
by partners if they believe that the time taken to complete the goal seems unrealistic or if they know you haven't 
actually completed the goal, and you have the choice to try taking on the goal again. 
For partnership requests, you can send a request by searching for an existing username. You can also choose to reject 
a request as well as undo a rejection if it was a mistake or if you change your mind. 
#### Dockerfile and docker-compose-dev.yaml: 
The dockerfile gets the python interpreter to read the **requirements.txt** file to get the needed 
requirements listed there to make a copy of the right container type where the app can run when the flask run 
command is used. It also clears any already existing flask sessions and identifies where the working directory 
is for the app. The yaml file actually builds the container and tells it which port to be in.
#### layout.html and apology.html: 
These are mostly taken from the CS50 finance project. **layout.html** is where we can make the navigation bar 
so users can navigate between different pages. The apology page **apology.html** uses jinja to extend 
**layout.html** and inserts code into specific blocks. 
#### login.html and register.html: 
**login.html** has a form for login that connects to **app.py("/login")** with a post request checking the user id 
and password information. **register.html** has a form for registering a new user which connects to 
**app.py("/register")** with a post request inserting the new user data and checking that the password is 
correctly entered both times.
#### home.html: 
This is an introductory page accessible to both registered and non-registered people. This also extends **layout.html**.
### app.py and helpers.py, partners.py, timecalc.py, wallet.py
#### app.py: 
**app.py** is the main app file where we specify the routes for certain functions. mainly, what commands are run and 
which templates to render for certain addresses. It also has commands to jsonify data from python commands so 
that it can be used for javascript files.
**helpers.py**, **goals.py**, **partners.py**, **timecalc.py**, **wallet.py** are all helping files with functions 
that can be called when needed to make everything easier to read and more organized.
#### helpers.py 
This includes some original files from the CS50 finance project, such as the apology function that includes a 
function to replace special characters if needed. Similarly, there is the route for requiring logins. 
On top of these, there is a function for finding usernames and id numbers to make things easier when 
having to find user information for SQL queries. There are also added functions to find the list of goals 
based on user id and adding new goals to the right user.
#### partners.py: 
Here, there are functions that will find a user's partners (this would mean that the request has 
been accepted). To differentiate between who has requested and who has answered the request (accept or deny), 
there are two lists. One list is where the user is the requester and another is where the user is the acceptee. 
As well, there are functions to help find account information by username, partnership information by requester 
and acceptee user id numbers, and printing the right messages for when a user requests a partnership with 
another user.
#### timecalc.py: 
This contains functions to help calculate the time taken for a goal based on the goal id number. One function is for 
completed goals and another is for if a goal is still in progress. There is also another function to calculate the 
time difference in hours to make it easier to calculate the income received for a completed task. 
#### wallet.py: 
This has functions to make numeric values match the euro currency format ("," instead of "." for cent values), 
find a list of approved and completed tasks (tasks you can be paid for), find the total "money" spent 
on items from wishlist, and find the current wallet value based on user id number.  
#### projectdata.db and log.sql: 
This is the sqlite3 database and a file to store schema to easily look back to when needed.

### In /static directory: javascript files
This directory has some files from the CS50 finance project (such as fav icon and I-heart-validator, styles.css).
Alongside it, it has pictures for the home page (2 jpg that are freely accessible stock photo images) and 
javascript files **acceptgoals.js**, **goals.js**, **partnerlistnew.js**, **timefunctions.js**, and **wishlist.js**.
### In /templates directory: html files
#### findpartner.html: 
This has input for searching for users to request a partnership with and script that connects to 
javascript file **"static/findpartner.js"**.
##### findpartner.js: 
This has an event listener for the input that fetches json data from **app.py("/searchpartner")** to find matching 
usernames to search result and inserts a button with class ("add-partner-action") for each search result. It also 
has an event listener function for the buttons that fetches json data from **app.py("/addpartner-json")** to see if 
partnership can be requested, added to the database, and get the right response message.

#### partnerlist.html: 
This has a table and script that connects to file "**/static/partnerlistnew.js"**.
##### partnerlistnew.js: 
This fetches json data from **app.py("/requestedpartnerlist-json")** and **app.py("/acceptedpartnerlist-json")**. It 
makes a table that automatically updates the current user's partnerships (for all cases: requested, to respond, 
denied, accepted). There are buttons created based on the status of the partnership. Based on the status, the 
user has the option to either accept or deny a request for partnership they receive from another user. They 
also have the option to undo the status of a partnership that they've previously denied. These buttons are 
connected to **app.py("/answerpartnerrequest")** that sends the user id number of the partnership and which action 
to take. Based on this, it will return the right message that will replace the message inside the button and disable 
the button once selected. 
  
#### seepartnergoals.html: 
This has a table and 2 scripts. One script for calling time functions from **"/static/timefunctions.js"** and 
another connecting to **"/static/acceptgoals.js"**. This page allows the user to see the goals of their 
accepted partners.
##### timefunctions.js: 
This has a function for calculating the time difference based on inserted start and end time. There is also another 
function for calculating the time difference from start time and current time. 
##### acceptgoals.js: 
This updates the table of user's partners' goals. Based on the completion status of each goal, it 
shows the time taken for each goal (in progress or completed). The user can also choose to accept or deny a completed 
goal of their partners. These buttons are connected to functions that sends and fetches json data to and from 
**app.py("/partnergoalaction")**. it sends the id of the goal as well as which action to take for each goal.
#### maingoalpage.html: 
This has a table and 2 scripts, one script for calling time functions from **"/static/timefunctions.js"** 
and another connecting to **"/static/goals.js"**. This page shows a table of the current 
user's goals. it also has an input and button for adding new goals. 
##### timefunctions.js: 
This has a function for calculating the time difference based on inserted start and end time. It also has another 
function for calculating the time difference from start time and current time. 
##### goals.js: 
Based on the completion status, a button with either a start or finish button are available. This will 
set a start or end time for the chosen goal as well as show the time difference for started and completed goals. 
There are also buttons for deleting a goal or redoing a goal that had been rejected by a partner. The NewGoalAdd()
function sends jsonified data to **app.py("/addgoal")** to add a new goal from the input section of the site. The other 
button functions sends jsonified data to **app.py("/goalaction")** which sends the goal id number and the action to take 
for the chosen goal. 
#### seewallets.html: 
This page has a table showing the user's partners' wallets alongside the user's own wallet. This information is 
simply updated using jinja and jinja environment functions defined in **helpers.py** (find_username and find_wallet).
#### wishlist.html: 
This page has a table showing a list of items in the current user's wishlist and their corresponding 
prices, a script connecting to **"/static/wishlist.js"**, and 2 inputs and one button for adding new items and their 
prices to the current user's wishlist.
##### wishlist.js: 
This updates the wishlist table with the current items on the user's wishlist by getting data with a requested 
to **app.py("/wishlist-json")**. Depending on the current user's wallet value, it will provide a button next
to each item for purchasing an item. If the wallet value is lower than the price of the item, it will show a message
saying that there are not enough funds. For the purchase button, there is a function buttonPurchase() that sends 
the item id to **app.py("/purchaseitem")** and updates the wishlist table in the database as well as the user's wallet 
value. There is also a function NewWishAdd() that sends information from the input fields (description and price) for a 
newly added item when the add button is clicked. this information is sent to **app.py("/addwish")** and inserts 
information on the new item to the wishlist database.



