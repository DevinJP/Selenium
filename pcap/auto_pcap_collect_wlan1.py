
#!/usr/bin/python

# Feb 9, 2017
# The goal of this script is to continually collect pcap for a given interface
# The script runs on a raspberry pi 3 with an external wifi dongle (wlan1)
#
# The script is run by root in a cron after the system reboots (after short sleep to let system fully boot)
# @reboot sleep 32 && /usr/bin/python  /home/pi/src/PYTHON/AUTO_PCAP/auto_pcap_collect_wlan1.py
#
# The script assumes there is a wifi dongle in wlan1
# the script assumes the pcap file directory exists
# If wlan1 is up, packets will be written to the file until timeout (800 sec) or wlan1 goes down
# if wlan1 is down, current file is closed, new filename based on time is opened, and attempt to collect pcap
# if the timeout is reached, a new filename will be generated and packets captured
# another script will scan open wifi and attempt to connect to the hotspot
# the other script will bring the wlan1 down and back up before each connection attempt
# as soon as wlan1 comes up, the pcap will be opened and all communication with the hotspot will be captured
# since internal operations are much faster than the time it takes to send a packet, packet capture should be up before
# packets are sent and received 
# an empty pcap file will be 24 bytes which is the pcap header. this indicates no activity during the capture







from struct import *
import datetime
import os
import subprocess
import time


def create_filename(net):
    # use time and the interface (wlan1) to create unique filename
    # this assumes the directories are already created
    # if there is a problem, will return a default filename
    my_pcap = '/home/pi/src/TSHARK/error.pcap'
    try:
        my_dir  = '/home/pi/src/TSHARK/'
        my_time = datetime.datetime.now()
        format  = "%b_%d_%Y_%H_%M_%S_%s"
        s = my_time.strftime(format)
        #print s
        my_file = 'tcpdump_%s_%s.pcap' % (s,net)
        my_pcap = os.path.join(my_dir,my_file)
        #print my_pcap
    except:
        my_pcap = '/home/pi/src/TSHARK/error.pcap'
    return my_pcap
    
    
    
def capture_packet(netw):
    rtn_str = ''
    # make finite attempts to capture packets, no need to run forever
    # assume many reboot and connection attempts
    # can adjust the loop size depending on conditions
    for i in range(1000):
        try:
            newfile = create_filename(netw)
            # use the tcpdump command to collect packets
            # use 800 seconds as timeout, could be much shorter
            ifconfig_command= ['sudo', '/usr/bin/timeout' , '800', '/usr/sbin/tcpdump', '-pni', netw, '-s65535', '-w', newfile ]
            ifconfig_cmd=subprocess.Popen(ifconfig_command,stdout=subprocess.PIPE)
            ifconfig_result=ifconfig_cmd.communicate()[0]
            if 'That device is not up' in ifconfig_result:
                pass
                #print ifconfig_result
            elif 'The interface went down' in ifconfig_result:
                pass
                #print ifconfig_result
        except:
            print 'failed'
        
    return rtn_string
       
    


def main():
    
    yy = capture_packet('wlan1')
    
if __name__ == "__main__":
    main()