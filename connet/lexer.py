"""Lexer for ConnecT source files."""

from .exceptions import LexerError
from .tokens import KEYWORDS, Token, TokenType


class Lexer:
    """Converts ConnecT source text into tokens while tracking line numbers."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.line = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while not self._is_at_end():
            char = self._peek()
            if char in " \t\r":
                self._advance()
            elif char == "\n":
                self._advance()
                self.line += 1
            elif char == "{":
                self._advance()
                tokens.append(Token(TokenType.LBRACE, "{", self.line))
            elif char == "}":
                self._advance()
                tokens.append(Token(TokenType.RBRACE, "}", self.line))
            elif char in {'"', '“'}:
                tokens.append(self._string())
            elif char.isdigit():
                tokens.append(self._number())
            elif char.isalpha() or char == "_":
                tokens.append(self._identifier_or_keyword())
            else:
                raise LexerError(f"Unexpected character {char!r}", self.line)
        tokens.append(Token(TokenType.EOF, None, self.line))
        return tokens

    def _identifier_or_keyword(self) -> Token:
        start = self.position
        while not self._is_at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        text = self.source[start:self.position]
        return Token(KEYWORDS.get(text, TokenType.IDENTIFIER), text, self.line)

    def _number(self) -> Token:
        start = self.position
        while not self._is_at_end() and self._peek().isdigit():
            self._advance()
        return Token(TokenType.NUMBER, int(self.source[start:self.position]), self.line)

    def _string(self) -> Token:
        opener = self._advance()
        closer = '”' if opener == '“' else '"'
        start_line = self.line
        chars: list[str] = []
        while not self._is_at_end():
            char = self._advance()
            if char == closer:
                return Token(TokenType.STRING, "".join(chars), start_line)
            if char == "\n":
                self.line += 1
            chars.append(char)
        raise LexerError("Unterminated string", start_line)

    def _peek(self) -> str:
        return self.source[self.position]

    def _advance(self) -> str:
        char = self.source[self.position]
        self.position += 1
        return char

    def _is_at_end(self) -> bool:
        return self.position >= len(self.source)
