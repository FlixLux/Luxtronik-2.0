#!/usr/bin/env python3
"""
Script to read values from Luxtronik 2.0 heat pump control units
(used by Alpha Innotec and other vendors)

Temperature values are displayed in degrees Celsius

Original author: Stefan Prokop
Version: 2.0
Python 3 port/fix
"""

import sys
import socket
import struct
import datetime
import time

#####################
# Luxtronik 2.0 configuration
#####################
hostHeatpump = "10.1.18.112"  # IP of Luxtronik 2.0 device
portHeatpump = 8888          # Standard port

#####################
# Helpers
#####################
def ts2string(ts, fmt="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime(fmt)

#####################
# Argument handling
#####################
if len(sys.argv) > 1:
    arg = str(sys.argv[1])
else:
    arg = None

#####################
# Socket communication
#####################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostHeatpump, portHeatpump))

# Request calculated values
s.send(struct.pack("!i", 3004))
s.send(struct.pack("!i", 0))

if struct.unpack("!i", s.recv(4))[0] != 3004:
    print("Error: REQ_CALCULATED CMD")
    sys.exit(1)

stat = struct.unpack("!i", s.recv(4))[0]
length = struct.unpack("!i", s.recv(4))[0]

array_calculated = []
for _ in range(length):
    array_calculated.append(struct.unpack("!i", s.recv(4))[0])

s.close()

#####################
# Output selection
#####################
if arg == "ambtemp":
    print(float(array_calculated[15]) / 10)

elif arg == "avetemp":
    print(float(array_calculated[16]) / 10)

elif arg == "servicewateract":
    print(float(array_calculated[17]) / 10)

elif arg == "servicewatertarget":
    print(float(array_calculated[18]) / 10)

elif arg == "flow":
    print(float(array_calculated[10]) / 10)

elif arg == "return":
    print(float(array_calculated[11]) / 10)

elif arg == "returntarget":
    print(float(array_calculated[12]) / 10)

elif arg == "hotgas":
    print(float(array_calculated[14]) / 10)

elif arg == "datelastfailure":
    print(int(array_calculated[95]))

elif arg == "datelastfailurenice":
    print(ts2string(int(array_calculated[95])))

elif arg == "codelastfailure":
    print(int(array_calculated[100]))

elif arg == "operationalstate":
    print(int(array_calculated[119]))

else:
    print(
        "Usage: {ambtemp|avetemp|servicewateract|servicewatertarget|"
        "flow|return|returntarget|hotgas|datelastfailure|"
        "datelastfailurenice|codelastfailure|operationalstate}"
    )

# RAW Data (for debugging)
 
# print(array_calculated)
