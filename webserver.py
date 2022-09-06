# https://www.instructables.com/Webserver-Using-Pi-Pico-and-ESP01/
# https://circuitdigest.com/microcontroller-projects/interfacing-esp8266-01-wifi-module-with-raspberry-pi-pico < CHECK THIS OUT PLEASE DO ANOTHER TEST
from machine import UART
import machine
import _thread
import time

# Nmap scan report for 192.168.1.37
# MAC Address: 80:7D:3A:3B:EA:0E (Espressif)
# Wi-Fi credentials (if needed)
WIFI_SSID = ("XXXX")
WIFI_PASSWORD = ("XXXX")
PORT = 80

FIRST_TIME_CONNECT_TO_WIFI = False
MAX_BUFFER_SIZE_BEFORE_OUT_OF_MEMORY_ERROR = 51800


def ESP8266Webserver(html_file):
    # Set variables
    recv = ""
    recv_buf = ""
    uart = UART(1, 115200)  # uart on uart1 with baud of 115200

    # Function to handle reading from the uart serial to a buffer
    def _serial_read(mode):
        if mode == "0":
            serial_recv = str(uart.readline())
        else:
            serial_recv = str(uart.read(mode))
        # replace generates less errors than .decode("utf-8")
        serial_recv = serial_recv.replace("b'", "").replace("\\r", "").replace("\\n", "\n").replace("'", "")
        return serial_recv

    def _connect_to_wifi(wifi_ssid, wifi_password):
        """
        Connect to Wi-Fi, this only needs to run once,
        ESP will retain the CWMODE and Wi-Fi details and reconnect after power cycle,
        leave commented out unless this has been run once.
        """
        print('[ !!! ] connecting to Wi-Fi')
        print("  - Setting AP Mode...")
        uart.write('AT+CWMODE=1' + '\r\n')
        time.sleep(2)
        print("  - Connecting to WiFi...")
        uart.write('AT+CWJAP="' + wifi_ssid + '","' + wifi_password + '"' + '\r\n')
        time.sleep(15)
        print('[ VVV ] connected to Wi-Fi')

    def _do_html_handshake():
        print('[ !!! ] starting HTML handshake')
        html_file_object = open(html_file, "r")
        html_file_lines = html_file_object.readlines()
        html_file_object.close()
        uart.write('AT+CIPSEND=0,17' + '\r\n')
        time.sleep(0.1)
        uart.write('HTTP/1.1 200 OK' + '\r\n')
        time.sleep(0.1)
        uart.write('AT+CIPSEND=0,25' + '\r\n')
        time.sleep(0.1)
        uart.write('Content-Type: text/html' + '\r\n')
        time.sleep(0.1)
        uart.write('AT+CIPSEND=0,19' + '\r\n')
        time.sleep(0.1)
        uart.write('Connection: close' + '\r\n')
        time.sleep(0.1)
        uart.write('AT+CIPSEND=0,2' + '\r\n')
        time.sleep(0.1)
        uart.write('\r\n')
        time.sleep(0.1)
        uart.write('AT+CIPSEND=0,17' + '\r\n')
        time.sleep(0.1)
        uart.write('<!DOCTYPE HTML>' + '\r\n')
        time.sleep(0.1)
        print('[ VVV ] finished HTML handshake')
        return html_file_lines

    def _send_html_over_serial():
        print('[ !!! ] sending HTML file')
        for line in html_file_lines:
            cipsend = line.strip()
            ciplength = str(len(cipsend) + 2)  # calculates byte length of send plus newline
            print(ciplength, cipsend)
            uart.write('AT+CIPSEND=0,' + ciplength + '\r\n')
            time.sleep(0.1)
            uart.write(cipsend + '\r\n')
            time.sleep(0.1)  # The sleep commands prevent the send coming through garbled and out of order..
        print('[ VVV ] done sending HTML file')

    def _close_conn():
        print('[ !!! ] closing connection')
        uart.write('AT+CIPCLOSE=0' + '\r\n')  # once file sent, close connection
        time.sleep(4)
        print('[ VVV ] connection closed')

    def _start_webserver():
        print("[ !!! ] Setting Connection Mode...")
        uart.write('AT+CIPMUX=1' + '\r\n')
        time.sleep(2)
        print("[ !!! ] Starting Webserver..")
        uart.write(f'AT+CIPSERVER=1,{PORT}' + '\r\n')  # Start webserver on port 80
        time.sleep(2)
        print("[ VVV ] Webserver Ready!\n")

    print("[ !!! ] Setting up Webserver...")
    time.sleep(2)

    if FIRST_TIME_CONNECT_TO_WIFI:
        _connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

    _start_webserver()

    while True:
        # if the buffer is about to crash the application, reset it
        if len(recv_buf) >= MAX_BUFFER_SIZE_BEFORE_OUT_OF_MEMORY_ERROR:
            print(f'[ WARNING ] resetting buffer, it exceeds size {MAX_BUFFER_SIZE_BEFORE_OUT_OF_MEMORY_ERROR}')
            recv_buf = ''

        # read a byte from serial into the buffer
        recv = _serial_read(1)
        recv_buf = recv_buf + recv

        # if the buffer contains IPD(a connection), then respond with HTML handshake
        if '+IPD' in recv_buf:
            html_file_lines = _do_html_handshake()
            # After handshake, read in html file from pico and send over serial line by line with CIPSEND
            _send_html_over_serial()
            # _close_conn()
            recv_buf = ""  # reset buffer


if __name__ == '__main__':
    # Place in main code
    html_file = ("/webpage.html")  # this is the path to the html file on the pico filesystem
    _thread.start_new_thread(ESP8266Webserver(html_file), ())  # starts the webserver in a _thread
