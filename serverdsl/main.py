"""Command line interface for ServerDSL."""

import argparse
import sys

from .compiler import Compiler
from .exceptions import ServerDSLError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile ServerDSL .sdl files to JSON.")
    parser.add_argument("file", help="Path to a .sdl file")
    parser.add_argument(
        "--check-entrypoint-files",
        action="store_true",
        help="Require app entrypoint paths to exist relative to the .sdl file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        compiler = Compiler(check_entrypoint_files=args.check_entrypoint_files)
        data = compiler.compile_file(args.file)
        print(Compiler.to_json(data))
        return 0
    except ServerDSLError as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
