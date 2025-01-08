from base.selenium_driver_util import seleniumDriver
import utilities.custom_logger as cl
import logging

class homePage(seleniumDriver):

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.log.info('*+' * 35)

    #locators
    _username_input_field = '//*[@name="username"]'
    _password_input_field = '//*[@name="password"]'
    _login_btn = '.oxd-button'

    def inputUsername(self, username):
        self.waitForElementVisible(self._username_input_field, 'xpath')
        try:
            self.setValue(username, self._username_input_field, 'xpath')
        except():
            print('failed to input username')
        
    def inputPassword(self, password):
        self.waitForElementVisible(self._password_input_field, 'xpath')
        try:
            self.setValue(password, self._password_input_field, 'xpath')
        except:
            print('failed to input password')

    def clickLoginBtn(self):
        self.waitForElementPresent(self._login_btn, 'css')
        try:
            self.clickElement(self._login_btn, 'css')
        except:
            print('could not interact with button')
        
    def loginToPage(self):
        self.inputUsername('Admin')
        self.inputPassword('admin123')
        self.clickLoginBtn()

    