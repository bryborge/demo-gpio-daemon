"""Entry point for the demo gpio daemon package."""

from . import gpio_daemon

gd = gpio_daemon.Daemon()
gd.cmd_listener()
