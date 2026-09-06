import argparse
import sys
from antainer.registry import pull_and_extract_oci_image

def handle_pull(args: argparse.Namespace) -> None:
    print(f"[Antainer] Pulling image: {args.image}")
    try:
        rootfs_path = pull_and_extract_oci_image(
            image_ref=args.image,
            custom_name = args.name,
        )
        print(f"[Antainer] Pull operation completed -> {rootfs_path}")
    except Exception as e:
        print(f"[Antainer] Error fetching OCI image: {e}")
        sys.exit(1)

def handle_enter(args: argparse.Namespace) -> None:
    print(f"[Antainer] Entering target: {args.target} with shell {args.shell}")

def handle_clean(args: argparse.Namespace) -> None:
    print(f"[Antainer] Cleaning target: {args.target}")

def handle_create(args: argparse.Namespace) -> None:
    print(f"[Antainer] Creating container '{container_name}' from image '{args.image}'")

def handle_build(args: argparse.Namespace) -> None:
    print(f"[Antainer] Building tag '{args.tag}' from file '{args.file}'")
