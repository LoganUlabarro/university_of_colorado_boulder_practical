from base.selenium_driver_util import seleniumDriver
import utilities.custom_logger as cl
import logging

class userManagementPage(seleniumDriver):

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.log.info('*+' * 35)

    #locators
    _admin_btn = '((//*[@class="oxd-main-menu-item"])[1])'
    
    _username_input_field = '((//input)[2])'
    _role_select_dropdown = '((//*[@class="oxd-icon bi-caret-down-fill oxd-select-text--arrow"])[1])'
    _status_select_dropdown = '((//*[@class="oxd-icon bi-caret-down-fill oxd-select-text--arrow"])[2])'
    _search_btn = '((//*[@type="submit"]))'
    _reset_btn = '//button[contains(@class, "oxd-button") and .//text()[normalize-space()="Reset"]]'
    _add_user_btn = '//button[contains(@class, "oxd-button") and .//text()[normalize-space()="Add"]]'
    _res_first_username = '((//div[@data-v-6c07a142])[1])'
    _res_first_delete_btn = '((//i[@class="oxd-icon bi-trash"])[1])'
    
    _create_user_role_input = '((//*[@class="oxd-select-text-input"])[1])'
    _create_status_input = '((//*[@class="oxd-select-text-input"])[2])'
    _create_employee_name_input = '((//input)[2])'
    _create_username_create_field = '((//input)[3])'
    _create_password_create_field = '((//*[@type="password"])[1])'
    _create_password_confirm_field = '((//*[@type="password"])[2])'
    _create_save_btn = '((//button)[5])'
    
    def navigateToAdminPage(self):
        self.waitForElementPresent(self._admin_btn)
        self.clickElement(self._admin_btn)
    
    def verifySearchBtnExists(self):
        self.waitForElementPresent(self._add_user_btn)
        if self.isElementPresent(self._add_user_btn):
            return True
        else:
            return False
    
    def clickAddBtn(self):
        self.waitForElementVisible(self._add_user_btn)
        self.clickElement(self._add_user_btn)
        
    def setNewUserRole(self, role):
        self.waitForElementVisible(self._create_user_role_input)
        self.clickElement(self._create_user_role_input)
        if role == 'Admin':
            self.pressDownArrow(self._create_user_role_input)
            self.pressEnter(self._create_user_role_input)
        else:
            self.pressDownArrow(self._create_user_role_input)
            self.pressDownArrow(self._create_user_role_input)
            self.pressEnter(self._create_user_role_input)
        
    def setEmployeeName(self, name):
        self.waitForElementVisible(self._create_employee_name_input)
        self.clearValue(self._create_employee_name_input)
        self.setValue(name, self._create_employee_name_input)
        self.pauseFor(3)
        self.pressDownArrow(self._create_employee_name_input)
        self.pauseFor(1)
        self.pressEnter(self._create_employee_name_input)
        
    def setStatus(self, status):
        self.waitForElementVisible(self._create_status_input)
        if status == 'enabled':
            self.pressDownArrow(self._create_status_input)
            self.pressEnter(self._create_status_input)
        else:
            self.pressDownArrow(self._create_status_input)
            self.pressDownArrow(self._create_status_input)
            self.pressEnter(self._create_status_input)
        
    def setUsername(self, username):
        self.waitForElementVisible(self._create_username_create_field)
        self.clearValue(self._create_employee_name_input)
        self.setValue(username, self._create_username_create_field)
        
    def setPasswordFields(self, password):
        self.waitForElementVisible(self._create_password_create_field)
        self.setValue(password, self._create_password_create_field)
        self.waitForElementVisible(self._create_password_confirm_field)
        self.setValue(password, self._create_password_confirm_field)
        
    def clickSaveBtn(self):
        self.waitForElementVisible(self._create_save_btn)
        self.clickElement(self._create_save_btn)
        self.waitForElementVisible(self._username_input_field, 'xpath', 30)
        
    def createNewUser(self, role, employee, status, username, password):
        self.setNewUserRole(role)
        self.setEmployeeName(employee)
        self.setStatus(status)
        self.setUsername(username)
        self.setPasswordFields(password)
        self.clickSaveBtn()
        
    def clickSearechBtn(self):
        self.waitForElementPresent(self._search_btn)
        self.clickElement(self._search_btn)
    
    def inputUsername(self, username):
        self.waitForElementVisible(self._username_input_field)
        self.clearValue(username, self._username_input_field)
        self.setValue(username, self._username_input_field)
        self.clickSearechBtn()
        self.waitForElementPresent(self._res_first_username)
        
    def validateUsername(self, username):
        self.waitForElementPresent(self._res_first_username)
        result = self.getText(self._res_first_username)
        if username == result:
            return True
        else:
            self.log.error(f'Got the username {result}')
            return False
        
    def validateUserDeleted(self, username):
        self.waitForElementPresent(self._username_input_field)
        self.clearValue(self._username_input_field)
        self.inputUsername(username)
        self.clickSearechBtn()
        self.waitForElementVisible(self._res_first_username)
        if self.isElementNotPresent(self._res_first_username):
            return True
        else:
            return True

    def deleteUser(self, username):
        self.waitForElementPresent(self._res_first_delete_btn)
        if self.validateUsername(username):
            self.clickElement(self._res_first_delete_btn)
            
    
    def checkResults(self, username):
        self.clearValue(self._username_input_field)
        self.inputUsername(username)
        self.clickElement(self._search_btn)
        return self.validateUsername(username)