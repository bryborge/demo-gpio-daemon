# Sandbox (Python Edition)

A portable Python Development Environment for experimentation and glory.

## ⚙️ Dependencies

-   [Podman](https://podman.io/)

## 🔧 Up and Running

These instructions assume you have the above dependencies installed, configured,
and running.

1.  Build and run the container.

    ```sh
    podman compose up -d
    ```

    That's it. If you want to drop into the container at a shell, run:

    ```sh
    podman compose exec sandbox-py bash
    ```

2.  Install dependencies (inside the container):

    ```sh
    pip install -e .[dev]
    ```

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
