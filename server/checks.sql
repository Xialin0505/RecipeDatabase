ALTER TABLE Recipe ADD CHECK (Fats >= 0);
ALTER TABLE Recipe ADD CHECK (Sugar >= 0);
ALTER TABLE Recipe ADD CHECK (Sodium >= 0);
ALTER TABLE Recipe ADD CHECK (Protein >= 0);
ALTER TABLE Recipe ADD CHECK (SaturatedFat >= 0);
ALTER TABLE Recipe ADD CHECK (Carbohydrates >= 0);
ALTER TABLE Recipe ADD CHECK (RecipeID >= 0);

ALTER TABLE RecipeMeta ADD CHECK (NumStep >= 0);
ALTER TABLE RecipeMeta ADD CHECK (NumIngredient >= 0);

ALTER TABLE RecipeWithReview ADD CHECK (RateCount5 >= 0);
ALTER TABLE RecipeWithReview ADD CHECK (RateCount4 >= 0);
ALTER TABLE RecipeWithReview ADD CHECK (RateCount3 >= 0);
ALTER TABLE RecipeWithReview ADD CHECK (RateCount2 >= 0);
ALTER TABLE RecipeWithReview ADD CHECK (RateCount1 >= 0);
ALTER TABLE RecipeWithReview ADD CHECK (RateCount0 >= 0);
ALTER TABLE RecipeWithReview ADD CHECK (OverallRate BETWEEN 0 AND 5);
ALTER TABLE RecipeWithReview ADD CHECK (ReviewNum >= 0);

ALTER TABLE Reviews ADD CHECK (Rating BETWEEN 0 AND 5);

ALTER TABLE Users ADD CHECK (TotalRateNumber >= 0); 

ALTER TABLE Author ADD CHECK (RecipeNum >= 0);
