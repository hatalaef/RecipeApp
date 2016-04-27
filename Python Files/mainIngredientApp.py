#from bs4 import BeautifulSoup
from urllib2 import urlopen
import os
import urllib2
import time
import random

import mySoup
import cookingDatabase
import getIngredients

#!!CHANGE THESE!!#
useragent = "User-Agent=Mozilla/5.0 (Windows NT 6.0; rv:32.0) Gecko/20100101 Firefox/32.0"
BASE_URL = "http://www.bonappetit.com/sitemap/recipes" #sitemap
METHOD_NAME = "bonApp" #from getIngredients


fileName = METHOD_NAME + ".txt" #unique file to keep track of info between runs
methodToCall = getattr(getIngredients, METHOD_NAME)
    
def saveToFile(theLink):
    try:
        file = open(fileName, "w")
        file.write(theLink)
        file.close()
    except:
        print "Error %s:" % sys.exc_info()[0]
        print sys.exc_traceback.tb_lineno
        raise e

def loadFromFile():
    try:
        file = open(fileName, "r")
        theLink = file.read()
        file.close()
        
    except:
        print "Error %s:" % sys.exc_info()[0]
        print sys.exc_traceback.tb_lineno
        raise e
    return theLink

def getURL(theLink):
    global lastLink
    global foundLink
    
    if not foundLink and lastLink == theLink:
        foundLink = True
    if foundLink:
        saveToFile(theLink)
        if cookingDatabase.checkRecipeUnique("cooking.db.zip", theLink):
            print "Getting ingredients from: %s" % (theLink)
            cookingDatabase.updateDatabase("cooking.db.zip", getIngredients.get_ingredientsMain(theLink, methodToCall, useragent))
            time.sleep(random.uniform(5, 7)) #to space out requests
        print    
        
    
links = mySoup.get_links(BASE_URL, useragent)
lastLink = loadFromFile()

#checks link ran last time
foundLink = False
if lastLink == "":
    foundLink = True

#to test one URL
#getURL("http://www.bonappetit.com/recipe/kung-pao-brussels-sprouts")    
    
for link in links:
    getURL(link)