import socket
from time import strftime, localtime, sleep
from urllib2 import urlopen
import subprocess
import netifaces as ni
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

def makePacket(status):
	MESSAGE = "packet: {\nTime: "

	MESSAGE += strftime("%Y-%m-%d %H:%M:%S", localtime())

	ni.ifaddresses('wlp2s0')
	ip = ni.ifaddresses('wlp2s0')[2][0]['addr']
	routerIP = ni.gateways()['default'].values()[0][0]

	iwCall = subprocess.Popen(["iwconfig wlp2s0"], stdout=subprocess.PIPE, shell=True)
	iwOutput = iwCall.communicate()[0].split()
	SSID = iwOutput[3]
	mac = iwOutput[9]

	MESSAGE += "\nADDR:" + ip
	MESSAGE += "\n" + SSID
	MESSAGE += "\nROUTER_IP:" + routerIP
	MESSAGE += "\nROUTER_MAC:" + mac
	if status == True:
		MESSAGE += "\nEXT_IP:" + urlopen('http://ip.42.pl/raw').read()
	MESSAGE += "\n}"
	return MESSAGE;


DEST = "ec2-54-81-149-127.compute-1.amazonaws.com" #Dest IP
DPORT = 83 #Dest Port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP Socket
display = Display(visible=0, size=(800,600))
display.start()

#Packet before login
beforePacket = makePacket(False) 
#Try to send before login
sock.sendto(beforePacket, (DEST, DPORT))

#Selenium webdriver NOGUI
driver = webdriver.Firefox()

#Test destination, should return "Microsoft Connect Test"
driver.get("http://www.msftconnecttest.com/connecttest.txt")

print driver.page_source #testing first html page
print "\n-------------------------------------------\n"
sleep(5) #wait for possible redirect
print driver.page_source #testing new html page

#get all buttons on login page click on log in buttons
buttons = driver.find_elements_by_tag_name("input")
for button in buttons:
	if "ccept" in button.get_attribute("value"):
		button.click()
		break
	if "onnect" in button.get_attribute("value"):
		button.click()
		break
	if "ubmit" in button.get_attribute("value"):
		button.click()
		break

afterPacket = makePacket(True)
sock.sendto(beforePacket, (DEST, DPORT))
sock.sendto(afterPacket, (DEST, DPORT))

driver.close()
sock.close()
