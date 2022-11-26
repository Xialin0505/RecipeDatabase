import pandas as pd
import ast
import pickle
import os

# a tool to generate CSV file from raw data
# no need to run this agian as we already has all CSV files ready on marmoset server

def dump_ingr():

    ingr_map = pd.read_pickle('/Users/yuzhi/ECE356/ece356-project/dataset/ingr_map.pkl')

    ingr_df = ingr_map.copy(deep=True)
    ingr_df = ingr_df.rename({"id":"ingr_id","replaced":"ingr_name"}, axis="columns")

    ingr_df = ingr_df[["ingr_id","ingr_name"]]
    ingr_df = ingr_df.drop_duplicates(ignore_index=True)

    #ingr_df.to_csv('/home/x596liu/ECE356/project/ece356-project/dataset/ingrmap.csv')

    f = open('/Users/yuzhi/ECE356/ece356-project/dataset/ingrmap.csv', "w")
    f.write("IngredientID,Name\r\n") 

    token = list(ingr_df.ingr_id)
    name = list(ingr_df.ingr_name)

    for i in range(len(token)):
        ingredient_info = str(token[i])+",\""+name[i]+"\"\r\n"
        f.write(ingredient_info)

    f.close()

    # longest string length is 60 char
    #print(ingr_df.head(10))

def ingr_recipe():
    raw_recipes = pd.read_csv('/home/x596liu/ECE356/project/ece356-project/dataset/RAW_recipes.csv')
    ingr = pd.read_csv('/home/x596liu/ECE356/project/ece356-project/dataset/PP_recipes.csv')
    recipes = ingr.merge(right=raw_recipes, left_on="id", right_on="id")
    recipes = recipes[["id","name","submitted","ingredient_ids","ingredients","n_ingredients"]]
    
    recipes = recipes[['id','ingredient_ids']]
    recipes = recipes.rename({"id":"RecipeID","ingredient_ids":"ingredient"}, axis="columns")
    
    ingre = list(recipes.ingredient)
    RecipeID = list(recipes.RecipeID)

    f = open('/home/x596liu/ECE356/project/ece356-project/dataset/ingredients.csv', "w")
    f.write("RecipeID,Ingredient\r\n") 

    for x in range(len(RecipeID)):
        thisIngre = ast.literal_eval(ingre[x])
        
        for ins in range(len(thisIngre)):
            recipeInfo = str(RecipeID[x])+","+str(thisIngre[ins])+"\r\n"
            f.write(recipeInfo)

    f.close()
    


def dump_instr():
    instru = pd.read_csv('/Users/yuzhi/ECE356/ece356-project/dataset/RAW_recipes.csv')
    instru = instru[['id','steps']]
    instru = instru.rename({"id":"RecipeID","steps":"instructions"}, axis="columns")

    instruction = list(instru.instructions)
    RecipeID = list(instru.RecipeID)

    
    f = open('/Users/yuzhi/ECE356/ece356-project/dataset/instructions.csv', "w")
    f.write("RecipeID,StepNum,Instruction\r\n") 

    for x in range(len(RecipeID)):
        thisInstruction = ast.literal_eval(instruction[x])
        
        for ins in range(len(thisInstruction)):
            recipeInfo = str(RecipeID[x])+","+str(ins+1)+",\""+thisInstruction[ins]+"\"\r\n"
            f.write(recipeInfo)

    f.close()
    
    '''''
    max_len = 0
    max_string = ''

    for x in range(len(RecipeID)):
        thisInstruction = ast.literal_eval(instruction[x])

        for i in range(len(thisInstruction)):
            thisInstruction[i] = str(thisInstruction[i])
            if (max_len < len(thisInstruction[i])):
                max_len = len(thisInstruction[i])
                max_string = thisInstruction[i]

    print (max_len)
    print (max_string)

    '''

def dump_nutrition():
    nutri = pd.read_csv('/home/x596liu/ECE356/project/ece356-project/dataset/RAW_recipes.csv')
    nutri = nutri[['id','nutrition']]
    nutri = nutri.rename({"id":"RecipeID"}, axis="columns")

    nutrition = list(nutri.nutrition)
    RecipeID = list(nutri.RecipeID)

    f = open('/home/x596liu/ECE356/project/ece356-project/dataset/nutrition.csv', "w")
    f.write("RecipeID,Calories,TotalFat(PDV),Sugar(PDV),Sodium(PDV),Protein(PDV),SaturatedFat(PDV),Carbohydrates(PDV)\r\n") 

    for x in range(len(RecipeID)):
        thisNutrition = ast.literal_eval(nutrition[x])
        
        for ins in range(len(thisNutrition)):
            nutritionInfo = str(RecipeID[x])
            for n in thisNutrition:
                nutritionInfo += ","+str(n)
                
            nutritionInfo+="\r\n"
            #print(nutritionInfo)
            f.write(nutritionInfo)

    f.close()

def dump_tags():
    tags = pd.read_csv('/home/x596liu/ECE356/project/ece356-project/dataset/RAW_recipes.csv')
    tags = tags[['id','tags']]
    tags = tags.rename({"id":"RecipeID"}, axis="columns")

    tag = list(tags.tags)
    RecipeID = list(tags.RecipeID)

    '''
    f = open('/home/x596liu/ECE356/project/ece356-project/dataset/tags.csv', "w")
    f.write("RecipeID,StepNum,Instruction\r\n") 

    for x in range(len(RecipeID)):
        thisTag = ast.literal_eval(tag[x])
        
        for t in range(len(thisTag)):
            recipeTags = str(RecipeID[x])+","+str(t+1)+",\'"+thisTag[t]+"\'\r\n"
            #print(recipeTags)
            f.write(recipeTags)

    f.close()
    '''
    max_len = 0
    max_string = ''

    for x in range(len(RecipeID)):
        thisTag = ast.literal_eval(tag[x])

        for i in range(len(thisTag)):
            thisTag[i] = str(thisTag[i])
            if (max_len < len(thisTag[i])):
                max_len = len(thisTag[i])
                max_string = thisTag[i]

    print (max_len)
    print (max_string)

def count_comment():
    comments = pd.read_csv('/home/x596liu/ECE356/project/ece356-project/dataset/RAW_interactions.csv')
    comment = list(comments.review)
    
    max_len = 0
    max_string = ''
    for i in range(len(comment)):
        comment[i] = str(comment[i])
        if (max_len < len(comment[i])):
            max_len = len(comment[i])
            max_string = comment[i]

    print (max_len)
    print (max_string)


def Technique_Count():
    tech = pd.read_csv('/home/x596liu/ECE356/project/ece356-project/dataset/PP_recipes.csv')
    techs = list(tech.techniques)

    print(techs[1])
    print(len(techs[1]))

dump_ingr()