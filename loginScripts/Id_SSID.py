#!/usr/bin/python

import os
from shutil import copyfile
import string
import subprocess
import datetime
import glob # for getting files in a directory

from time import strftime, localtime

def ExtractUDP(fname):
    extract_command = ['/usr/bin/tshark', '-r', fname, '-Y', 'udp.dstport==83', '-T', 'fields', '-e', 'data.data']
    #print extract_command
    cmd1=subprocess.Popen(extract_command,stdout=subprocess.PIPE)
    cmd1_result=cmd1.communicate()[0]
    items = cmd1_result.split('\n')
    results = []
    for item in items:
        fields = item.split(' ')
        for field in fields:
            # the UDP data.data string has lots of ':'
            if field.count(':') > 20:
                print fname
                x  = string.replace(field,':','')
                x2 = x.decode('hex')
                x3 = x2.decode('base64')
                # now x3 should be the decoded string
                if 'SSID' in x3 and 'ROUTER_IP' in x3:
                    y = x3.find('SSID')
                    y2 = x3.find('ROUTER_IP')
                    SSID = x3[y+6:y2 -3]
                    SSID = string.replace(SSID,' ','_')
                    SSID = string.replace(SSID,'.','_')
                    SSID = string.replace(SSID,':','_')
                    if SSID not in results:
                        results.append(SSID)
    for result in results:
        newname = '%s%s.pcap' %(fname[:-5],SSID)
        print newname
        copyfile(fname,newname)

def Copy_and_clean(f1):
    # use util.copyfile and mergecap to clean up pcap
    # and remove last broken packet
    # only useful for small pcap files since it takes time
    dir2  = '/home/pi/TMP2/'
    file1 = os.path.basename(f1)
    path1 = os.path.dirname(f1)
    file2 = os.path.join(dir2,file1)
    mergecap_command = ['/usr/bin/mergecap', '-w', file2, f1 ]
    #print extract_command
    cmd1=subprocess.Popen(mergecap_command,stdout=subprocess.PIPE)
    cmd1_result=cmd1.communicate()[0]
    ExtractUDP(file2)
 
def Check_file(f2):
    #check the pcap for the base64 string before processing it
    print f2
    f3       = open(f2,'r')
    f3_data  = f3.read()
    f3.close()
    if "cGFja2V0OiB7ClRp" in f3_data:
        print 'found the beacon so process it'
        Copy_and_clean(f2)
        
def main():
    #loop through the files in this directory
    #open the file as binary and search for the base64 string
    #If the file contais the start of the base64 string
    #then use mergecap to clean up the pcap
    #and then use tshark to extract the beacon info
    # finally, rename the file to include the SSID
    # notice the wildcard in the file path
    dirname = '/home/pi/src/TSHARK/*wlan1.pcap'
    for name in glob.glob(dirname):
        #print name
        Check_file(name)
        #ExtractUDP(name)


    
if __name__ == '__main__':
    main()
