import subprocess
from typing import List, Union

def run_command(
    cmd: Union[str, List[str]],
    is_android: bool = False,
    requires_root: bool = False,
    check: bool = True,
    interactive: bool = False,
) -> subprocess.CompletedProcess:
    """
    Central command executor for Antainer.

    Formats and executes system commands based on the operating platform.
    On Android, if requires_root is True, it wraps the command in `su -c`.

    Args:
        cmd: Command string or list of argument strings.
        is_android: Whether Antainer is running in an Android environment.
        requires_root: Whether the command requires elevated (root) privileges.
        check: If True, raises PermissionError / RuntimeError on non-zero exit codes.
        interactive:

    Returns:
        subprocess.CompletedProcess containing stdout and stderr.
    """
    # Convert command list into a single shell command string if needed
    if isinstance(cmd, list):
        # Shell-quote arguments if passing a list to su or shell execution
        cmd_str = " ".join(f"'{arg}'" if " " in arg else arg for arg in cmd)
    else:
        cmd_str = cmd

    # Determine execution wrapper
    if is_android and requires_root:
        exec_args = ["su", "-c", cmd_str]
    else:
        # On non-Android or unprivileged calls, execute via shell or direct list
        if isinstance(cmd, list):
            exec_args = cmd
        else:
            exec_args = ["/bin/sh", "-c", cmd_str]

    if interactive:
        # Pass standard I/O streams directly to the terminal
        res = subprocess.run(exec_args)
        return res

    # Execute process
    res = subprocess.run(exec_args, capture_output=True, text=True)

    # Standardized error handling
    if check and res.returncode != 0:
        err_msg = res.stderr.strip() or f"Command failed with return code {res.returncode}"
        if is_android and requires_root:
            raise PermissionError(f"Root operation failed [{cmd_str}]: {err_msg}")
        raise RuntimeError(f"Command failed [{cmd_str}]: {err_msg}")

    return res
