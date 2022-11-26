import os
from typing import Counter
import mysql.connector as con
from mysql.connector import errorcode
from datetime import datetime
#import pandas as pd
import ast
import sys
from random import randint

class User():
    def __init__(self, id):
        self.id = id

# Initialize global user with -1 as id to differentiate from actual user id
globalUser = User(-1)

# Connecting to mysql server using mysql.connector
# returns connection
def ConnectDatabase():
    try:
        cnx = con.connect(user='x596liu',password='ECE356.grp28',host='marmoset04.shoshin.uwaterloo.ca',database='db356_x596liu')
        return cnx
    except con.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

# Helper function to update user's activity time
def updateLastInteractionTime():
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    currentTime = datetime.now(tz=None)
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    currentTime = "\'"+currentTime+"\'"

    query = ("UPDATE Users SET LastInteractionTime={} WHERE UserID={}".format(currentTime, globalUser.id))
    cursor.execute(query)

    cursor.close()
    cnx.close()

# Helper function for printing list of results
def printResult(resultName, result):
    print(resultName+"s: ")
    for i in range(len(result)):
        for j in range(len(result[i])):
            print(resultName+str(i+1)+": "+str(result[i][j]).replace("'",''))
    print("\n")

# Formatted printing for displaying one recipe
def printRecipe(result,cursor):

    for i in range(len(result)):
        for j in range(len(result[i])):
	# 11th place is reserved for techniques
            if (j == 11):
                printTech(result[i][j])
            elif (j == 1):
                print(str(RECIPE_ATTRIBUTES_LIST[j])+": "+ str(result[i][j]))
                recipeID=str(result[i][0])
                query = ("SELECT ReviewNum,OverallRate FROM RecipeWithReview WHERE RecipeID={}".format(recipeID))
                cursor.execute(query)
                review = cursor.fetchone()
                if (review == None):
                    print("Review number: 0")
                    print("Overall rate: NA")
                else:
                    print("Review number: {}".format(str(review[0])))
                    print("Overall rate: {}".format(str(review[1])))
            else:
                print(str(RECIPE_ATTRIBUTES_LIST[j])+": "+ str(result[i][j]))
        print("\n")

# formatted printting of details for given recipe ID (from Recipe table)
def displayRecipeByID(recipeID,cnx):
    print("\n")
    query = ("WITH rcp AS (SELECT * FROM Recipe WHERE RecipeID={}) SELECT * FROM rcp INNER JOIN RecipeMeta USING(RecipeID)".format(recipeID))
    newCursor = cnx.cursor()
    newCursor.execute(query)

    result = newCursor.fetchall()
    printRecipe(result,newCursor)
    newCursor.close()

# formatted printting of ingredient for given recipe ID
def printIngredient(RecipeID,cnx):
    cursor = cnx.cursor()
    query = ("SELECT Name FROM RecipeIngredient INNER JOIN Ingredients USING(IngredientID) WHERE RecipeID={}".format(RecipeID))
    cursor.execute(query)
    
    result = cursor.fetchall()
    if (result == None):
        print("No ingredient for this recipe")
        return

    outputList = []
    for i in result:
        outputList.append(i[0])
    
    print("Ingredients: "+",".join(outputList))

    cursor.close()
    

# Formatted printing for comments
def printComment(result):
    print("Comments: ")
    for i in range(len(result)):
        for j in range(len(result[i])):
            print(result[i][j])
        print("\n")

# Converts user input into bitstring
# 0: technique not used
# 1: technique is used
def techConvert(techList):
# Default: none of the techniques are used
    resultList = 58*[0]

    if (techList != None):
	# Get index based on string and set the bit to 1
        for techniques in techList:
            index = TECHNIQUES_LIST.index(techniques)
            resultList[index] = 1
    
    resultStr = ",".join([str(x) for x in resultList])
    return "\"["+resultStr+"]\""

# Helper function for inserting instructions inputs
def inputSteps(recipeID,cursor,cnx):
# stepNum counter used for updating RecipeMeta for data consistency
# stepNum counter also used for maintaining instructions order
    stepNum = 1
    print("Type \'finish\' to finish")
    
    step = ''
    
    while (step != "finish"):
        step = input("Enter your step{}: ".format(stepNum))

        if (step == "finish" and stepNum == 1):
            print("You must input instructions.")
            step = ''
            continue
        elif (step == "finish"):
            break
        
        query = ("INSERT INTO Instructions VALUES ({},{},{})".format(recipeID,stepNum,"\'"+step+"\'"))
        cursor.execute(query)
        cnx.commit()

        stepNum += 1
    
    query = ("UPDATE RecipeMeta SET NumStep={} WHERE RecipeID={}".format(stepNum-1, recipeID))
    cursor.execute(query)
    cnx.commit()

# Helper function for inserting ingredient inputs
def inputIngredient(recipeID,cursor,cnx):
    print("Type \'finish\' to finish")
# numIngr counter used for updating RecipeMeta for data consistency
    numIngr = 1

    ingr = ''

    while (ingr != "finish"):
        ingr = input("Enter your ingredient: ")
        if (ingr == "finish" and numIngr == 1):
            print("You must input ingredient.")
            ingr = ''
            continue
        elif (ingr == "finish"):
            break

        query = ("SELECT IngredientID FROM Ingredients WHERE Name={}".format("\'"+ingr+"\'"))
        cursor.execute(query)
	
	# Client must choose ingredients from our list of ingredients
        ingrID = cursor.fetchone()
        if (ingrID == None):
            print("Invalid ingredient, choose another one")
        else:
            query = ("INSERT INTO RecipeIngredient VALUES({},{})".format(recipeID,ingrID[0]))
            cursor.execute(query)
            cnx.commit()
            numIngr += 1


    query = ("UPDATE RecipeMeta SET NumIngredient={} WHERE RecipeID={}".format(numIngr-1,recipeID))
    cursor.execute(query)
    cnx.commit()
    
# Helper function for techniques input
# Returns techniques used bitstring
def inputTechs():
    print("Type \'finish\' to finish")
    tech = input("Technique: ")
    techList = []

    while (tech != "finish"):
	# Client must choose from out list of techniques
        try:
            index = TECHNIQUES_LIST.index(tech)
            techList.append(tech)
        except:
            print("Invalid technique, please enter another one.")

        tech = input("Technique: ")

    # Converting string to bitstring
    return techConvert(techList)

# Helper function for tags input
def inputTags(recipeID,cursor,cnx):
# tagNum counter assigns number to each tag of the same recipe
    tagNum = 1
    print("Type \'finish\' to finish")

    tag = input("Enter your tag{}: ".format(tagNum))

    while (tag != "finish"):
        query = ("INSERT INTO Tags VALUES ({},{},{})".format(recipeID,tagNum,"\'"+tag+"\'"))
        cursor.execute(query)
        cnx.commit()

        tagNum += 1
        tag = input("Enter your tag{}: ".format(tagNum))

# Helper function for printing techniques
def printTech(tech):

    if (len(tech) != 0):
        techList = ast.literal_eval(tech)
        outputList = []

        # Converting bitstring to string
        for i in range(len(techList)):
            if techList[i] == 1:
                outputList.append(TECHNIQUES_LIST[i])

        print(RECIPE_ATTRIBUTES_LIST[11]+": "+",".join(outputList))
    else:
        print(RECIPE_ATTRIBUTES_LIST[11]+": ")


TECHNIQUES_LIST = [
    'bake',
    'barbecue',
    'blanch',
    'blend',
    'boil',
    'braise',
    'brine',
    'broil',
    'caramelize',
    'combine',
    'crock pot',
    'crush',
    'deglaze',
    'devein',
    'dice',
    'distill',
    'drain',
    'emulsify',
    'ferment',
    'freez',
    'fry',
    'grate',
    'griddle',
    'grill',
    'knead',
    'leaven',
    'marinate',
    'mash',
    'melt',
    'microwave',
    'parboil',
    'pickle',
    'poach',
    'pour',
    'pressure cook',
    'puree',
    'refrigerat',
    'roast',
    'saute',
    'scald',
    'scramble',
    'shred',
    'simmer',
    'skillet',
    'slow cook',
    'smoke',
    'smooth',
    'soak',
    'sous-vide',
    'steam',
    'stew',
    'strain',
    'tenderize',
    'thicken',
    'toast',
    'toss',
    'whip',
    'whisk',
]

RECIPE_ATTRIBUTES_LIST = [
    'Recipe ID',
    'Recipe Name',
    'Cook Time',
    'Description',
    'Calories',
    'Fats',
    'Sugar',
    'Sodium',
    'Protein',
    'SaturatedFat',
    'Carbohydrates',
    'Techniques',
    'Creation Date',
    'Author',
    'Number of step',
    'Number of ingredient'
]
