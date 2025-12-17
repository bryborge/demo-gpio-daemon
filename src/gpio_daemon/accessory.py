"""Accessory module for GPIO devices."""

from . import gpio_daemon as daemon


class Accessory:
    """Base class for GPIO accessories."""

    def __init__(self, cfg_section: str) -> None:
        """Initialize the accessory with configuration section."""
        self.cfg_section = cfg_section
        self.power_pin = int(daemon.config[cfg_section]["power_pin"])
        self.power_line = daemon.assert_out(self.power_pin, cfg_section)

    def power_on(self) -> None:
        """Turn on the accessory."""
        daemon.power_on(self.power_line, self.power_pin)

    def power_off(self) -> None:
        """Turn off the accessory."""
        daemon.power_off(self.power_line, self.power_pin)


class LED(Accessory):
    """LED accessory class."""

    def __init__(self) -> None:
        """Initialize the LED with the gpiochip4 configuration."""
        super().__init__("/dev/gpiochip4")
