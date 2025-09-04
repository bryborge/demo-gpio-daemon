#!/usr/bin/env python3
"""Test client for the GPIO daemon."""

import socket
import sys
import time


def send_command(command: str, host: str = '127.0.0.1', port: int = 5005) -> str:
    """Send a command to the GPIO daemon and return the response."""
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)  # 5 second timeout

        # Send command
        sock.sendto(command.encode('utf-8'), (host, port))

        # Receive response
        response, _ = sock.recvfrom(1024)
        sock.close()

        return response.decode('utf-8').strip()

    except socket.timeout:
        return "ERROR: Timeout waiting for response"
    except Exception as e:
        return f"ERROR: {e}"


def main():
    """Main function to test the GPIO daemon."""
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <command>")
        print("Examples:")
        print("  python test_client.py 'led power on'")
        print("  python test_client.py 'led power off'")
        sys.exit(1)

    command = ' '.join(sys.argv[1:])
    print(f"Sending command: {command}")

    response = send_command(command)
    print(f"Response: {response}")


def demo():
    """Run a quick demo of turning LED on and off."""
    print("Running LED demo...")

    # Turn LED on
    response = send_command('led power on')
    print(f"LED ON: {response}")

    time.sleep(2)

    # Turn LED off
    response = send_command('led power off')
    print(f"LED OFF: {response}")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo()
    else:
        main()
