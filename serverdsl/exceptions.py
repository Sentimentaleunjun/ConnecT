"""Exceptions for ServerDSL."""


class ServerDSLError(Exception):
    """Base class for ServerDSL errors with optional source line."""

    def __init__(self, message: str, line: int | None = None) -> None:
        self.message = message
        self.line = line
        if line is None:
            super().__init__(message)
        else:
            super().__init__(f"Line {line}:\n{message}")


class LexerError(ServerDSLError):
    """Raised when lexing fails."""


class ParserError(ServerDSLError):
    """Raised when parsing fails."""


class ValidationError(ServerDSLError):
    """Raised when semantic validation fails."""
