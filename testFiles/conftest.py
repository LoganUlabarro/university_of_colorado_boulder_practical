from base.web_driver_setup import WebDriverSetup
import pytest

#runs before and after every method
@pytest.fixture()
def setUp():
    print("Running method level setUp")
    yield
    print("Running method level tearDown")

#runs before and after every class, default browser set to Chrome, but you can change it manually
@pytest.fixture(scope="class")
def oneTimeSetUp(request, browser = 'chrome'):
    #set up the driver for whichever browser you are using
    wds = WebDriverSetup(browser)
    driver = wds.getWebDriverInstance()

    print("Running one time setUp")

    if request.cls is not None:
        request.cls.driver = driver

    #close driver when tests are done
    yield driver
    driver.quit()
    print("Running one time tearDown")

def pytest_addoption(parser):
    parser.addoption("--browser", help="Type of browser: chrome, firefox")
    parser.addoption("--osType", help="Type of operating system")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")