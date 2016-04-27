import mySoup

def get_ingredientsMain(the_url, theBaseSite, useragent):
    soup = mySoup.make_soup(the_url, useragent)
    
    recipeUrl = the_url
    tableInfo = theBaseSite(the_url, soup)
    recipeName = tableInfo["recipeName"].strip()
    ingredients = tableInfo["ingredients"]    
    
    if type(recipeName) == str:
        recipeName = unicode(value, "utf-8", errors="ignore")
    else:
        recipeName = unicode(recipeName)
    
    #strips trailing spaces and makes lowercase. not sure exactly how it works
    for ingredient, temp in enumerate(ingredients):
        ingredients[ingredient] = temp.strip().lower()
        
    #prints for testing
    print
    for ingredient in ingredients:
        if type(ingredient) == str:
            ingredient = unicode(value, "utf-8", errors="ignore")
            print ingredient
        else:
            ingredient.encode("utf-8")
            print ingredient.encode("utf-8") 
    print
    return {"recipeUrl": recipeUrl, "recipeName": recipeName, "ingredients": ingredients}

def bonApp(the_url, soup):
    recipeName = soup.find("h1", {"itemprop" : "name" }).string
    ingredients = [span.text for span in soup.findAll("span", class_="name", itemprop = "ingredients")]
    
    return {"recipeName": recipeName, "ingredients": ingredients}
    
#def foodNetwork(the_url, soup):
    