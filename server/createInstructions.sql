DROP TABLE IF EXISTS Instructions;

CREATE TABLE Instructions (
	RecipeID int NOT NULL,
	StepNumber int NOT NULL,
	Instruction varchar(1000) NOT NULL,
	CHECK (StepNumber > 0),
	CONSTRAINT PK_Instruction PRIMARY KEY (RecipeID,StepNumber),  
	FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID) ON DELETE CASCADE
);
	
LOAD DATA INFILE
'/var/lib/mysql-files/Group28/instructions.csv' IGNORE
INTO TABLE Instructions
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'

IGNORE 1 ROWS
(RecipeID,StepNumber,Instruction);
