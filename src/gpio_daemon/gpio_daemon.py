"""Main module for the GPIO Daemon Demo package."""

import configparser
import logging
import socket
import threading

import gpiod

from . import accessory as acc

# Setup Configuration
config = configparser.ConfigParser()
config.read("config.ini")

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Daemon:
    """UDP daemon for controlling GPIO devices on Raspberry Pi.

    This daemon listens for UDP commands on a configurable IP address and port,
    parses the commands, and executes the appropriate GPIO operations on
    connected devices.

    The daemon supports multi-threaded command processing to handle multiple
    concurrent requests without blocking.

    Attributes:
        sock (socket.socket): UDP socket for receiving commands.
        sock_lock (threading.Lock): Thread lock for socket operations.
        led (acc.LED): LED accessory instance for GPIO control.

    Example:
        >>> daemon = Daemon()
        >>> daemon.cmd_listener()  # Starts listening for commands
    """

    def __init__(self) -> None:
        """Initialize the GPIO daemon.

        Sets up a UDP socket bound to the configured IP address and port,
        creates a thread lock for safe concurrent access, and initializes
        the LED accessory for GPIO control.

        Raises:
            OSError: If socket binding fails.
            ConfigParser.Error: If configuration file is invalid.
        """
        # Specify socket address family (IPv4) and type (Datagram)
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        # Bind to socket at <udp_ip:udp_port>
        self.sock.bind(
            (
                config["NETWORK"]["udp_ip"],
                int(config["NETWORK"]["udp_port"])
            )
        )
        # Put a lock on the socket in a thread
        self.sock_lock = threading.Lock()

        # Initialize LED accessory
        self.led = acc.LED()

    def cmd_listener(self) -> None:
        """Listen for incoming UDP commands and spawn handler threads.

        This is the main loop, which continuously listens for UDP packets on the
        configured socket. When a command is received, it spawns a new daemon
        thread to handle the command processing, allowing multiple commands to
        be processed concurrently.

        The received payload is decoded from UTF-8, stripped of whitespace,
        and split into command components before being passed to the handler.

        Raises:
            OSError: If socket operations fail (logged but not re-raised).

        Note:
            This method blocks indefinitely. Use threading or multiprocessing
            if you need to run other code concurrently.
        """
        while True:
            try:
                payload, client_addr = self.sock.recvfrom(1024)
                cmd_payload = payload.decode().strip("\n").strip("\r").split()
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
                logger.exception("Socket error occurred")

    def cmd_handler(
        self,
        cmd: list[str],
        sock: socket.socket,
        addr: tuple[str, int]
    ) -> None:
        """Handle incoming command and send response to client.

        This method processes a parsed command, determines the target device,
        executes the appropriate action, and sends a response back to the
        client.

        Args:
            cmd (list[str]): Parsed command components (e.g., ['led', 'power',
            'on']).
            sock (socket.socket): UDP socket for sending response.
            addr (tuple[str, int]): Client address (IP, port) for response.

        Command Format:
            - cmd[0]: Device name (e.g., 'led')
            - cmd[1]: Action category (e.g., 'power')
            - cmd[2]: Action (e.g., 'on', 'off')

        Response Format:
            - SUCCESS: "SUCCESS: <original command>"
            - FAILURE: "FAIL: Invalid Command"

        Example:
            cmd = ['led', 'power', 'on'] -> Calls self.led.power_on()
        """
        with self.sock_lock:
            dev = cmd[0].replace("-", "_")

            if dev in ["led"]:
                msg = self.cmd_parser(getattr(self, dev), cmd)
            else:
                msg = "FAIL: Invalid Command\n"

            sock.sendto(msg.encode("utf-8"), addr)
            logger.debug(
                "ADDRESS: %s, CMD: %s",
                addr,
                " ".join(cmd)
            )

    def cmd_parser(self, dev: "acc.Accessory", cmd: list[str]) -> str:
        """Parse command and execute the corresponding device method.

        This method takes a command list and constructs a method name by
        combining the action category and action (cmd[1] + '_' + cmd[2]). It
        then attempts to find and execute the corresponding method on the
        device object.

        Args:
            dev (acc.Accessory): The device object to execute the command on.
            cmd (list[str]): Command components [device, category, action].

        Returns:
            str: Success or failure message for the client.

        Command Examples:
            - ['led', 'power', 'on'] -> dev.power_on()
            - ['led', 'power', 'off'] -> dev.power_off()

        Returns:
            - "SUCCESS: <command>" if method execution succeeds
            - "FAIL: Unknown command <command>" if method doesn't exist

        Note:
            Uses opinionated function naming convention: {category}_{action}
        """
        fxn_name = f"{cmd[1]}_{cmd[2]}"

        try:
            fxn = getattr(dev, fxn_name)
        except AttributeError:
            return f'FAIL: Unknown command {" ".join(cmd)}\n'

        fxn()

        return f'SUCCESS: {" ".join(cmd)}\n'


# GLOBALS

def assert_out(pin: int, chip_path: str = "/dev/gpiochip4") -> gpiod.LineRequest:
    """Assert a GPIO pin as output and return the line request."""
    try:
        chip = gpiod.Chip(chip_path)

        return chip.request_lines(
            consumer="gpio-daemon",
            config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
        )
    except Exception:
        logger.exception("Failed to assert GPIO pin %s on %s", pin, chip_path)
        raise


def power_on(line_request: gpiod.LineRequest, pin: int) -> None:
    """Turn on power to a GPIO pin."""
    try:
        line_request.set_value(pin, gpiod.line.Value.ACTIVE)
        logger.info("Powered ON GPIO pin %s", pin)
    except Exception:
        logger.exception("Failed to power on GPIO pin %s", pin)
        raise


def power_off(line_request: gpiod.LineRequest, pin: int) -> None:
    """Turn off power to a GPIO pin."""
    try:
        line_request.set_value(pin, gpiod.line.Value.INACTIVE)
        logger.info("Powered OFF GPIO pin %s", pin)
    except Exception:
        logger.exception("Failed to power off GPIO pin %s", pin)
        raise
