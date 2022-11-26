DROP TABLE IF EXISTS RecipeWithReview;

CREATE TABLE RecipeWithReview (
    RecipeID int UNIQUE NOT NULL PRIMARY KEY,
    ReviewNum int DEFAULT 0 NOT NULL,
    OverallRate FLOAT(2,1) DEFAULT 0 NOT NULL,
    RateCount5 int DEFAULT 0 NOT NULL,
    RateCount4 int DEFAULT 0 NOT NULL,
    RateCount3 int DEFAULT 0 NOT NULL,
    RateCount2 int DEFAULT 0 NOT NULL,
    RateCount1 int DEFAULT 0 NOT NULL,
	RateCount0 int DEFAULT 0 NOT NULL,
	CHECK (RateCount5 >= 0),
	CHECK (RateCount4 >= 0),
	CHECK (RateCount3 >= 0),
	CHECK (RateCount2 >= 0),
	CHECK (RateCount1 >= 0),
	CHECK (RateCount0 >= 0),
	CHECK (OverallRate BETWEEN 0 AND 5),
	CHECK (ReviewNum > 0),
	FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID)
	ON DELETE CASCADE
);  

INSERT INTO RecipeWithReview (RecipeID,ReviewNum)
SELECT RecipeID,COUNT(UserID) AS num FROM Reviews GROUP BY RecipeID;


ALTER TABLE Reviews ADD FOREIGN KEY (RecipeID) REFERENCES RecipeWithReview(RecipeID) ON DELETE CASCADE;

WITH AvgR AS (
	SELECT RecipeID,AVG(Rating) AS AR FROM Reviews GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN AvgR USING(RecipeID)
SET RecipeWithReview.OverallRate = AvgR.AR;

WITH fistar AS (
	SELECT RecipeID,COUNT(RecipeID) AS five FROM Reviews WHERE Rating=5 GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN fistar USING(RecipeID)
SET RecipeWithReview.RateCount5 = fistar.five;

WITH fostar AS (
    SELECT RecipeID,COUNT(RecipeID) AS four FROM Reviews WHERE Rating=4 GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN fostar USING(RecipeID)
SET RecipeWithReview.RateCount4 = fostar.four;

WITH thstar AS (
    SELECT RecipeID,COUNT(RecipeID) AS three FROM Reviews WHERE Rating=3 GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN thstar USING(RecipeID)
SET RecipeWithReview.RateCount3 = thstar.three;

WITH twstar AS (
    SELECT RecipeID,COUNT(RecipeID) AS two FROM Reviews WHERE Rating=2 GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN twstar USING(RecipeID)
SET RecipeWithReview.RateCount2 = twstar.two;

WITH ostar AS (
    SELECT RecipeID,COUNT(RecipeID) AS one FROM Reviews WHERE Rating=1 GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN ostar USING(RecipeID)
SET RecipeWithReview.RateCount1 = ostar.one;

WITH zstar AS (
    SELECT RecipeID,COUNT(RecipeID) AS zero FROM Reviews WHERE Rating=0 GROUP BY RecipeID
)
UPDATE RecipeWithReview
INNER JOIN zstar USING(RecipeID)
SET RecipeWithReview.RateCount0 = zstar.zero;


