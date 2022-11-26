# ECE356-Project

### Step to load data

The dataset can be found on Kaggle

1. run `./server/createReviews.sql`
2. run `./server/createRecipe.sql`
3. run `./server/createUser.sql`
4. run `./server/createRecipeReview.sql`
5. run `./server/createAuthor.sql`
6. run `./server/createInstructions.sql`
7. run `./server/createIngredient.sql`
8. run `./server/createTags.sql`
9. run `./server/index.sql`
10. run `./server/cleanUp.sql`

### Login information for database

The login information hardcoded in the utility.py located inside the client/ folder

It is inside connectDatabase() function looked like the following:

```
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
```

### Step to run client application:
1. Change login information for the database using [Login information for database in this documentation](# Login information for database)
2. Navigate to `./client` folder
3. run `python3 welcome.py`
