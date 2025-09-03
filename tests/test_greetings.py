"""Test Suite for the Greetings Module."""

from greetings.main import main


class TestGreetingsModule:
    """Unit Tests for the Greetings Module."""

    def test_greeting(self) -> None:
        """Test that the main function returns the expected message."""
        result = main()
        assert result == "Hello World"

    def test_greeting_is_string(self) -> None:
        """Test that the main function returns a string."""
        result = main()
        assert isinstance(result, str)

    def test_greeting_not_empty(self) -> None:
        """Test that the greeting function doesn't return an empty string."""
        result = main()
        assert len(result) > 0
