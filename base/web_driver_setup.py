from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from utilities.get_env_settings import getEnvSettings
import logging
import os

class WebDriverSetup:
    """
    A class to set up WebDriver instances for different browsers.
    """

    def __init__(self, browser):
        """
        Initialize the WebDriverSetup with the desired browser.

        Parameters:
        browser (str): The name of the browser (e.g., 'chrome', 'firefox', 'iexplorer').
        """
        self.browser = browser
        self.logger = logging.getLogger(__name__)

    def getWebDriverInstance(self):
        """
        Get the WebDriver instance based on the specified browser.

        Returns:
        WebDriver: The WebDriver instance.
        """
        testSettings = getEnvSettings()

        # Set up path to downloads folder
        downloadDirectory = '../downloadFiles/'
        currentDirectory = os.path.dirname(__file__)
        relativePath = os.path.join(currentDirectory, downloadDirectory)
        cannonDownloadPath = os.path.realpath(relativePath)

        try:
            if self.browser == "chrome":
                self.logger.info('Setting up Chrome WebDriver')
                driver = self._setup_chrome(cannonDownloadPath)
            elif self.browser == "firefox":
                self.logger.info('Setting up Firefox WebDriver')
                driver = self._setup_firefox(cannonDownloadPath)
            elif self.browser == "iexplorer":
                self.logger.info('Setting up Internet Explorer WebDriver')
                driver = self._setup_ie()
            else:
                self.logger.error('Driver not supported')
                raise ValueError('Driver not supported')

            # Maximize the window and set implicit wait
            driver.maximize_window()
            driver.implicitly_wait(10)
            # Navigate to the URL provided in settings
            driver.get(testSettings[0])
            return driver

        except Exception as e:
            self.logger.error(f'Error setting up WebDriver: {str(e)}')
            raise

    def _setup_chrome(self, download_path):
        """
        Set up Chrome WebDriver with options.

        Parameters:
        download_path (str): The path to the download directory.

        Returns:
        WebDriver: The Chrome WebDriver instance.
        """
        options = ChromeOptions()
        prefs = {"download.default_directory": download_path}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--incognito")
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument(f"download.default_directory={download_path}")
        chromeInstall = ChromeDriverManager().install()
        folder = os.path.dirname(chromeInstall)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path, options=options)
        #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    def _setup_firefox(self, download_path):
        """
        TODO: Check if this works
        Set up Firefox WebDriver with options.

        Parameters:
        download_path (str): The path to the download directory.

        Returns:
        WebDriver: The Firefox WebDriver instance.
        """
        options = FirefoxOptions()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.dir", download_path)
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        options.profile = profile
        options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        return driver

    def _setup_ie(self):
        """
        TODO: Check if this works and expand functionality
        Set up Internet Explorer WebDriver.

        Returns:
        WebDriver: The Internet Explorer WebDriver instance.
        """
        driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
        return driver
