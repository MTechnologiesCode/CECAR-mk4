import serial

arduino_port = "/dev/tty.usbmodem1101"
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def send_arduino_command(command):
    ser.write((command + '\n').encode())
    response = ser.readline().decode().strip()
    return response