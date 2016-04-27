import sqlite3 as lite
import sys

db = None
try:
    db = lite.connect("cooking.db")
    cursor = db.cursor()
    
    #clears database
    cursor.execute("DELETE FROM recipe")
    cursor.execute("DELETE FROM ingredient")
    cursor.execute("DELETE FROM ingRec_xref")
    db.commit()
        
    try:
        open("lastUsed.txt", "w").close()
    except Error, e:
        print "Error %s:" % e.args[0]
        print sys.exc_traceback.tb_lineno
        raise e
        
except lite.Error, e:
    print "Error %s:" % e.args[0]
    print sys.exc_traceback.tb_lineno
    db.rollback()
    raise e
finally:
    db.close()