
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    UserID int UNIQUE NOT NULL PRIMARY KEY,
    FirstName varchar(20),
    LastName varchar(20),
    Constraints int NOT NULL DEFAULT 0,
    LastInteractionTime datetime,
    TotalRateNumber int NOT NULL DEFAULT 0, 
	CHECK (TotalRateNumber >= 0),
	CHECK (Constraints BETWEEN 0 AND 1),
	CHECK (UserID > 0)
);

LOAD DATA INFILE
'/var/lib/mysql-files/02-Recipes/RAW_interactions.csv' IGNORE
INTO TABLE Users
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(UserID,@ignore,@ignore,@ignore,@ignore);

CREATE TABLE Reviews (
	RecipeID int NOT NULL,
	UserID int NOT NULL,
	Comments varchar(500),
	Rating int NOT NULL DEFAULT 0,
	ReviewDate datetime,
	CHECK (Rating BETWEEN 0 AND 5),
	CONSTRAINT PK_Reviews PRIMARY KEY (RecipeID,UserID),
	FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

LOAD DATA INFILE
'/var/lib/mysql-files/02-Recipes/RAW_interactions.csv' IGNORE
INTO TABLE Reviews
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(UserID,RecipeID,ReviewDate,Rating,Comments);

