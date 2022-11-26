from utility import *

def createReview ():
    print("Create recipe review")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    # gather data from user input
    recipeID = input("Enter the recipe ID that you want to review: ")
    # validate inout recip ID
    query = ("SELECT RecipeID FROM Recipe WHERE RecipeID={}".format(recipeID))
    cursor.execute(query)
    if cursor.fetchone() == None:
        print("This recipe does not exist")
        cursor.close()
        cnx.close()
        return
    comments = input("Enter the comment you want to add: ")
    comments = "\'"+ comments + "\'"
    rating = input("Enter the rating for this recipe: ")

    while (len(rating) == 0):
        print("You must have a rating.")
        rating = input("Enter the rating for this recipe: ")

    currentTime = datetime.now(tz=None)
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    currentTime = "\'"+currentTime+"\'"

    # check if the recipe has review
    query = ("SELECT RecipeID FROM RecipeWithReview WHERE RecipeID={}".format(recipeID))
    cursor.execute(query)
    if cursor.fetchone() == None:
        # first review for this recipe
        # add this recipe into RecipeWithReview table
        query = ("INSERT INTO RecipeWithReview (RecipeID,ReviewNum) VALUES ({},1)".format(recipeID))
        cursor.execute(query)
        cnx.commit()
    else:
        query = ("UPDATE RecipeWithReview SET ReviewNum=ReviewNum+1\
                WHERE RecipeID={}".format(recipeID))
        cursor.execute(query)
        cnx.commit()

    # Add the new comment into the Review table
    query = ("INSERT INTO Reviews VALUES ({},{},{},{},{})".format(recipeID,globalUser.id,comments,rating,currentTime))
    cursor.execute(query)
    cnx.commit()

    # Update the RecipeWithReview table
    query = ("UPDATE RecipeWithReview SET RateCount{}=RateCount{}+1\
                WHERE RecipeID={}".format(rating,rating,recipeID))
    cursor.execute(query)
    cnx.commit()

    # Update the ovearll rate
    query = ("UPDATE RecipeWithReview SET OverallRate=(RateCount5*5+RateCount4*4+\
                RateCount3*3+RateCount2*2+RateCount1)/ReviewNum")
    cursor.execute(query)
    cnx.commit()

    # increament on number of rate in User table
    query = ("UPDATE Users SET TotalRateNumber=TotalRateNumber+1 WHERE UserID={}".format(globalUser.id))
    cursor.execute(query)
    cnx.commit()

    # Update the overall rate of Author as every new rating takes effect on it
    # get the Author ID for this recipe
    query = ("SELECT Author FROM RecipeMeta WHERE RecipeID={}".format(recipeID))
    cursor.execute(query)
    authorID = cursor.fetchone()
    #print(authorID[0])

    # update her/his overall rate
    query = ("UPDATE Author SET OverallRate=\
            (SELECT AVG(OverallRate) FROM RecipeWithReview INNER JOIN RecipeMeta USING(RecipeID) WHERE Author={})\
                WHERE UserID={}".format(authorID[0], authorID[0]))
    cursor.execute(query)
    cnx.commit()

    print("Your review is successfully created")
    cursor.close()
    cnx.close()

def modifyReview():
    print("Modify my reviews")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    recipeID = input("Enter the recipe ID you want to edit the review for: ")
    # check if user has a review for this recipe
    query = ("SELECT Rating FROM Reviews WHERE RecipeID={} AND UserID={}".format(recipeID,globalUser.id))
    cursor.execute(query)
    oldRate = cursor.fetchone()
    
    if oldRate == None:
        # user has no review for this recipe
        print("You do not have a review for this recipe, please add one first")
        cursor.close()
        cnx.close()
        return
    comment = input("Type in the new comment, type No if you don't want to make a change: ")
    rating = ''
    while(True):
        rating = input("Enter the new rating, type No if you don't want to make a change: ")
        if (rating != "No" and (int(rating) < 0 or int(rating) > 5)):
                print("Invalid rating")
        else:
            break

    # modify comments in Reviews table
    if (comment != "No"):
        query = ("Update Reviews SET Comments={} WHERE RecipeID={} AND UserID={}".format("\'"+comment+"\'",recipeID,globalUser.id))
        cursor.execute(query)
        cnx.commit()

    # modify rating 
    if (rating != "No"):
        # update the rating in Review table
        query = ("Update Reviews SET Rating={} WHERE RecipeID={} AND UserID={}".format(rating,recipeID,globalUser.id))
        cursor.execute(query)
        cnx.commit()

        # update RecipeWithReview table
        query = ("UPDATE RecipeWithReview SET RateCount{}=RateCount{}-1, RateCount{}=RateCount{}+1\
                 WHERE RecipeID={}".format(oldRate[0],oldRate[0],rating,rating,recipeID))
        cursor.execute(query)
        cnx.commit()

        query = ("UPDATE RecipeWithReview SET OverallRate=(RateCount5*5+RateCount4*4+\
                RateCount3*3+RateCount2*2+RateCount1)/ReviewNum")
        cursor.execute(query)
        cnx.commit()

        # Update the overall rate of Author as every new rating takes effect on it
        # get the Author ID for this recipe
        query = ("SELECT Author FROM RecipeMeta WHERE RecipeID={}".format(recipeID))
        cursor.execute(query)

        authorID = cursor.fetchone()[0]
        query = ("UPDATE Author SET OverallRate=\
            (SELECT AVG(OverallRate) FROM RecipeWithReview INNER JOIN RecipeMeta USING(RecipeID) WHERE Author={})\
                WHERE UserID={}".format(authorID,authorID))
        cursor.execute(query)
        cnx.commit()

    print("Your review is successfully modified")

    cursor.close()
    cnx.close()

def deleteReview():
    print("Delete my review")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    # ask for the recipeID to delete
    recipeID = input("Enter the recipe id of the review you want to delete: ")

    # get the rating of the review to be deleted
    query = ("SELECT Rating FROM Reviews WHERE RecipeID={} AND UserID={}".format(recipeID,globalUser.id))
    cursor.execute(query)
    oldRate = cursor.fetchone()
    if oldRate == None:
        # user has no review for this recipe
        print("You do not have a review for this recipe")
        cursor.close()
        cnx.close()
        return

    # check if the deleted review is the last one for this recipe
    query = ("Select ReviewNum FROM RecipeWithReview WHERE RecipeID={}".format(recipeID))
    cursor.execute(query)
    reviewNum = cursor.fetchone()[0]

    # deleting review
    query = ("DELETE FROM Reviews WHERE RecipeID={} AND UserID={}".format(recipeID,globalUser.id))
    cursor.execute(query)
    cnx.commit()

    if reviewNum == 1:
        # removew this recipe from RecipeWithReviews specialization
        query = ("DELETE FROM RecipeWithReview WHERE RecipeID={}".format(recipeID))
        cursor.execute(query)
        cnx.commit()

    else:
        # decrementing the ratecount
        query = ("UPDATE RecipeWithReview SET RateCount{}=RateCount{}-1 WHERE RecipeID={}".format(oldRate[0],oldRate[0],recipeID))
        cursor.execute(query)
        cnx.commit()

        # recompute the overall rating of the recipe
        query = ("UPDATE RecipeWithReview SET OverallRate=(RateCount5*5+RateCount4*4+\
                    RateCount3*3+RateCount2*2+RateCount1)/ReviewNum")
        cursor.execute(query)
        cnx.commit()

        # decrementing the total number of reviews
        query = ("UPDATE RecipeWithReview SET ReviewNum=ReviewNum-1 WHERE RecipeID={}".format(recipeID))
        cursor.execute(query)
        cnx.commit()

    # decreament on number of rate in User table
    query = ("UPDATE Users SET TotalRateNumber=TotalRateNumber-1 WHERE UserID={}".format(globalUser.id))
    cursor.execute(query)
    cnx.commit()

    # updating the overall rating of the author
    # get the authorID
    query = ("SELECT Author FROM RecipeMeta WHERE RecipeID={}".format(recipeID))
    cursor.execute(query)
    authorID = cursor.fetchone()[0]

    query = ("UPDATE Author SET OverallRate=\
            (SELECT AVG(OverallRate) FROM RecipeWithReview INNER JOIN RecipeMeta USING(RecipeID) WHERE Author={})\
                WHERE UserID={}".format(authorID,authorID))
    cursor.execute(query)
    cnx.commit()

    print("Your review is deleted")

    cursor.close()
    cnx.close()


def viewMyReview():
    print("View my reviews")
    cnx = ConnectDatabase()
    cursor = cnx.cursor()
    
    # get review info from Reviews table
    query = ("SELECT RecipeID,Comments,Rating,ReviewDate FROM Reviews WHERE UserID={}".format(globalUser.id))
    cursor.execute(query)
    result = cursor.fetchmany(10)
    if (len(result) == 0):
        print("You have no review so far.")
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

    if (len(result) == 0):
        print("You have no more reviews.")

    cursor.close()
    cnx.close()

if __name__ == "__main__":
    #globalUser.id = 596506
    createReview()
    deleteReview()
    viewMyReview()
    modifyReview()


