import argparse
import sys
from typing import List, Optional

def create_parser() -> argparse.ArgumentParser:
    """Construct and return the root argument parser for Antainer."""
    parser = argparse.ArgumentParser(
        prog="antainer",
        description="Run OCI container environments on Android using chroot.",
        epilog="Designed for reproducible Android development environments.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Valid Antainer operations",
        help="Use 'antainer <command> --help' for detailed sub-command information.",
        required=True,
    )

    # --- Command: pull ---
    pull_parser = subparsers.add_parser(
        "pull",
        help="Fetch and unpack an OCI container image into a local rootfs",
    )
    pull_parser.add_argument(
        "image",
        type=str,
        help="OCI image reference (e.g., alpine:latest, debian:bookworm)",
    )
    pull_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Custom name for the extracted environment directory",
    )

    # --- Command: enter ---
    enter_parser = subparsers.add_parser(
        "enter",
        help="Mount filesystems and launch an interactive chroot shell",
    )
    enter_parser.add_argument(
        "target",
        type=str,
        help="Name or path of the extracted rootfs environment",
    )
    enter_parser.add_argument(
        "-s",
        "--shell",
        type=str,
        default="/bin/sh",
        help="Shell executable to execute inside chroot (default: /bin/sh)",
    )

    # --- Command: clean ---
    clean_parser = subparsers.add_parser(
        "clean",
        help="Safely unmount pseudo-filesystems (/proc, /sys, /dev) from an environment",
    )
    clean_parser.add_argument(
        "target",
        type=str,
        help="Name or path of the extracted rootfs environment",
    )

    # --- Command: create ---
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new container instance from a pulled OCI image",
    )
    create_parser.add_argument(
        "image",
        type=str,
        help="Source image name/tag (e.g., alpine:latest)",
    )
    create_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Name for the created container (defaults to auto-generated or image name)",
    )

    # --- Command: build ---
    build_parser = subparsers.add_parser(
        "build",
        help="Parse a Containerfile/Dockerfile recipe and generate a rootfs layout",
    )
    build_parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="Containerfile",
        help="PAth to recipe file (default: Containerfile)",
    )
    build_parser.add_argument(
        "-t",
        "--tag",
        type=str,
        required=True,
        help="Tag/name to assign to the target environment",
    )

    return parser

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse raw arguments or sys.argv if none provided."""
    parser = create_parser()

    # If no arguments were passed on the command line, show the help menu automatically
    if args is None and len(sys.argv) == 1:
        args = ["--help"]

    return parser.parse_args(args)
