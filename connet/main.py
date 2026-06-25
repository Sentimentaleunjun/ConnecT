"""Command line interface for ConnecT."""

import argparse
import sys

from .compiler import Compiler
from .exceptions import ConnecTError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile ConnecT .ct files to JSON.")
    parser.add_argument("file", help="Path to a .ct file")
    parser.add_argument(
        "--check-entrypoint-files",
        action="store_true",
        help="Require app entrypoint paths to exist relative to the .ct file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        compiler = Compiler(check_entrypoint_files=args.check_entrypoint_files)
        data = compiler.compile_file(args.file)
        print(Compiler.to_json(data))
        return 0
    except ConnecTError as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
