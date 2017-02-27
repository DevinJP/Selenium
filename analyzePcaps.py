import os
import sys

#Run by "python analyzePcaps.py [.pcap file]" 
#analyzes the pcap file given as a parameter when running the script
# pipe the output to a file for saving, otherwise prints to command line

tsharkr = "tshark -r "
pcap = str(sys.argv[1])

dhcpidCommand = tsharkr + pcap + " -Y \"bootp.option.dhcp eq 5\" -T fields -e bootp.id | tail -n 1"
id = os.popen(dhcpidCommand)
dhcpid = id.read()
dhcp = tsharkr + pcap + " -Y 'bootp.id eq " + dhcpid + "'"

lease = tsharkr + pcap + " -Y \"bootp.option.dhcp eq ack\" -T fields -e bootp.option.ip_address_lease_time | tail -n 1"

newip = tsharkr + pcap + " -Y \"bootp.option.dhcp eq ack\" -T fields -e bootp.ip.your | tail -n 1"

dnsq = tsharkr + pcap + " -Y \"dns.qry.name eq www.msftconnecttest.com && dns.flags.response eq 0 && ! dns.response_in\" -T fields -e frame.number -e ip.dst -e dns.qry.name"

dnsr = tsharkr + pcap + " -Y \"dns.qry.name eq www.msftconnecttest.com && dns.flags.response eq 1 && ! dns.response_in\" -T fields -e frame.number -e ip.dst -e dns.qry.name"

macs = tsharkr + pcap + " -Y \"eth.addr_resolved\" -T fields -e eth.src -e eth.dst | sort -n | uniq"

sentPackets = tsharkr + pcap + " -Y \"ip.dst eq 54.81.149.127\" -T fields -e frame.number -e ip.dst"  

#Execute the commands
print("DHCP\n")
os.system(dhcp)
print("\nLEASE TIME\n")
os.system(lease)
print("\nNEW IP\n")
os.system(newip)
print("\nDNS QUERIES\n")
os.system(dnsq)
print("\nDNS RESPONSES\n")
os.system(dnsr)
print("\nTRACKED MAC ADDRESSES\n")
os.system(macs)
print("\nSENT DATA PACKETS\n")
os.system(sentPackets)

