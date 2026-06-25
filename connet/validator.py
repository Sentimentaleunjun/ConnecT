"""Semantic validator for ConnecT ASTs."""

from pathlib import Path

from .ast_nodes import AppNode, DatabaseNode, ProgramNode
from .exceptions import ValidationError

ALLOWED_RUNTIMES = {"flask", "fastapi", "django", "node"}
ALLOWED_ENGINES = {"mysql", "postgres", "sqlite", "redis", "mongodb"}


class Validator:
    def __init__(self, base_dir: str | Path | None = None, check_entrypoint_files: bool = False) -> None:
        self.base_dir = Path(base_dir or ".")
        self.check_entrypoint_files = check_entrypoint_files

    def validate(self, program: ProgramNode) -> None:
        self._validate_unique_names(program.apps, "app")
        self._validate_unique_names(program.databases, "database")
        for app in program.apps:
            self._validate_app(app)
        for database in program.databases:
            self._validate_database(database)

    def _validate_unique_names(self, nodes: list[AppNode] | list[DatabaseNode], kind: str) -> None:
        seen: dict[str, int] = {}
        for node in nodes:
            if node.name in seen:
                raise ValidationError(f"Duplicate {kind} name {node.name!r}", node.line)
            seen[node.name] = node.line

    def _validate_app(self, app: AppNode) -> None:
        if app.runtime is None:
            raise ValidationError("Missing runtime", app.line)
        if app.runtime not in ALLOWED_RUNTIMES:
            raise ValidationError(f"Unknown runtime {app.runtime!r}", app.runtime_line)
        if not app.entrypoint:
            raise ValidationError("Missing entrypoint", app.line)
        if self.check_entrypoint_files and not (self.base_dir / app.entrypoint).exists():
            raise ValidationError(f"Entrypoint does not exist {app.entrypoint!r}", app.entrypoint_line)
        if app.network is None:
            raise ValidationError("Missing network block", app.line)
        if not app.network.domain:
            raise ValidationError("Missing domain", app.network.line)
        if app.network.port is None:
            raise ValidationError("Missing port", app.network.line)
        if isinstance(app.network.port, int) and not 1 <= app.network.port <= 65535:
            raise ValidationError("Port must be between 1 and 65535", app.network.port_line)
        if isinstance(app.network.port, str) and app.network.port != "auto":
            raise ValidationError("Port must be auto or an integer between 1 and 65535", app.network.port_line)
        if app.network.ssl is not None and app.network.ssl != "auto":
            raise ValidationError("ssl only supports 'auto'", app.network.ssl_line)

    def _validate_database(self, database: DatabaseNode) -> None:
        if database.engine is None:
            raise ValidationError("Missing engine", database.line)
        if database.engine not in ALLOWED_ENGINES:
            raise ValidationError(f"Unknown engine {database.engine!r}", database.engine_line)
