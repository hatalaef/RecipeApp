#adds into recipeDatabase
import sqlite3 as lite
import sys

db = None


#checks if recipe url is unique
def checkRecipeUnique(name, theURL):
    global db
    
    recipeUrl = theURL

    try:
        db = lite.connect(name)
        cursor = db.cursor()
        
        uniqueRecipe = cursor.execute("SELECT EXISTS(SELECT 1 FROM recipe WHERE recipe.url = ?)", (recipeUrl,)).fetchone()
        if uniqueRecipe[0] == 1:
            print "Recipe URL already exists for %s." % (recipeUrl)
            return False
        else:
            return True

    except lite.Error, e:
        print "Error: %s" % e.args[0]
        print sys.exc_traceback.tb_lineno
        raise e
    finally:
        db.close()

def updateDatabase(name, tableInfo):
    global db
    
    recipeUrl = tableInfo["recipeUrl"]
    recipeName = tableInfo["recipeName"]
    ingredients = tableInfo["ingredients"]
    
    try:
        db = lite.connect(name)
        cursor = db.cursor()
        
        #checks unique recipe url
        try:
            cursor.execute("INSERT INTO recipe(url, name) VALUES (?, ?)", (recipeUrl, recipeName))
            
        except lite.IntegrityError, e:
            print "Rolling back: %s" % e.args[0]
            db.rollback()
            return
            
        recipeId = cursor.lastrowid
        for ingredient in ingredients:
            #checks if ingredient is already in database
            uniqueIngredient = cursor.execute("SELECT EXISTS(SELECT 1 FROM ingredient WHERE ingredient.name = ?)", (ingredient,)).fetchone()
            if uniqueIngredient[0] == 1:
                ingredientId = (cursor.execute("SELECT ingredient._id FROM ingredient WHERE ingredient.name = ?", (ingredient,)).fetchone())[0]
            else:
                cursor.execute("INSERT OR IGNORE INTO ingredient(name) VALUES (?)", (ingredient,))
                ingredientId = cursor.lastrowid
            uniqueRecipe = cursor.execute("SELECT EXISTS(SELECT 1 FROM ingRec_xref WHERE ingId = ? AND recId = ?)", (ingredientId, recipeId)).fetchone()
            if uniqueRecipe[0] == 0:
                cursor.execute("INSERT INTO ingRec_xref(ingId, recId) VALUES (?, ?)", (ingredientId, recipeId))
            else:
                print "ingRec already exists for %s." % (ingredient)
        db.commit()
        
        if type(recipeName) == str:
            print "Success: entered %s" % (recipeName)
        else:
            print "Success: entered %s" % (recipeName.encode("utf-8"))
            
        print
        
    except lite.Error, e:
        print "Error: %s" % e.args[0]
        print sys.exc_traceback.tb_lineno
        db.rollback()
        raise e
    finally:
        db.close()