"""AST node definitions for ServerDSL."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class EnvNode:
    values: dict[str, str] = field(default_factory=dict)
    lines: dict[str, int] = field(default_factory=dict)


@dataclass(slots=True)
class NetworkNode:
    domain: str | None = None
    port: str | int | None = None
    ssl: str | None = None
    line: int = 0
    domain_line: int | None = None
    port_line: int | None = None
    ssl_line: int | None = None


@dataclass(slots=True)
class AppNode:
    name: str
    line: int
    runtime: str | None = None
    entrypoint: str | None = None
    network: NetworkNode | None = None
    env: EnvNode = field(default_factory=EnvNode)
    runtime_line: int | None = None
    entrypoint_line: int | None = None


@dataclass(slots=True)
class DatabaseNode:
    name: str
    line: int
    engine: str | None = None
    env: EnvNode = field(default_factory=EnvNode)
    engine_line: int | None = None


@dataclass(slots=True)
class ProgramNode:
    apps: list[AppNode] = field(default_factory=list)
    databases: list[DatabaseNode] = field(default_factory=list)
