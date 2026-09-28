import json
import os
import shutil
import tarfile
from antainer.core.exec import run_command

def get_staging_dir() -> str:
    """Returns an unprivileged temporary directory for staging downloads."""
    tmp_base = os.environ.get("TMPDIR", "/tmp")
    staging = os.path.join(tmp_base, "antainer_staging")
    os.makedirs(staging, exist_ok=True)
    return staging

def ensure_dir(path: str, is_android: bool = False, requires_root: bool = False) -> None:
    """Creates directory, escalating via 'su' if target is /data/local."""
    if is_android and requires_root:
        run_command(f"mkdir -p '{path}'", is_android=is_android, requires_root=True)
    else:
        os.makedirs(path, exist_ok=True)

def extract_layer(tar_path: str, destination: str, is_android: bool = False, requires_root: bool = False) -> None:
    """Extracts a tarball into destination rootfs using elevated su if on Android."""
    if is_android and requires_root:
        # Use system tar via su to preserve permissions, device nodes, and symlinks properly
        run_command(f"tar -xf '{tar_path}' -C '{destination}'", is_android=is_android, requires_root=True)
    else:
        with tarfile.open(tar_path, "r:*") as tar:
            tar.extractall(path=destination)

def copy_dir_tree(src: str, dst: str, is_android: bool = False, requires_root: bool = False) -> None:
    """Copies a directory tree, escalating via 'su' if operating on /data/local."""
    if is_android and requires_root:
        run_command(f"cp -a '{src}' '{dst}'", is_android=is_android, requires_root=True)
    else:
        shutil.copytree(src, dst, symlinks=True)

def write_json_file(filepath: str, data: dict, is_android: bool = False, requires_root: bool = False) -> None:
    """
    Writes a JSON object to a file.

    On Android / protected paths, stages the file in staging memory first
    and uses 'su' to copy it to destination.
    """
    if is_android and requires_root:
        staging_dir = get_staging_dir()
        temp_file = os.path.join(staging_dir, f"temp_{os.path.basename(filepath)}")

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        cmd = f"cp '{temp_file}' '{filepath}' && rm -f '{temp_file}'"
        run_command(
            f"cp '{temp_file}' '{filepath}' && rm -f '{temp_file}'",
            is_android=is_android,
            requires_root=True,
        )
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

