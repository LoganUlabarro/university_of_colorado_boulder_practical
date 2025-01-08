import csv
import utilities.sql_connection as sq
import utilities.get_path as g_p

def getCSVData(filename):
    #set up an empty array where the data will be stored
    rows = []
    
    #Open the csv file
    datFile = open(filename, 'r')
    
    #create a csv reader and give it the file
    reader = csv.reader(datFile)
    
    #skip headers
    next(reader)
    
    #add rows from reader to list
    for row in reader:
        rows.append(row)
    
    #return the data
    return rows

def writeCSVData(filePath, headerData, csvData):   
    with open(filePath, 'w', encoding='UTF8', newline='') as f:
        #create a writer to write to the csv
        writer = csv.writer(f)

        #write the header
        writer.writerow(headerData)
        #print(headers)
        #write the rest of the file
        writer.writerows(csvData)
        #print(data)

#'SELECT TOP 5 * FROM [database].[dbo].[table]'
def writeDataFromSQL(fileName,headers,query):
    pathToFile = g_p.getPathToFile(fileName, '../uploadFiles/', 'csv')
    #['header1', 'header2', 'header3']
    csvHeader = headers
    dataSet = sq.generateListMachineLearning(query)
    #writeCSVData('masterFile.csv', csvHeader, dataSet)
    with open(pathToFile, 'w', encoding='UTF8', newline='') as f:
        #create a writer to write to the csv
        writer = csv.writer(f)

        #write the header
        writer.writerow(csvHeader)

        #write the rest of the file
        writer.writerows(dataSet)