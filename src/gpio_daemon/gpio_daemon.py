"""Main module for the GPIO Daemon Demo package."""

import configparser
import logging
import socket
import threading

import gpiod

from . import accessory as acc

# Setup Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Daemon:
    def __init__(self) -> None:
        # Specify socket address family (IPv4) and type (Datagram)
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        # Bind to socket at <udp_ip:udp_port>
        self.sock.bind(
            (
                config['NETWORK']['udp_ip'],
                int(config['NETWORK']['udp_port'])
            )
        )
        # Put a lock on the socket in a thread
        self.sock_lock = threading.Lock()

        # Initialize LED accessory
        self.led = acc.LED()

    def cmd_listener(self) -> None:
        while True:
            try:
                payload, client_addr = self.sock.recvfrom(1024)
                cmd_payload = payload.decode().strip('\n').strip('\r').split()
                cmd_thread = threading.Thread(
                    target=self.cmd_handler,
                    args=(
                        cmd_payload,
                        self.sock,
                        client_addr
                    )
                )
                cmd_thread.daemon = True
                cmd_thread.start()
            except OSError:
                logger.exception('Socket error: %s')

    def cmd_handler(
        self,
        cmd: list[str],
        sock: socket.socket,
        addr: tuple[str, int]
    ) -> None:
        with self.sock_lock:
            dev = cmd[0].replace('-', '_')

            if dev in ['led']:
                msg = self.cmd_parser(getattr(self, dev), cmd)
            else:
                msg = 'FAIL: Invalid Command\n'

            sock.sendto(msg.encode('utf-8'), addr)
            logger.debug(
                'ADDRESS: %s, CMD: %s',
                addr,
                ' '.join(cmd)
            )

    def cmd_parser(self, dev: 'acc.Accessory', cmd: list[str]) -> str:
        # Example commands (cmd):
        #   - led power on
        #   - led power off
        fxn_name = f"{cmd[1]}_{cmd[2]}"

        try:
            # opinionated function naming ...
            fxn = getattr(dev, fxn_name)
        except AttributeError as err:
            return f'FAIL: Unknown command {" ".join(cmd)}\n'

        fxn()

        return f'SUCCESS: {" ".join(cmd)}\n'


# GLOBALS

def assert_out(pin: int, chip_path: str = '/dev/gpiochip4') -> gpiod.LineRequest:
    """Assert a GPIO pin as output and return the line request."""
    try:
        chip = gpiod.Chip(chip_path)
        line_request = chip.request_lines(
            consumer="gpio-daemon",
            config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
        )
        return line_request
    except Exception as e:
        logger.error(f"Failed to assert GPIO pin {pin} on {chip_path}: {e}")
        raise


def power_on(line_request: gpiod.LineRequest, pin: int) -> None:
    """Turn on power to a GPIO pin."""
    try:
        line_request.set_value(pin, gpiod.line.Value.ACTIVE)
        logger.info(f"Powered ON GPIO pin {pin}")
    except Exception as e:
        logger.error(f"Failed to power on GPIO pin {pin}: {e}")
        raise


def power_off(line_request: gpiod.LineRequest, pin: int) -> None:
    """Turn off power to a GPIO pin."""
    try:
        line_request.set_value(pin, gpiod.line.Value.INACTIVE)
        logger.info(f"Powered OFF GPIO pin {pin}")
    except Exception as e:
        logger.error(f"Failed to power off GPIO pin {pin}: {e}")
        raise
