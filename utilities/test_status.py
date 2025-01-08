from base.selenium_driver_util import seleniumDriver
import utilities.custom_logger as cl
import logging

class ResultHandler(seleniumDriver):
    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        super().__init__(driver)
        self.resultList = []

    def setResult(self, result, resultMessage):
        try:
            if result is not None:
                if result:
                    self.resultList.append('Pass')
                    self.log.info(f'Verification passed: {resultMessage}')
                else:
                    self.resultList.append('Fail')
                    self.screenshot(resultMessage)
                    self.log.error(f'Verification Failed: {resultMessage}')
            else:
                self.resultList.append('Fail')
                self.screenshot(resultMessage)
                self.log.error(f'Verification Failed, result is none: {resultMessage}')
        except Exception as e:
            self.resultList.append('Fail')
            self.screenshot(resultMessage)
            self.log.error(f'Exception occurred: {str(e)}')

    def mark(self, result, resultMessage):
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage):
        self.setResult(result, resultMessage)
        if 'Fail' in self.resultList:
            self.log.error(f'{testName}: Test Case Failed')
            self.screenshot(resultMessage)
            self.resultList.clear()
            assert False
        else:
            self.log.info(f'{testName}: All assertions passed')
            self.resultList.clear()
            assert True
