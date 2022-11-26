CREATE VIEW tmpReview AS SELECT UserID,count(*) as NumReviews,max(ReviewDate) as LastInteration FROM Reviews group by UserID;

UPDATE Users
INNER JOIN tmpReview ON Users.UserID = tmpReview.UserID
SET Users.TotalRateNumber = tmpReview.NumReviews;

UPDATE Users
INNER JOIN tmpReview ON Users.UserID = tmpReview.UserID
SET Users.LastInteractionTime = tmpReview.LastInteration;

DROP VIEW IF EXISTS tmpReview;

CREATE VIEW authors AS SELECT DISTINCT Author FROM RecipeMeta;

UPDATE Users
INNER JOIN authors ON authors.Author = Users.UserID
SET Users.Constraints = 1;

CREATE TABLE onlyauthors AS (SELECT * from authors where authors.Author NOT IN (SELECT UserID from Users));
INSERT INTO Users (UserID) SELECT (Author) FROM onlyauthors;


UPDATE Users
INNER JOIN onlyauthors ON onlyauthors.Author = Users.UserID
SET Users.Constraints = 1;


DROP VIEW IF EXISTS authors;
DROP TABLE IF EXISTS onlyauthors;


