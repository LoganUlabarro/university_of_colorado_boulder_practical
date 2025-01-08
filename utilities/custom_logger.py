import inspect
import logging
import os

#levels:
#debug
#info
#warn
#error
#critical

def customLogger(loglevel=logging.INFO, log_folder='logFiles'):
    #get the name of the class / method this is being used in and set up logger
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)

    #set the level of logs you can see, set to debug for now, will be overritten by filehandler
    logger.setLevel(loglevel)

    #set up a file handler
    #a is append, will keep adding on, w is write, will overwrite
    log_file_path = os.path.join(log_folder, 'automation.log')
    fileHandler = logging.FileHandler(log_file_path, 'w')
    fileHandler.setLevel(loglevel)

    #set up formatter
    formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger