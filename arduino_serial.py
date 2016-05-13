import sys
import serial
import time


s = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=None)
s.setDTR(False)
time.sleep(5)


def cmd(cmd):
    if cmd[-1] != '\n':
        cmd += '\n'
    s.write(cmd)
    s.flush()
    print('<< ' + s.read(len(cmd)))


def main():
    filename = sys.argv[1]
    raw_input("Ready?")
    for line in open(filename):
        if line[0:2] == 'PD':
            raw_input("PEN DOWN")
        if line[0:2] == 'PU':
            raw_input("PEN UP")
        print('>>' + line[:-1])
        cmd(line)

if __name__ == '__main__':
    main()
