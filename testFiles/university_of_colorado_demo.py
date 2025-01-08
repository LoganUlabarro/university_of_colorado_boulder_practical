# page objects
from pages.home_page import homePage
from pages.user_management_page import userManagementPage

# utilities
from utilities.test_status import ResultHandler
from utilities.get_env_settings import getEnvSettings

# assertions and data
import unittest
import pytest

# get environment settings
envSettings = getEnvSettings()
testEnvironment = envSettings[2]
testDataType = envSettings[3]

# Uses one time setup and setup from conftest file
@pytest.mark.usefixtures('oneTimeSetUp', 'setUp')
class SmokeTests(unittest.TestCase):

    # set up page object for all tests
    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        # set up page objects
        self.home = homePage(self.driver)
        self.um = userManagementPage(self.driver)
        # set up test status
        self.ts = ResultHandler(self.driver)

    #logs us into the application
    @pytest.mark.run(order=1)
    def test_valid_login(self):
        # run login page steps
        print('running search tests')
        self.home.loginToPage()
        self.um.navigateToAdminPage()
        result = self.um.verifySearchBtnExists()
        self.ts.markFinal('Navigate to User Managment Page', result, 'Navigated to user management page')
        
    @pytest.mark.run(order=2)
    def testCreateUsers(self):
        self.um.clickAddBtn()
        self.um.createNewUser('Admin','Orange', 'enabled', 'testUser1', 'abcdABCD1')
        self.um.clickAddBtn()
        self.um.createNewUser('ESS', 'Orange', 'disabled', 'testUser2', 'abcdABCD1')
        result1 = self.um.checkResults('testUser1')
        self.ts.mark(result1, 'checked first user')
        result2 = self.um.checkResults('testUser2')
        self.ts.mark(result2, 'checked second user')
        self.um.deleteUser('testUser2')
        resultFinal = self.um.validateUserDeleted('testUser2')
        self.ts.markFinal('testcreatedusers', resultFinal, 'test user successfully deleted')
        '''
        This is where the sql validation would be, I don't have a sql database but I have a utility to set up sql connections and run queries. This will be psuedocode from here on.
        Please see my sql_connection.py in the utilities folder:
        
        cursor = self.setupConnection(serverN, db, uid, pwd):
        self.executeQuery(cursor, 'select * from databasetable where username = "testUser2"')
        results = cursor.fetchall()
        
        if not results:
            self.ts.mark('successfully deleted from table', True)
        else:
            self.ts.mark('still in sql table', False)
            
        I don't have the library to do get requests in python, typically I'd confirm with postman, but it seems you just provide the url such as:
        url = "https://api.example.com/data"
        
        params = {
        "key1": "value1",
        "key2": "value2"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print("Data retrieved:", data)
        else:
            print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)
        
        '''
        
        
