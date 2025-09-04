"""Entry point for the demo gpio daemon package."""

from . import gpio_daemon

print('================')
print('Demo GPIO Daemon')
print('================')

gd = gpio_daemon.Daemon()
gd.cmd_listener()
