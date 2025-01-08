from unittest import result
import pyodbc

#generates a connection string
def getConnectionString(serverN, db, uid, pwd):
    try:
        cnxn_str = ("Driver={SQL Server};Server="+serverN+";Database="+db+";UID="+uid+";PWD="+pwd+";")
        return cnxn_str
    except:
        print('could not generate connection string')

#creates a connection to the provied cnxn string
def getConnectionToDB(cnxn_str):
    try:
        cnxn = pyodbc.connect(cnxn_str)
        return cnxn
    except:
        print('could not connect to db')

#creates a cursor to the provided cnxn
def createCursor(cnxn):
    try:
        cursor = cnxn.cursor()
        return cursor
    except:
        print('could not create cursor')

def executeQuery(cursor, query):
    try:
        cursor.execute(query)
    except:
        print('could not execute query')

#returns cursor for server you input
def setupConnection(serverN, db, uid, pwd):
    try:
        connectionString = getConnectionString(serverN, db, uid, pwd)
        cnxn = getConnectionToDB(connectionString)
        cursor = createCursor(cnxn)
        return cursor
    except:
        print('could not set up connection')

#returns a list for the data from your query
def generateListSQL(query,cursor):
    cursor.execute(query)
    dataList = []
    for i in cursor:
        dataList.append(i)  
    return dataList

