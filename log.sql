'''record of tables used for this project!'''
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    wallet NUMERIC NOT NULL DEFAULT 1.00
);

"""this ensures that there are no repeated values in said column"""
CREATE UNIQUE INDEX username ON accounts (username);

CREATE TABLE partnerships (
    requester INT,
    acceptee INT,
    status TEXT NOT NULL,
    PRIMARY KEY (requester, acceptee),
    FOREIGN KEY (requester) REFERENCES accounts (id),
    FOREIGN KEY (acceptee) REFERENCES accounts (id)
);

CREATE TABLE goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT,
    goalDescription TEXT NOT NULL,
    completionStatus TEXT NOT NULL,
    acceptanceStatus TEXT NOT NULL,
    timeStart INT,
    timeEnd INT,
    FOREIGN KEY (user_id) REFERENCES accounts(id)
);

CREATE TABLE wishlist (
    wish_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT,
    wishDescription TEXT NOT NULL,
    price INT,
    wishStatus TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(id)
);

### wishStatus can be LISTED or PURCHASED