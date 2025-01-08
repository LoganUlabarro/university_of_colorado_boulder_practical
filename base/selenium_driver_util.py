from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from utilities.csv_reader import getCSVData
import utilities.custom_logger as cl
import logging
import time
import os
import re

class seleniumDriver:
    """A utility class for Selenium WebDriver."""

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        """
        Initialize the SeleniumDriver.

        Parameters:
        driver (WebDriver): The WebDriver instance.
        """
        self.driver = driver

    def screenshot(self, resultName):
        """
        Take a screenshot and save it to the specified directory.

        Parameters:
        resultName (str): The name to save the screenshot under.
        """
        fileName = f"{resultName}_{int(time.time() * 1000)}.png"
        screenshotDirectory = '../screenshots/'
        relativeFileName = os.path.join(screenshotDirectory, fileName)
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.debug(f'Screenshot taken: {fileName}')
        except Exception as e:
            self.log.error(f'Could not save screenshot: {str(e)}')

    def getByType(self, locatorType):
        """
        Get the Selenium By type based on a string.

        Parameters:
        locatorType (str): The type of locator (e.g., 'id', 'name').

        Returns:
        By: The corresponding By type.
        """
        locatorType = locatorType.lower()
        byTypes = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "classname": By.CLASS_NAME,
            "linktext": By.LINK_TEXT
        }
        if locatorType in byTypes:
            return byTypes[locatorType]
        else:
            self.log.error(f"Locator type '{locatorType}' not correct/supported")
            return False

    def getElement(self, locator, locatorType='xpath'):
        """
        Get an element based on the locator and locator type.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').

        Returns:
        WebElement: The located element.
        """
        try:
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.debug(f'Element found with locator: {locator}, type: {locatorType}')
            return element
        except Exception as e:
            self.log.error(f"Element not found: {str(e)}")
            return None

    def clickElement(self, locator, locatorType='xpath'):
        """
        Click on an element based on the locator and locator type.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.debug(f'Clicked on element with locator: {locator}, type: {locatorType}')
        except Exception as e:
            self.log.error(f"Could not click element: {str(e)}")

    def pressEnter(self, locator, locatorType='xpath'):
        """
        Press the Enter key on an element.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(Keys.ENTER)
            element.submit()
        except Exception as e:
            self.log.error(f"Could not press Enter: {str(e)}")
            
    def pressDownArrow(self, locator, locatorType='xpath'):
        """
        Press the Down Arrow key on an element.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(Keys.ARROW_DOWN)  # Replace Enter with Down Arrow
        except Exception as e:
            self.log.error(f"Could not press Down Arrow: {str(e)}")

    def setValue(self, data, locator, locatorType='xpath'):
        """
        Type a value into a text field.

        Parameters:
        data (str): The value to type.
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(str(data))
            self.log.debug(f'Input "{data}" at locator: {locator}, type: {locatorType}')
        except Exception as e:
            self.log.error(f"Could not type at locator: {str(e)}")

    def clearValue(self, locator, locatorType='xpath'):
        """
        Clear the value at a text field.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            self.log.debug(f'Cleared value at locator: {locator}, type: {locatorType}')
        except Exception as e:
            self.log.error(f"Could not clear value: {str(e)}")

    def getText(self, locator, locatorType='xpath'):
        """
        Get the text of an element.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').

        Returns:
        str: The text of the element.
        """
        try:
            self.waitForElementPresent(locator, locatorType)
            element = self.getElement(locator, locatorType)
            text = element.text
            self.log.debug(f'Text at locator: {locator}, type: {locatorType} is "{text}"')
            return text
        except Exception as e:
            self.log.error(f"Could not get text: {str(e)}")
            return None

    def hoverMouse(self, locator, locatorType='xpath'):
        """
        Hover the mouse over an element.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.log.debug(f'Moved mouse to locator: {locator}, type: {locatorType}')
        except Exception as e:
            self.log.error(f"Could not move mouse: {str(e)}")

    def isElementPresent(self, locator, locatorType="xpath"):
        """
        Check if an element is present.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').

        Returns:
        bool: True if the element is present, False otherwise.
        """
        try:
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            if element:
                self.log.debug(f'Element present: locator: {locator}, type: {locatorType}')
                return True
            else:
                self.log.error(f'Element not present: locator: {locator}, type: {locatorType}')
                return False
        except NoSuchElementException:
            self.log.error(f'Element not found: locator: {locator}, type: {locatorType}')
            return False

    def isElementNotPresent(self, locator, locatorType="xpath"):
        """
        Check if an element is not present.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').

        Returns:
        bool: True if the element is not present, False otherwise.
        """
        try:
            byType = self.getByType(locatorType)
            self.driver.find_element(byType, locator)
            self.log.error(f'Element present: locator: {locator}, type: {locatorType}')
            return False
        except NoSuchElementException:
            self.log.debug(f'Element not present, as expected: locator: {locator}, type: {locatorType}')
            return True
        except Exception as e:
            self.log.error(f'Error checking element presence: {str(e)}')
            return False

    def areElementsPresent(self, locator, locatorType="xpath"):
        """
        Check if multiple elements are present.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').

        Returns:
        bool: True if elements are present, False otherwise.
        """
        try:
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            if elements:
                self.log.debug(f'Elements present: locator: {locator}, type: {locatorType}')
                return True
            else:
                self.log.error(f'Elements not present: locator: {locator}, type: {locatorType}')
                return False
        except Exception as e:
            self.log.error(f"Error finding elements: {str(e)}")
            return False

    def getPathToUploadFile(self, fileName, relativePathInput, fileTypeExtension='csv'):
        """
        Get the absolute path to a file for upload.

        Parameters:
        fileName (str): The name of the file.
        relativePathInput (str): The relative path to the file.
        fileTypeExtension (str): The file extension (default is 'csv').

        Returns:
        str: The absolute path to the file.
        """
        try:
            uploadDirectory = relativePathInput
            currentDirectory = os.path.dirname(__file__)
            relativePath = os.path.join(currentDirectory, uploadDirectory)
            fileToUpload = os.path.join(relativePath, f"{fileName}.{fileTypeExtension}")
            cannonFileToUpload = os.path.realpath(fileToUpload)
            self.log.debug(f'Built path to file: {cannonFileToUpload}')
            return cannonFileToUpload
        except Exception as e:
            self.log.error(f"Error building path to file: {str(e)}")
            return None

    def uploadFile(self, cannonPathToFile, locator, locatorType="xpath"):
        """
        Upload a file to an element.

        Parameters:
        cannonPathToFile (str): The absolute path to the file.
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        """
        try:
            self.setValue(cannonPathToFile, locator, locatorType)
            self.log.debug(f'Successfully uploaded file to locator: {locator}, type: {locatorType}')
        except Exception as e:
            self.log.error(f"Could not upload file: {str(e)}")

    def waitForElementVisible(self, locator, locatorType="xpath", timeout=10, pollFreq=0.5):
        """
        Wait for an element to be visible.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        timeout (int): The maximum wait time (default is 10 seconds).
        pollFreq (float): The polling frequency (default is 0.5 seconds).

        Returns:
        WebElement: The visible element.
        """
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFreq, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
            self.log.debug(f'Element visible: locator: {locator}, type: {locatorType}')
            return element
        except Exception as e:
            self.log.error(f"Element not visible: {str(e)}")
            return None
        finally:
            self.driver.implicitly_wait(2)

    def waitForElementNotVisible(self, locator, locatorType="xpath", timeout=10, pollFreq=0.5):
        """
        Wait for an element to not be visible.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        timeout (int): The maximum wait time (default is 10 seconds).
        pollFreq (float): The polling frequency (default is 0.5 seconds).

        Returns:
        bool: True if the element is not visible, False otherwise.
        """
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFreq, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(EC.invisibility_of_element_located((byType, locator)))
            self.log.debug(f'Element not visible: locator: {locator}, type: {locatorType}')
            return True
        except Exception as e:
            self.log.error(f"Element still visible: {str(e)}")
            return False
        finally:
            self.driver.implicitly_wait(2)

    def waitForElementPresent(self, locator, locatorType="xpath", timeout=10, pollFreq=0.5):
        """
        Wait for an element to be present in the DOM.

        Parameters:
        locator (str): The locator string.
        locatorType (str): The type of locator (default is 'xpath').
        timeout (int): The maximum wait time (default is 10 seconds).
        pollFreq (float): The polling frequency (default is 0.5 seconds).

        Returns:
        WebElement: The present element.
        """
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFreq, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            self.log.debug(f'Element present: locator: {locator}, type: {locatorType}')
            return element
        except Exception as e:
            self.log.error(f"Element not present: {str(e)}")
            return None
        finally:
            self.driver.implicitly_wait(2)

    def pauseFor(self, waitTime):
        """
        Pause execution for a specified amount of time.

        Parameters:
        waitTime (int): The time to wait in seconds.
        """
        time.sleep(waitTime)

    def extractFloatsFromString(self, stringToConvert):
        """
        Extract floating-point numbers from a string.

        Parameters:
        stringToConvert (str): The string to convert.

        Returns:
        list: A list of floats.
        """
        try:
            convertedString = re.findall(r'-?\d+\.?\d*', stringToConvert)
            floatList = list(map(float, convertedString))
            self.log.debug(f'Extracted floats: {floatList}')
            return floatList
        except Exception as e:
            self.log.error(f"Could not extract floats: {str(e)}")
            return []

    def extractIntFromString(self, stringToConvert):
        """
        Extract integers from a string.

        Parameters:
        stringToConvert (str): The string to convert.

        Returns:
        list: A list of integers.
        """
        try:
            convertedString = re.findall(r'-?\d+\.?\d*', stringToConvert)
            intList = list(map(int, convertedString))
            self.log.debug(f'Extracted integers: {intList}')
            return intList
        except Exception as e:
            self.log.error(f"Could not extract integers: {str(e)}")
            return []

    def stringContainsText(self, textToSearch, substr):
        """
        Check if a substring is present in a string.

        Parameters:
        textToSearch (str): The string to search.
        substr (str): The substring to find.

        Returns:
        bool: True if the substring is found, False otherwise.
        """
        if substr in textToSearch:
            self.log.debug(f'Found substring "{substr}" in string "{textToSearch}"')
            return True
        else:
            self.log.error(f'Could not find substring "{substr}" in string "{textToSearch}"')
            return False

    def getNewCSVData(self, pathToData):
        """
        Get data from a CSV file.

        Parameters:
        pathToData (str): The path to the CSV file.

        Returns:
        list: The data from the CSV file.
        """
        try:
            csvData = getCSVData(pathToData)
            self.log.debug(csvData)
            return csvData
        except Exception as e:
            self.log.error(f"Could not access data: {str(e)}")
            return []

    def checkFileExists(self, pathToFile):
        """
        Check if a file exists at a given path.

        Parameters:
        pathToFile (str): The path to the file.

        Returns:
        bool: True if the file exists, False otherwise.
        """
        try:
            if os.path.exists(pathToFile):
                self.log.debug(f'File exists at path: {pathToFile}')
                return True
            else:
                self.log.debug(f'File does not exist at path: {pathToFile}')
                return False
        except Exception as e:
            self.log.error(f"Error checking file existence: {str(e)}")
            return False

    def deleteFileAtPath(self, pathToFile):
        """
        Delete a file at a given path.

        Parameters:
        pathToFile (str): The path to the file.
        """
        if self.checkFileExists(pathToFile):
            try:
                os.unlink(pathToFile)
                self.log.debug(f'Removed file at: {pathToFile}')
            except Exception as e:
                self.log.error(f"Error removing file: {str(e)}")
        else:
            self.log.error('No such file exists')
