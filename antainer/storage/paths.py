import os
import sys

def resolve_storage_base(
    is_android: bool,
    is_root_available: bool,
    subfolder: str = "images",
) -> str:
    """
    Resolves the base storage path for Antainer assets using platform and
    root availability flags.
    """
    # Case 1: Unprivileged user on Android with root (su) access available
    if is_android and is_root_available:
        if os.path.exists("/data/local"):
            base_path = "/data/local/.antainer"
        else:
            print("[Antainer] Error: Android environment detected, but '/data/local' is inaccessible.")
            sys.exit(1)

    # Case 2: Standard user on non-Android or unrooted system
    else:
        home = os.environ.get("HOME", os.path.expanduser("~"))

        if not home or home in ("/", "//", "/root"):
            print("[Antainer] Error: Unable to determine a valid home directory for storage.")
            sys.exit(1)

        base_path = os.path.join(home, ".antainer")

    target_dir = os.path.join(base_path, subfolder)
    return target_dir
