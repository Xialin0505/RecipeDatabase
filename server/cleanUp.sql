DROP TABLE IF EXISTS nutrition;
DROP TABLE IF EXISTS tmptech;
DROP VIEW IF EXISTS authors;

DELETE FROM Recipe WHERE RecipeID NOT IN (SELECT RecipeID FROM RecipeMeta);
