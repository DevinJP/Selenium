import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("google.com")
	time.sleep(5)
	buttons = driver.find_elements_by_tag_name("button")
	for button in buttons
		if "Accept" in button.getText()
			button.click()
			return
		if "Connect" in button.getText()
			button.click()
			return
		if "Submit" in button.getText()
			button.click()
			return	


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
