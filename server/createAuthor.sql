DROP TABLE IF EXISTS Author;
DROP VIEW IF EXISTS authors;
CREATE VIEW authors AS SELECT DISTINCT Author FROM RecipeMeta;

CREATE TABLE Author (
	UserID int UNIQUE NOT NULL PRIMARY KEY,
	RecipeNum int DEFAULT 1,
	OverallRate float(2,1) DEFAULT 0,
	CHECK (RecipeNum > 0),
	CHECK (OverallRate >= 0),
	FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

INSERT INTO Author (UserID)
SELECT * FROM authors;


WITH Overall AS (
		SELECT Author,avg(OverallRate) AS OvR FROM RecipeWithReview INNER JOIN RecipeMeta USING(RecipeID) GROUP BY Author
)UPDATE Author INNER JOIN Overall ON Author.UserID = Overall.Author SET Author.OverallRate = Overall.OvR;


WITH rcpN AS (
		SELECT Author,COUNT(RecipeID) AS recps FROM RecipeMeta GROUP BY Author
)UPDATE Author INNER JOIN rcpN ON Author.UserID = rcpN.Author SET Author.RecipeNum = rcpN.recps;

