import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.google.com")
        time.sleep(5)
	driver.current_url
	elem = driver.find_element_by_name("Submit").click()
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
