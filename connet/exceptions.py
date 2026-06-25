"""Exceptions for ConnecT."""


class ConnecTError(Exception):
    """Base class for ConnecT errors with optional source line."""

    def __init__(self, message: str, line: int | None = None) -> None:
        self.message = message
        self.line = line
        if line is None:
            super().__init__(message)
        else:
            super().__init__(f"Line {line}:\n{message}")


class LexerError(ConnecTError):
    """Raised when lexing fails."""


class ParserError(ConnecTError):
    """Raised when parsing fails."""


class ValidationError(ConnecTError):
    """Raised when semantic validation fails."""
