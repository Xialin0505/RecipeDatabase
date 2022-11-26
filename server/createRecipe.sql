DROP TABLE IF EXISTS tmptech;
DROP TABLE IF EXISTS nutrition;
DROP TABLE IF EXISTS RecipeMeta;
DROP TABLE IF EXISTS Recipe;

CREATE TABLE Recipe (
    RecipeID int UNIQUE NOT NULL PRIMARY KEY,
    RecipeName varchar(1000) NOT NULL,
    CookTime int,
    Description varchar(10000),
    Calories int,
    Fats int,
    Sugar int,
    Sodium int,
    Protein int,
    SaturatedFat int,
	Carbohydrates float(4,1),
	Techniques varchar(174) NOT NULL DEFAULT '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]',
	CHECK (RecipeID >= 0)
);


LOAD DATA INFILE
'/var/lib/mysql-files/02-Recipes/RAW_recipes.csv' IGNORE
INTO TABLE Recipe
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(RecipeName,RecipeID,CookTime,@ignore,@ignore,@ignore,@ignore,@ignore,@ignore,Description,@ignore,@ignore);


CREATE TABLE RecipeMeta (
    RecipeID int NOT NULL PRIMARY KEY,
    CreationDate datetime,
    Author int NOT NULL,
    NumStep int DEFAULT 1,
    NumIngredient int DEFAULT 1,
	CHECK (NumStep > 0),
	CHECK (NumIngredient > 0),
	FOREIGN KEY (Author) REFERENCES Users(UserID),
	FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID)  
	ON DELETE CASCADE
);

LOAD DATA INFILE
'/var/lib/mysql-files/02-Recipes/RAW_recipes.csv' IGNORE
INTO TABLE RecipeMeta
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(@ignore,RecipeID,@ignore,Author,CreationDate,@ignore,@ignore,NumStep,@ignore,@ignore,@ignore,NumIngredient);

CREATE TABLE nutrition (
	RecipeID int UNIQUE NOT NULL PRIMARY KEY,
	Calories float(6,1),
	Fats float(4,1),
	Sugar float(4,1),
	Sodium float(4,1),
	Protein float(4,1),
	SaturatedFat float(4,1),
	Carbohydrates float(4,1),
	FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID)
);

LOAD DATA INFILE
'/var/lib/mysql-files/Group28/nutrition.csv' IGNORE
INTO TABLE nutrition
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(RecipeID,Calories,Fats,Sugar,Sodium,Protein,SaturatedFat,Carbohydrates);


UPDATE Recipe INNER JOIN nutrition USING (RecipeID)
SET Recipe.Calories = nutrition.Calories, 
	Recipe.Fats = nutrition.Fats, 
	Recipe.Sugar = nutrition.Sugar, 
	Recipe.Sodium = nutrition.Sodium, 
	Recipe.Protein = nutrition.Protein, 
	Recipe.SaturatedFat = nutrition.SaturatedFat, 
	Recipe.Carbohydrates = nutrition.Carbohydrates;


CREATE TABLE tmptech (
	RecipeID int UNIQUE NOT NULL PRIMARY KEY,
	Techniques varchar(174) NOT NULL
);

LOAD DATA INFILE
'/var/lib/mysql-files/02-Recipes/PP_recipes.csv' IGNORE
INTO TABLE tmptech
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(RecipeID,@ignore,@ignore,@ignore,@ignore,Techniques,@ignore,@ignore);


UPDATE Recipe INNER JOIN tmptech USING (RecipeID)
SET Recipe.Techniques = tmptech.Techniques;
