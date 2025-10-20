#!/usr/bin/env python3
import argparse
import shlex
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: list[str]):
    """
    run given shell command
    """
    print(cmd)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(shlex.quote(part) for part in e.cmd)
        print(f"Error:\n\t`{cmd_str}`\nfailed with exit code {e.returncode}")
        sys.exit(e.returncode)


def find_proto_files(base_dir: Path):
    """
    Recursively find all .proto files in the given directory using pathlib.

    Args:
        base_dir (str): The root directory to search from.

    Returns:
        list of Path: List of pathlib.Path objects pointing to .proto files.
    """
    return list(base_dir.rglob("*.proto"))


def generate_proto(nanopb_dir: Path, output_dir: Path):
    """
    Generate nanopb protobuf code with C++ descriptors.

    Args:
        nanopb_dir (Path): Path to nanopb root directory.
        output_dir (Path): Output directory for generated files (created if needed).

    Runs the nanopb_generator.py script with C++ descriptor support on all .proto files
    found in the current directory.
    """
    nanopb_script = nanopb_dir / "generator" / "nanopb_generator.py"
    output_dir.mkdir(exist_ok=True)

    cmd = [
        "python",
        str(nanopb_script),
        "-I",
        ".",
        "--cpp-descriptors",
        "-S",
        ".cpp",
        "--output-dir",
        str(output_dir),
    ]
    cmd.extend([str(p) for p in find_proto_files(Path("."))])
    run_cmd(cmd)


def main():
    parser = argparse.ArgumentParser(
        prog="build.py",
    )

    parser.add_argument(
        "nanopb_dir",
        type=Path,
        help="Path to a nanopb clone",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default="out",
        type=Path,
        help="Specify custom output directory (default: out)",
    )

    arg = parser.parse_args()
    generate_proto(arg.nanopb_dir, arg.output_dir)


if __name__ == "__main__":
    main()
