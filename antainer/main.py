import sys
from antainer.cli import parse_args
from antainer.core import init_context
from antainer.handlers import COMMAND_HANDLERS


def main() -> None:
    # 1. Parse arguments (displays help and exits if invalid/missing)
    args = parse_args()

    # 2. Initialize in-memory runtime context and execute system checks
    print("[Antainer] Initializing system checks...")
    try:
        ctx = init_context()
    except RuntimeError as err:
        print(f"[Antainer] Error:\n{err}")
        sys.exit(1)

    print("[Antainer] Success: Environment checks passed.")
    print(f"[Antainer] Images directory: {ctx.images_dir}")

    # 3. Dispatch to handler module
    handler = COMMAND_HANDLERS.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"[Antainer] Error: Unknown command '{args.command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()