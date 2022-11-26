CREATE TABLE Interactions (
    UserID int NOT NULL,
    RecipeID int NOT NULL,
    InterationDate datetime,
    Rating int,
    Comments varchar(600),
    FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    PRIMARY KEY (UserID,RecipeID,InterationDate)
);

LOAD DATA INFILE
'/var/lib/mysql-files/02-Recipes/RAW_interactions.csv' IGNORE
INTO TABLE Interactions
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(UserID,RecipeID,InterationDate,Rating,Comments);
