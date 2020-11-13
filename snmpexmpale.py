#!/usr/bin/env python3
from pysnmp.hlapi import *
import logging
import logging.handlers
import traceback
import time
import argparse

def walk(ipaddress, oid):
	while True:
		for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(), 
			CommunityData('public'), UdpTransportTarget((ipaddress, 161)), ContextData(), 
			ObjectType(ObjectIdentity(oid))):
			if errorIndication:
				print(errorIndication, file=sys.stderr)
				break
			elif errorStatus:
				print('%s at %s' % (errorStatus.prettyPrint(),
									errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
									file=sys.stderr)             
				break
			else:
				writetoFile(varBinds)
		time.sleep(10)
		
def writetoFile(varBinds):
		timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
		try:
            f = open("/tmp/output", 'w')
            for i in varBinds:
			f.write(timestamp + ":"+ i +"\n"))
        except Exception as e:
                logging.error("Could not write to file: " + str(e) + "\n" + traceback.format_exc())
				
if __name__ == '__main__':
	parser = argparse.ArgumentParser("ConnectivityAlerting.py")
	parser.add_argument("-i", "--IP", type=str, help="request destination")
	parser.add_argument("-o", "--OID", type=str, help="OID to walk")
	parser.parse_args()
	cmd_args = parser.parse_args()
	walk_thread = threading.Thread(target=walk, args=[cmd_args.IP, cmd_args.OID])
	walk_thread.start()
	walk_thread.join()
