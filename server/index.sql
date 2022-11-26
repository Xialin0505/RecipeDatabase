CREATE INDEX CookTimeIndex ON Recipe(CookTime);
CREATE INDEX CaloriesIndex ON Recipe(Calories);
CREATE INDEX FatsIndex ON Recipe(Fats);
CREATE INDEX SugarIndex ON Recipe(Sugar);
CREATE INDEX SodiumIndex ON Recipe(Sodium);
CREATE INDEX ProteinIndex ON Recipe(Protein);
CREATE INDEX SaturatedFatIndex ON Recipe(SaturatedFat);
CREATE INDEX CarbohydratesIndex ON Recipe(Carbohydrates);

CREATE INDEX IngredientNameIndex ON Ingredients(Name);

CREATE INDEX NumStepIndex ON RecipeMeta(NumStep);
CREATE INDEX NumIngredientIndex ON RecipeMeta(NumIngredient);
CREATE INDEX AuthorIndex ON RecipeMeta(Author);

CREATE INDEX OverallRateIndex ON RecipeWithReview(OverallRate);

