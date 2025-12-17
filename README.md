# GPIO Daemon Demo

A UDP daemon that runs on Raspberry Pi to control GPIO pins remotely. This demo controls an LED connected to GPIO pin 18.

## ⚙️ Dependencies

-   Python 3.11+
-   [Podman](https://podman.io/) (for containerized development)
-   Raspberry Pi with GPIO pins (for actual hardware control)

## 🔧 Up and Running

### For Development (Container)

These instructions assume you have Podman installed and configured.

1.  Build and run the container:

    ```sh
    podman compose up -d
    ```

2.  Drop into the container:

    ```sh
    podman compose exec demo-gpio-daemon bash
    ```

3.  Install dependencies (inside the container):

    ```sh
    pip install -e .[dev]
    ```

### For Raspberry Pi (Hardware)

1.  Install Python dependencies:

    ```sh
    pip install -e .
    ```

2.  Run the daemon:

    ```sh
    python -m gpio_daemon
    ```

## 🎮 Usage

### Starting the Daemon

The daemon listens for UDP commands on `127.0.0.1:5005` by default (configurable in `config.ini`).

```sh
python -m gpio_daemon
```

### Sending Commands

Use the test client to send commands:

```sh
# Turn LED on
python scripts/test_client.py "led power on"

# Turn LED off
python scripts/test_client.py "led power off"

# Run demo (turns LED on, waits 2 seconds, turns off)
python scripts/test_client.py demo
```

Or send UDP packets directly:

```sh
echo "led power on" | nc -u 127.0.0.1 5005
echo "led power off" | nc -u 127.0.0.1 5005
```

### Hardware Setup

Connect an LED to your Raspberry Pi:
- Connect LED anode to GPIO pin 18
- Connect LED cathode to ground through a 220Ω resistor

### Configuration

Edit `config.ini` to change network settings or GPIO pins.

### ⚙️ Build System

This project uses [setuptools](https://setuptools.pypa.io/en/latest/setuptools.html) for the build backend.

### ✅ Testing

This project uses the [pytest](https://docs.pytest.org/en/stable/) testing framework.

To run the test suite, simply run the command `pytest`.

## 🔌 Spinning Down

To spin the container down, run:

```sh
podman compose down
```

To clean up all the cache and generated files created during development:

```sh
make clean
```

## 📚 Resources

-   ["Official" Python Documentation](https://www.python.org/doc/)
-   [Pytest Documentation](https://docs.pytest.org/en/stable/)
-   [Setuptools Documentation](https://setuptools.pypa.io/en/latest/setuptools.html)
