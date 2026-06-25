"""Token definitions for ServerDSL."""

from dataclasses import dataclass
from enum import StrEnum, auto


class TokenType(StrEnum):
    APP = auto()
    DATABASE = auto()
    RUNTIME = auto()
    ENTRYPOINT = auto()
    NETWORK = auto()
    ENV = auto()
    ENGINE = auto()
    DOMAIN = auto()
    PORT = auto()
    SSL = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    LBRACE = auto()
    RBRACE = auto()

    EOF = auto()


KEYWORDS: dict[str, TokenType] = {
    "app": TokenType.APP,
    "database": TokenType.DATABASE,
    "runtime": TokenType.RUNTIME,
    "entrypoint": TokenType.ENTRYPOINT,
    "network": TokenType.NETWORK,
    "env": TokenType.ENV,
    "engine": TokenType.ENGINE,
    "domain": TokenType.DOMAIN,
    "port": TokenType.PORT,
    "ssl": TokenType.SSL,
}


@dataclass(frozen=True, slots=True)
class Token:
    type: TokenType
    value: str | int | None
    line: int
