from pyvirtualdisplay import Display
from selenium import webdriver
 
display = Display(visible=0, size=(800, 600))
display.start()
 
browser = webdriver.Firefox()
browser.get('http://54.209.45.155/monitor')
print browser.title
browser.quit()
 
display.stop()
