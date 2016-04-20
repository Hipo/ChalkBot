import sys
import serial
import time


s = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=5)
# s.setDTR(False)

for line in sys.stdin:
    print(line)
    s.write(line)
    s.flush()
    print(s.readline())
