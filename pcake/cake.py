import serial
import pdb

# open a serial connection
serial_port = serial.Serial("COM8", 115200)

# blink the led
def switch():
    serial_port.write(b"switch\n")

pdb.set_trace()