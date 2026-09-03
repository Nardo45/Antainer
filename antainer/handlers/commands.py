import argparse

def handle_pull(args: argparse.Namespace) -> None:
    print(f"[Antainer] Pulling image: {args.image}")

def handle_enter(args: argparse.Namespace) -> None:
    print(f"[Antainer] Entering target: {args.target} with shell {args.shell}")

def handle_clean(args: argparse.Namespace) -> None:
    print(f"[Antainer] Cleaning target: {args.target}")

def handle_create(args: argparse.Namespace) -> None:
    print(f"[Antainer] Creating container '{container_name}' from image '{args.image}'")

def handle_build(args: argparse.Namespace) -> None:
    print(f"[Antainer] Building tag '{args.tag}' from file '{args.file}'")
