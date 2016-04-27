from bs4 import BeautifulSoup
from urllib2 import urlopen
import os
import urllib2
import testHeaders
import cookingDatabase

useragent = "User-Agent=Mozilla/5.0 (Windows NT 6.0; rv:32.0) Gecko/20100101 Firefox/32.0"
BASE_URL = "http://www.bonappetit.com/sitemap/recipes"

def make_soup(url):
    params = testHeaders.fetch(url, agent = useragent)
    return BeautifulSoup(params["data"], "lxml")

def get_ingredients(the_url):
    soup = make_soup(the_url)
    recipeUrl = the_url
    recipeName = soup.find("h1", {"itemprop" : "name" }).string
    recipeName = recipeName.strip()
    
    if type(recipeName) == str:
        recipeName = unicode(value, "utf-8", errors="ignore")
    else:
        recipeName = unicode(recipeName)
    ingredients = [span.text for span in soup.findAll("span", class_="name", itemprop = "ingredients")]
    for ingredient in ingredients:
        #ingredient = ingredient.strip() 
        if type(ingredient) == str:
            ingredient = unicode(value, "utf-8", errors="ignore")
            ingredient = ingredient.strip()
            print ingredient
        else:
            ingredient.encode("utf-8")
            ingredient = ingredient.strip()
            print ingredient.encode("utf-8")  
    
    return {"recipeUrl": recipeUrl, "recipeName": recipeName, "ingredients": ingredients}
    
theIngredients = get_ingredients("http://www.bonappetit.com/recipe/slow-cooker-indian-spiced-chicken-tomato-cream")
ingredients = theIngredients["ingredients"]

for ingredient, temp in enumerate(ingredients):
    ingredients[ingredient] = temp.strip()
    if type(ingredient) == str:
        ingredient = unicode(value, "utf-8", errors="ignore")
        print ingredient
    else:
        ingredient.encode("utf-8")
        print ingredient.encode("utf-8") 


ingredients = [" apple", "banana", "carrot", "soup", " ground turmeric"]
for i, s in enumerate(ingredients):
    ingredients[i] = s.strip()
for ingredient in ingredients:
        print ingredient


