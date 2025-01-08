import utilities.csv_reader as cr
import utilities.get_path as gp
from os.path import exists

def getEnvSettings():
    #Set up a list to store the results
    testSettings = []

    #gets url, browser, and env from the config file
    try: 
        pathToFile = gp.getPathToFile('config', '../config')
        settings_file_exists = exists(pathToFile)
        if settings_file_exists:
            print('using settings from file')
            dataSet = cr.getCSVData(pathToFile)

            for rows in dataSet:
                if rows[0] == 'Y':
                    testUrl = rows[3]
                    testBrowser = rows[4]
                    testEnv = rows[2]
                    settingFileFlag = 1
    except:
        print('Could not fild config file')

    #append the important fields to our testSettings
    testSettings.append(testUrl.strip())
    testSettings.append(testBrowser.lower())
    testSettings.append(testEnv.lower())
    testSettings.append(settingFileFlag)
    
    return testSettings