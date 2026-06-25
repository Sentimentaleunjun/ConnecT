"""Recursive descent parser for ConnecT."""

from .ast_nodes import AppNode, DatabaseNode, EnvNode, NetworkNode, ProgramNode
from .exceptions import ParserError
from .tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse(self) -> ProgramNode:
        program = ProgramNode()
        while not self._check(TokenType.EOF):
            if self._check(TokenType.APP):
                program.apps.append(self.parse_app())
            elif self._check(TokenType.DATABASE):
                program.databases.append(self.parse_database())
            else:
                token = self._peek()
                raise ParserError("Expected top-level app or database block", token.line)
        self._consume(TokenType.EOF, "Expected end of file")
        return program

    def parse_app(self) -> AppNode:
        app_token = self._consume(TokenType.APP, "Expected app")
        name = self._consume_after_keyword(TokenType.STRING, "Expected STRING after app", app_token)
        node = AppNode(name=str(name.value), line=app_token.line)
        env_seen = False
        self._consume(TokenType.LBRACE, "Expected '{' after app name")
        while not self._check(TokenType.RBRACE):
            if self._check(TokenType.EOF):
                raise ParserError("Expected '}' to close app block", app_token.line)
            if self._check(TokenType.RUNTIME):
                keyword = self._advance()
                if node.runtime is not None:
                    raise ParserError("Duplicate runtime declaration", keyword.line)
                value = self._consume_after_keyword(TokenType.IDENTIFIER, "Expected IDENTIFIER after runtime", keyword)
                node.runtime = str(value.value)
                node.runtime_line = value.line
            elif self._check(TokenType.ENTRYPOINT):
                keyword = self._advance()
                if node.entrypoint is not None:
                    raise ParserError("Duplicate entrypoint declaration", keyword.line)
                value = self._consume_after_keyword(TokenType.STRING, "Expected STRING after entrypoint", keyword)
                node.entrypoint = str(value.value)
                node.entrypoint_line = value.line
            elif self._check(TokenType.NETWORK):
                if node.network is not None:
                    raise ParserError("Duplicate network block", self._peek().line)
                node.network = self.parse_network()
            elif self._check(TokenType.ENV):
                if env_seen:
                    raise ParserError("Duplicate env block", self._peek().line)
                env_seen = True
                node.env = self.parse_env()
            else:
                token = self._peek()
                raise ParserError("Expected runtime, entrypoint, network, env, or '}'", token.line)
        self._consume(TokenType.RBRACE, "Expected '}' after app block")
        return node

    def parse_database(self) -> DatabaseNode:
        db_token = self._consume(TokenType.DATABASE, "Expected database")
        name = self._consume_after_keyword(TokenType.STRING, "Expected STRING after database", db_token)
        node = DatabaseNode(name=str(name.value), line=db_token.line)
        env_seen = False
        self._consume(TokenType.LBRACE, "Expected '{' after database name")
        while not self._check(TokenType.RBRACE):
            if self._check(TokenType.EOF):
                raise ParserError("Expected '}' to close database block", db_token.line)
            if self._check(TokenType.ENGINE):
                keyword = self._advance()
                if node.engine is not None:
                    raise ParserError("Duplicate engine declaration", keyword.line)
                value = self._consume_after_keyword(TokenType.IDENTIFIER, "Expected IDENTIFIER after engine", keyword)
                node.engine = str(value.value)
                node.engine_line = value.line
            elif self._check(TokenType.ENV):
                if env_seen:
                    raise ParserError("Duplicate env block", self._peek().line)
                env_seen = True
                node.env = self.parse_env()
            else:
                token = self._peek()
                raise ParserError("Expected engine, env, or '}'", token.line)
        self._consume(TokenType.RBRACE, "Expected '}' after database block")
        return node

    def parse_network(self) -> NetworkNode:
        network_token = self._consume(TokenType.NETWORK, "Expected network")
        node = NetworkNode(line=network_token.line)
        self._consume(TokenType.LBRACE, "Expected '{' after network")
        while not self._check(TokenType.RBRACE):
            if self._check(TokenType.EOF):
                raise ParserError("Expected '}' to close network block", network_token.line)
            if self._check(TokenType.DOMAIN):
                keyword = self._advance()
                if node.domain is not None:
                    raise ParserError("Duplicate domain declaration", keyword.line)
                value = self._consume_after_keyword(TokenType.STRING, "Expected STRING after domain", keyword)
                node.domain = str(value.value)
                node.domain_line = value.line
            elif self._check(TokenType.PORT):
                keyword = self._advance()
                if node.port is not None:
                    raise ParserError("Duplicate port declaration", keyword.line)
                if self._check(TokenType.IDENTIFIER) and self._peek().value == "auto":
                    value = self._advance()
                    node.port = "auto"
                    node.port_line = value.line
                elif self._check(TokenType.NUMBER):
                    value = self._advance()
                    node.port = int(value.value)  # type: ignore[arg-type]
                    node.port_line = value.line
                else:
                    raise ParserError("Expected NUMBER or auto after port", keyword.line)
            elif self._check(TokenType.SSL):
                keyword = self._advance()
                if node.ssl is not None:
                    raise ParserError("Duplicate ssl declaration", keyword.line)
                value = self._consume_after_keyword(TokenType.IDENTIFIER, "Expected auto after ssl", keyword)
                node.ssl = str(value.value)
                node.ssl_line = value.line
            else:
                token = self._peek()
                raise ParserError("Expected domain, port, ssl, or '}'", token.line)
        self._consume(TokenType.RBRACE, "Expected '}' after network block")
        return node

    def parse_env(self) -> EnvNode:
        env_token = self._consume(TokenType.ENV, "Expected env")
        env = EnvNode()
        self._consume(TokenType.LBRACE, "Expected '{' after env")
        while not self._check(TokenType.RBRACE):
            if self._check(TokenType.EOF):
                raise ParserError("Expected '}' to close env block", env_token.line)
            key = self._consume(TokenType.IDENTIFIER, "Expected IDENTIFIER in env")
            value = self._consume(TokenType.STRING, f"Expected STRING after {key.value}")
            key_text = str(key.value)
            if key_text in env.values:
                raise ParserError(f"Duplicate env variable {key_text!r}", key.line)
            env.values[key_text] = str(value.value)
            env.lines[key_text] = key.line
        self._consume(TokenType.RBRACE, "Expected '}' after env block")
        return env

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserError(message, self._peek().line)

    def _consume_after_keyword(self, token_type: TokenType, message: str, keyword: Token) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserError(message, keyword.line)

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type == token_type

    def _advance(self) -> Token:
        token = self.tokens[self.position]
        self.position += 1
        return token

    def _peek(self) -> Token:
        return self.tokens[self.position]
