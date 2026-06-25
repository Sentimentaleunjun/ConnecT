"""Compiler utilities for ServerDSL: source -> validated JSON-ready data."""

import json
from pathlib import Path
from typing import Any

from .ast_nodes import AppNode, DatabaseNode, ProgramNode
from .lexer import Lexer
from .parser import Parser
from .validator import Validator


class Compiler:
    def __init__(self, base_dir: str | Path | None = None, check_entrypoint_files: bool = False) -> None:
        self.validator = Validator(base_dir=base_dir, check_entrypoint_files=check_entrypoint_files)

    def compile_source(self, source: str) -> dict[str, Any]:
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        self.validator.validate(program)
        return self.to_dict(program)

    def compile_file(self, path: str | Path) -> dict[str, Any]:
        file_path = Path(path)
        source = file_path.read_text(encoding="utf-8")
        compiler = Compiler(base_dir=file_path.parent, check_entrypoint_files=self.validator.check_entrypoint_files)
        return compiler.compile_source(source)

    @staticmethod
    def to_dict(program: ProgramNode) -> dict[str, Any]:
        return {
            "apps": [Compiler._app_to_dict(app) for app in program.apps],
            "databases": [Compiler._database_to_dict(database) for database in program.databases],
        }

    @staticmethod
    def to_json(data: dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def _app_to_dict(app: AppNode) -> dict[str, Any]:
        assert app.network is not None
        return {
            "name": app.name,
            "runtime": app.runtime,
            "entrypoint": app.entrypoint,
            "network": {
                "domain": app.network.domain,
                "port": app.network.port,
                "ssl": app.network.ssl,
            },
            "env": dict(app.env.values),
        }

    @staticmethod
    def _database_to_dict(database: DatabaseNode) -> dict[str, Any]:
        return {
            "name": database.name,
            "engine": database.engine,
            "env": dict(database.env.values),
        }
