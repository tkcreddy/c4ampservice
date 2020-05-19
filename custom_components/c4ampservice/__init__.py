import logging
import socket
import random


_LOGGER = logging.getLogger(__name__)

DOMAIN = "c4amp_services"

ATTR_ZONE = "zone"
DEFAULT_ZONE = ""
ATTR_SOURCE = "source"
DEFAULT_SOURCE = ""
ATTR_VOLUME = "volume"


ZONE_SRC_CMD = 'c4.amp.out 0' # Play wireless bridge Input 2 select
ZONE_VOL_CMD = 'c4.amp.chvol 0'
ZONE_MUT_CMD = 'c4.amp.mute 0'
VOLUME_MIN = 156
VOLUME_MAX = 255
VOLUME_DEFAULT = 45
volume_select = VOLUME_MIN + VOLUME_DEFAULT
volume_select = hex(volume_select)[2:]

host = '192.168.1.247'
port = 8750

def send_udp_command(command, host, port):
    COUNTER = "0s2a" + str(random.randint(10, 99))
    COMMAND = COUNTER + " " + command + " \r\n"
    _LOGGER.warning('Sending command: %s', COMMAND)
    HOST = host
    PORT = port
    sent = COUNTER + " " + "000"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(20)
        sock.sendto(bytes(COMMAND, "utf-8"), (HOST, PORT))
        received = str(sock.recv(1024), "utf-8")
        recv=str(received).rstrip()
        if sent[-6] == (recv[-6]):
            _LOGGER.warning("Command sent!!. Response: %s", str(received))
            return True
        else:
            _LOGGER.warning("Command Failed with bad response!!. Response: %s", str(received))
            print("was failed in try")
            return False
    except:
        print("Host not responding Please check if c4Amp is up or IP is correct")
        return False


def setup(hass, config):

    def switch_of_zone(call):
        zone = call.data.get(ATTR_ZONE, DEFAULT_ZONE)
        cmd = ZONE_SRC_CMD + zone + " " + "00"
        send_udp_command(cmd,host,port)

    def handle_switch_c4ampon_zone(call):
        zone = call.data.get(ATTR_ZONE, DEFAULT_ZONE)
        source = call.data.get(ATTR_SOURCE, DEFAULT_SOURCE)
        cmd = ZONE_SRC_CMD + zone + " " + "0" + source
        cmd1 = ZONE_VOL_CMD + zone + " " + volume_select
        send_udp_command(cmd,host,port)
        send_udp_command(cmd1,host,port)

    hass.services.register(DOMAIN, "switch_of_zone", switch_of_zone)
    hass.services.register(DOMAIN, "handle_switch_on_zone", handle_switch_c4ampon_zone)
    return True
