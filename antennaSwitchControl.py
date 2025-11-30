import socket
import time
from gpiozero import OutputDevice

out1 = OutputDevice(23, active_high=False, initial_value=False)
out2 = OutputDevice(22, active_high=False, initial_value=False)
out3 = OutputDevice(27, active_high=False, initial_value=False)

HOST = '192.168.152.12'
PORT = 5000
SWITCH_DELAY_MS = 10
DEFAULT_ANTENNA = 1

antennas = [out1, out2, out3]
current_antenna = DEFAULT_ANTENNA

def turn_on_antenna(antenna_number):
    global current_antenna
    for antenna in antennas:
        antenna.off()

    time.sleep(SWITCH_DELAY_MS / 1000)
    if antenna_number:
        antennas[antenna_number - 1].on()
        current_antenna = antenna_number
        print('current antenna: ' + str(current_antenna))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Antenna server is listening on port: {PORT}...")

    turn_on_antenna(DEFAULT_ANTENNA)

    while True:
        conn, addr = s.accept()
        print(f"Connected with: {addr}")
        with conn:
            data = conn.recv(1024)
            print("RAW data:", data)
            if not data:
                continue

            cmd = data.decode('utf-8', errors='replace').strip()
            print(f"Command received: {repr(cmd)}")
            
            # Just turn on antenna from cmd number: '1' for antenna no.1, '2' for antenna no.2 .. . . . ..
            if cmd.isnumeric():
                turn_on_antenna(int(cmd))
                resp = "Antenna no." + str(cmd) + "\n"
                conn.sendall(resp.encode("ascii", errors="ignore"))
            elif cmd == 'get':
                print('current antenna: ' + str(current_antenna))
                conn.sendall(str(current_antenna).encode("ascii", errors="ignore"))

            conn.close()
            print("Connection closed\n")
