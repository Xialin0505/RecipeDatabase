from utility import *
from recipe import *
from review import *

# user login page
def Login():
    result = None

    while (result == None):

        userInput = input("Please enter your user id: ")

        cnx = ConnectDatabase()
        cursor = cnx.cursor()
        
        # check if user registration status
        query = ("SELECT UserID FROM Users WHERE UserID={}".format(userInput))
        cursor.execute(query)
        result = cursor.fetchone()
        if result == None:
            print("Invalid user id, please try again")
        
        cursor.close()
        cnx.close()

    globalUser.id = userInput

# user logout page
def LogOut():
    print("Going to logout")
    # record the logout timestamp
    updateLastInteractionTime()
    print("Bye.")
    sys.exit()

# register a new user
def Register():
    # ask for user name
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")

    cnx = ConnectDatabase()
    cursor = cnx.cursor()

    # assign a new ID for user
    query = ("SELECT max(UserID) FROM Users ")
    cursor.execute(query)
    maxID = cursor.fetchone()

    maxID = maxID[0]
    newID = maxID + randint(1,5)*randint(3,10)

    # add the new user in database
    query = ("INSERT INTO Users (UserID,FirstName,LastName,Constraints) VALUES ({},{},{},0)".format(newID,"\'"+firstName+"\'","\'"+lastName+"\'"))
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()
    print("Your user id is: {}".format(newID))
    globalUser.id = newID

# home page
def HomePage():
    print("Welcome")

    while (True):
        userInput = input("Are you a new user? Yes/No: ")

        if (userInput == "Yes"):
            Register()
            break
        elif(userInput == "No"):
            Login()
            break
    
    while (True):
        AvailableAction()

def AvailableAction():
    print("\n")
    print("Menu")
    # list of actions that user can take
    actions = "Avaiable Actions: \n\
                1:\tSearch recipe\n\
                2:\tCreate recipe\n\
                3:\tMy recipes\n\
                4:\tModify my recipe\n\
                5:\tDelete my recipe\n\
                6:\tSearch recipe by ID\n\
                7:\tCreate review\n\
                8:\tMy reviews\n\
                9:\tModify my review\n\
                10:\tDelete my review\n\
                11:\tLog out\n\
                \r\n"

    print(actions)
    userInput = input("Enter your action number: ")

    # calling corresponding function based on input 
    print("\n")
    if (userInput == "1"):
        searchRecipe()
    elif (userInput == "2"):
        createRecipe()
    elif (userInput == "3"):
        viewMyRecipe()
    elif (userInput == "4"):
        modifyRecipe()
    elif (userInput == "5"):
        deleteRecipe()
    elif (userInput == "6"):
        searchRecipeByID()
    elif (userInput == "7"):
        createReview()
    elif (userInput == "8"):
        viewMyReview()
    elif (userInput == "9"):
        modifyReview()
    elif (userInput == "10"):
        deleteReview()
    elif (userInput == "11"):
        LogOut()


if __name__ == "__main__":
    HomePage()
    #Register()
    #Login()

