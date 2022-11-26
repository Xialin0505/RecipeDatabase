DROP TABLE IF EXISTS RecipeIngredient;
DROP TABLE IF EXISTS Ingredients;

CREATE TABLE Ingredients (
    IngredientID int UNIQUE NOT NULL PRIMARY KEY,
	Name varchar(60) UNIQUE NOT NULL
);

LOAD DATA INFILE
'/var/lib/mysql-files/Group28/ingrmap.csv' IGNORE
INTO TABLE Ingredients
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(IngredientID,Name);

CREATE TABLE RecipeIngredient (
	RecipeID int NOT NULL,
	IngredientID int NOT NULL,
	CONSTRAINT PK_RecipeIngredient PRIMARY KEY (RecipeID,IngredientID),
	FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID) ON DELETE CASCADE,
	FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID) ON DELETE CASCADE
);

LOAD DATA INFILE
'/var/lib/mysql-files/Group28/ingredients.csv' IGNORE
INTO TABLE RecipeIngredient
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(RecipeID,IngredientID);


