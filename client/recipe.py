from utility import *

# create a new recipe for logon user
def createRecipe():
    #establish connection
    print("Create recipe")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    # gather recipe detailed info from user
    recipeName = ''
    while (len(recipeName) == 0):
        recipeName = input("Recipe name: ")
        if (len(recipeName) == 0):
            print("Recipe must have a name")
    
    recipeName = "\'"+recipeName+"\'"
    print(recipeName)

    tech = inputTechs()
    cookTime = input("Cook time: ")
    description = input("Description: ")
    calories = input("Calories: ")
    fats = input("Fats: ")
    sugar = input("Sugar: ")
    sodium = input("Sodium: ")
    protein = input("Protein: ")
    saturatedFat = input("SaturatedFat: ")
    carbohydrates = input("Carbohydrates: ")

    # assign a new ID for the recipe to be created
    query = ("SELECT max(RecipeID) FROM Recipe")
    cursor.execute(query)
    maxID = cursor.fetchone()
    maxID = maxID[0]
    newID = maxID + randint(1,5)*randint(3,10)

    # deal with no input for optional attributes
    if (len(cookTime) == 0): cookTime = "0"
    if (len(description) == 0): 
        description = "NULL"
    else:
        description = "\'"+description+"\'"
    if (len(calories) == 0): calories = "NULL"
    if (len(fats) == 0): fats = "NULL"
    if (len(sugar) == 0): sugar = "NULL"
    if (len(sodium) == 0): sodium = "NULL"
    if (len(protein) == 0): protein = "NULL"
    if (len(carbohydrates) == 0): carbohydrates = "NULL"
    if (len(saturatedFat) == 0): saturatedFat = "NULL"

    query = ("INSERT INTO Recipe VALUES ({},{},{},{},{},{},{},{},{},{},{},{})"\
            .format(newID,recipeName,cookTime,description,calories,fats,sugar,sodium,protein,saturatedFat,carbohydrates,tech))

    cursor.execute(query)
    cnx.commit()
    
    # get the recipe creation time
    currentTime = datetime.now(tz=None)
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    currentTime = "\'"+currentTime+"\'"
    query = ("INSERT INTO RecipeMeta (RecipeID,CreationDate,Author) VALUES ({},{},{})".format(newID,currentTime,globalUser.id))
    cursor.execute(query)
    cnx.commit()
    
    inputSteps(newID,cursor,cnx)
    inputTags(newID,cursor,cnx)
    inputIngredient(newID,cursor,cnx)
    
    # update Users/Author table
    query = ("SELECT Constraints FROM Users WHERE UserID={}".format(globalUser.id))
    cursor.execute(query)

    constraint = cursor.fetchone()[0]
    # upgrade user to author if that is the first recipe this user creates 
    if (constraint == 0):
        query = ("INSERT INTO Author (UserID,RecipeNum) VALUES ({},1)".format(globalUser.id))
        cursor.execute(query)
        cnx.commit()
    else:
        query = ("UPDATE Author SET RecipeNum=RecipeNum+1 WHERE UserID={}".format(globalUser.id))
        cursor.execute(query)
        cnx.commit()
    
    query = ("UPDATE Users SET Constraints=1 WHERE UserID={}".format(globalUser.id))
    cursor.execute(query)
    cnx.commit()

    print("Your recipe has been successfully created")
    
    cursor.close()
    cnx.close()
    
def viewMyRecipe():
    print("View my recipe")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    # create a view for all the recipe user has
    try:
        query = ("CREATE VIEW Filtered AS (SELECT RecipeID FROM RecipeMeta INNER JOIN Recipe USING (RecipeID) WHERE Author=\'{}\')".format(globalUser.id))
        cursor.execute(query)
        cnx.commit()
    except:
        query = ("DROP VIEW IF EXISTS Filtered")
        cursor.execute(query)
        cnx.commit()

        query = ("CREATE VIEW Filtered AS (SELECT RecipeID FROM RecipeMeta INNER JOIN Recipe USING (RecipeID) WHERE Author=\'{}\')".format(globalUser.id))
        cursor.execute(query)
        cnx.commit()

    # print out uer's recipe 
    displayRecipe(cursor,cnx)

    cursor.close()
    cnx.close()

def displayRecipe(cursor,cnx):

    try:
        query = ("SELECT * FROM Recipe INNER JOIN Filtered USING(RecipeID) INNER JOIN RecipeMeta USING (RecipeID)")
        cursor.execute(query)
    except:
        query = ("DROP VIEW IF EXISTS Filtered")
        cursor.execute(query)
        cnx.commit()

        query = ("SELECT * FROM Recipe INNER JOIN Filtered USING(RecipeID) INNER JOIN RecipeMeta USING (RecipeID)")
        cursor.execute(query)

    allRecipes = cursor.fetchmany(10)
    if (len(allRecipes) == 0):
        print("You don't have recipe yet.")
        cursor.close()
        cnx.close()
        return

    # display recipe in a set of ten
    while (len(allRecipes) != 0):
        printRecipe(allRecipes,cursor)
        
        # total recipe is less than 10 
        if (len(allRecipes) < 10):
            print("No more recipe.")
            break

        more = input("to see more type \'Yes\', otherwise type \'No\' to exit: ")
        if (more == "No"):
            break
        else:
           allRecipes = cursor.fetchmany(10)
           if (len(allRecipes)==0):
               print("No more recipe.")

    query = ("DROP VIEW IF EXISTS Filtered")
    cursor.execute(query)
    cnx.commit()

# search for recipes bosed on customized filter
def searchRecipe():
    print("Search recipe")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    cursor = filter(cursor,cnx)

    result = cursor.fetchmany(500)
    if (len(result)==0):
        print("No more recipe.")
        cursor.close()
        cnx.close()
        return
    else:
        try:
            cursor.fetchall()
        except:
            pass
    # print out result found
    i = 0
    while(i < len(result)):
        for j in range(10):
            if i >= len(result):
                print("No more recipe.")
                break
            
            displayRecipeByID(result[i][0],cnx)
            i += 1
        if (i >= len(result)):
            break
        more = input("to see more type \'Yes\', otherwise type \'No\' to exit: ")
        if (more == "No"):
            break 


    cursor.close()
    cnx.close()

# search for recipes bosed on given ID 
# gave the most detailed info of a recipe
# indcluding all its review displayed in a set of 10
def searchRecipeByID():
    print("Search recipe by its ID")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    while(True):
        RecipeID = input("Enter recipe ID: ")

        print("\n")

        query = ("WITH rcp AS (SELECT * FROM Recipe WHERE RecipeID={}) \
                SELECT * FROM rcp INNER JOIN RecipeMeta USING(RecipeID)".format(RecipeID))
        cursor = cnx.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        if len(result) == 0:
            print("Invalid RecipeID, please enter another")
        else:
            break
    
    printRecipe(result,cursor)
    
    query = ("SELECT Instruction FROM Instructions WHERE RecipeID={}".format(RecipeID))
    cursor.execute(query)

    result = cursor.fetchall()
    printResult("Instruction", result)

    query = ("SELECT Tag FROM Tags WHERE RecipeID={}".format(RecipeID))
    cursor.execute(query)

    result = cursor.fetchall()
    printResult("Tag", result)

    query = ("WITH rcp AS (SELECT RecipeID,IngredientID FROM RecipeIngredient WHERE RecipeID={}) \
                SELECT Name FROM rcp INNER JOIN Ingredients USING(IngredientID)".format(RecipeID))
    
    cursor.execute(query)
    result = cursor.fetchall()
    printResult("Ingredient", result)
    
    # get review info from Reviews table
    query = ("SELECT RecipeID,Comments,Rating,ReviewDate FROM Reviews WHERE RecipeID={}".format(RecipeID))
    cursor.execute(query)
    result = cursor.fetchmany(10)
    if (len(result) == 0):
        cursor.close()
        cnx.close()
        return
    
    while len(result) != 0:
        # display 10 reviews each time
        for row in result:
            print("-------------------")
            print("Recipe ID: " + str(row[0]))
            print("Comments: " + str(row[1]))
            print("Rating: " + str(row[2]))
            print("Review date: " + str(row[3]))
        
        if (len(result) < 10):
            break
        more = input("to see more type \'Yes\', otherwise type \'No\' to exit: ")
        if (more == "No"):
            cursor.fetchall()
            break
        else:
            result = cursor.fetchmany(10)   

    cursor.close()
    cnx.close()

def filter(cursor,cnx):

    #attribute
    whereMapping = {
        0 : "RecipeName",
        1 : "Author",
        2 : "OverallRate",
        3 : "CookTime",
        4 : "Tag",
        5 : "NumIngredient",
        6 : "Ingredient",
        7 : "NumStep"
    }

    # Table
    attributeMapping = {
        0 : "Recipe",
        1 : "RecipeMeta",
        2 : "RecipeWithReview",
        3 : "Recipe",
        4 : "Tags",
        5 : "RecipeMeta",
        6 : "RecipeIngredient",
        7 : "RecipeMeta"
    }

    print("Adding filter in the following order seperated by \':\':")

    
    print("key word:authorID:rate inveral:cook time(in minutes) interval:tag:number of ingredient inverval:ingredients:number of steps interval")
    print("please use the same format as the sample input below:")
    print("egg:[89831,37449,37779,89831,1533]:[2,5]:[20,60]:[\"healthy\",\"vegetarian\"]:[2,10]:[\"plum\",\"egg\"]:[0,10]")
    print("If don't want to specify a criteria, please type \'NULL\' in corresponding field")

    filter = input("Enter your filter: ")

    filterList = filter.split(':')


    joinList = []
    whereNum = []

    withClause = "WITH {} AS (SELECT RecipeID FROM {} WHERE {})" 
    query = "WITH "

    for i in range(len(filterList)):
        if (filterList[i] == "NULL"):
            continue

        if (i != 0):
            joinList.append(attributeMapping[i])
            try:
                cond = ast.literal_eval(filterList[i])
            except:
                print("Invalid input.")
                return curosr

            if (len(cond) != 8):
                print("Invalid input.")
                return cursor

        # filter every relavent table based on user input
        if (i == 1):
            whereClause = whereMapping[i]+" IN ("+str(cond[0])
            for j in range(1,len(cond)):
                whereClause += ","+str(cond[j])
            whereClause += ")"
            whereNum.append("tmp"+str(i))
            query += 'tmp{} AS (SELECT RecipeID FROM {} WHERE {}),'.format(i,attributeMapping[i],whereClause)
        elif (i == 4):
            whereClause = whereMapping[i]+" IN (\'"+str(cond[0])+"\'"
            for j in range(1,len(cond)):
                whereClause += ",\'"+str(cond[j])+"\'"
            whereClause += ")"
            whereNum.append("tmp"+str(i))
            query += 'tmp{} AS (SELECT RecipeID FROM {} WHERE {}),'.format(i,attributeMapping[i],whereClause)
        elif (i == 6):
            ingrList = []
            for ingr in cond:
                ingre_query = ("SELECT IngredientID FROM Ingredients WHERE Name=\'{}\'".format(ingr))
                cursor.execute(ingre_query)
                ingrList.append(str(cursor.fetchone()[0]))
            whereNum.append("tmp"+str(i))
            whereClause = "IngredientID IN ({})".format(",".join(ingrList))
            query += 'tmp{} AS (SELECT DISTINCT RecipeID FROM RecipeIngredient WHERE {}),'.format(i,whereClause)
        elif (i == 2 or i == 3 or i == 5 or i == 7):
            whereClause = whereMapping[i]+" BETWEEN "+str(cond[0])+" AND "+str(cond[1])
            whereNum.append("tmp"+str(i))
            query += 'tmp{} AS (SELECT RecipeID FROM {} WHERE {}),'.format(i,attributeMapping[i],whereClause)
        elif (i == 0):
            filterList[0] = filterList[0].replace("'","\\'")
            whereClause = whereMapping[i]+" LIKE \'%{}%\'".format(filterList[0])
            whereNum.append("tmp"+str(i))
            query += 'tmp{} AS (SELECT RecipeID FROM {} WHERE {}),'.format(i,attributeMapping[i],whereClause)

    # inner joint these filtered table
    # return resulting recipe ID 
    if (len(whereNum) == 0):
        query = "SELECT RecipeID FROM Recipe"
    else:
        query = query[:-1]
        query += "SELECT RecipeID FROM Recipe "  
        for t in range(len(whereNum)):
            query += " INNER JOIN " + whereNum[t] + " USING(RecipeID)"

    cursor.execute(query)
    return cursor

def modifyRecipe():
    print("Modify your recipe")
    recipeID = input("Enter recipe id that you want to modify: ")

    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    query = ("SELECT Author FROM RecipeMeta WHERE RecipeID={}".format(recipeID))
    cursor.execute(query)

    author = cursor.fetchone()
    
    # sanity check for inout ID
    if (author == None):
        print("Cannot find the recipe")
        cursor.close()
        cnx.close()
        return
    elif (str(author[0]) != str(globalUser.id)):
        print("You can only modify your own recipe")
        cursor.close()
        cnx.close()
        return
    else:
        # ask for attributes to be modified
        print("Type \'finish\' to finish")
        while (True):
            print("Which attribute you want to modify?\n \
                    RecipeName\n \
                    Instructions\n \
                    Ingredients\n \
                    Tags\n \
                    CookTime\n \
                    Description\n \
                    Calories\n \
                    Fats\n \
                    Sugar\n \
                    Sodium\n \
                    Protein\n \
                    SaturatedFat\n \
                    Carbohydrates\n \
                    Techniques\n")

            attribute = input("Enter your option: ")
            
            if attribute == "Instructions" or attribute == "Tags":
                # Instructions and Tags have their own tables
                # so they are handled seperately 
                query = ("DELETE FROM {} WHERE RecipeID={}".format(attribute,recipeID))
                cursor.execute(query)
                cnx.commit()
                if attribute == "Instructions": inputSteps(recipeID,cursor,cnx)
                else: inputTags(recipeID,cursor,cnx)
            elif attribute == "Ingredients":
                query = ("DELETE FROM RecipeIngredient WHERE RecipeID={}".format(recipeID))
                cursor.execute(query)
                cnx.commit()
                inputIngredient(recipeID,cursor,cnx)
            elif attribute == "RecipeName" or attribute == "Description":
                newValue = input("New {}:".format(attribute))
                query = ("UPDATE Recipe SET {}={} WHERE RecipeID={}".format(attribute,"\'"+newValue+"\'",recipeID))
                cursor.execute(query)
                cnx.commit()
            elif attribute == "Techniques":
                newValue = inputTechs()
                query = ("UPDATE Recipe SET {}={} WHERE RecipeID={}".format(attribute,"\'"+newValue+"\'",recipeID))
                cursor.execute(query)
                cnx.commit()
            elif (attribute == "finish"):
                print("Successfully update recipe: {}".format(recipeID))
                break
            else:
                newValue = input("New {}:".format(attribute))
                if (len(newValue) == 0): newValue = "NULL"
                query = ("UPDATE Recipe SET {}={} WHERE RecipeID={}".format(attribute,newValue,recipeID))
                cursor.execute(query)
                cnx.commit()

    print("Recipe {} has been modified.".format(recipeID))

    cursor.close()
    cnx.close()

def deleteRecipe():
    print("Delete recipe")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    RecipeID = input("Enter recipe ID that you want to delete: ")

    query = ("SELECT Author FROM RecipeMeta WHERE RecipeID={}".format(RecipeID))
    cursor.execute(query)
    
    result = cursor.fetchone()
    

    if (result == None):
        print("This recipe does not exist.")
        cursor.close()
        cnx.close()
        return

    elif (str(result[0]) == str(globalUser.id)):

        ## When delete a recipe, all relevant data needed to be deleted
        ## This is reply on "ON DELETE CASCADE" 
        ## Tags, instuctions, reviews and ingredient all needed to be deleted 

        query = ("DELETE FROM Recipe WHERE RecipeID={}".format(RecipeID))
        cursor.execute(query)
        cnx.commit()

        ## if the author has no recipe, he is no longer a author and therefore be removed from author table
        query = ("SELECT RecipeNum FROM Author WHERE UserID={}".format(globalUser.id))
        cursor.execute(query)

        if (cursor.fetchone()[0] == 1):

            query = ("DELETE FROM Author WHERE UserID={}".format(globalUser.id))
            cursor.execute(query)
            cnx.commit()

            query = ("UPDATE Users SET Constraints=0 WHERE UserID={}".format(globalUser.id))
            cursor.execute(query)
            cnx.commit()

        else:
            ## the author will have one recipe less
            query = ("UPDATE Author SET RecipeNum=RecipeNum-1 WHERE UserID={}".format(globalUser.id))
            cursor.execute(query)
            cnx.commit()

            query = ("UPDATE Author SET OverallRate=\
            (SELECT AVG(OverallRate) FROM RecipeWithReview INNER JOIN RecipeMeta USING(RecipeID) WHERE Author={})\
                WHERE UserID={}".format(globalUser.id,globalUser.id))
            cursor.execute(query)
            cnx.commit()

    else:
        print("You can only delete your own recipe")
        cursor.close()
        cnx.close()
        return

    print("Recipe {} has been deleted.".format(RecipeID))
    cursor.close()
    cnx.close()

