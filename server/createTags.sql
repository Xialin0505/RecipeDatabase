DROP TABLE IF EXISTS Tags;

CREATE TABLE Tags (
    RecipeID int NOT NULL,
    TagNumber int NOT NULL,
    Tag varchar(80) NOT NULL,
    CONSTRAINT PK_Tags PRIMARY KEY (RecipeID,TagNumber),
    FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID) ON DELETE CASCADE
);

LOAD DATA INFILE
'/var/lib/mysql-files/Group28/tags.csv' IGNORE
INTO TABLE Tags
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(RecipeID,TagNumber,Tag);