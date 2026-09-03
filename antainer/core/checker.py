import os
import shutil
import subprocess
from dataclasses import dataclass

@dataclass
class CheckResult:
    available: bool
    message: str

def is_android_environment() -> bool:
    """Check if the execution environment is an Android system."""
    return os.path.exists("/system/build.prop") or os.path.exists("/data/local")

def check_unprivileged_execution() -> CheckResult:
    """
    Checks if Antainer was executed as an unprivileged user, not directly as root/sudo.
    Returns available=True if running unprivileged, and available=False if running as root
    or if the execution identity cannot be safely determined.
    """
    is_root_user: bool | None = None

    # Primary POSIX effective UID check
    if hasattr(os, "geteuid"):
        is_root_user = (os.geteuid() == 0)
    # Secondary fallback to real UID
    elif hasattr(os, "getuid"):
        is_root_user = (os.getuid() == 0)
    
    # Indeterminate state guard
    if is_root_user is None:
        user_env = os.environ.get("USER", "") or os.environ.get("LOGNAME", "")
        if user_env == "root":
            is_root_user = True
        else:
            return CheckResult(
                available=False,
                message=(
                    "Unable to verify process privilege level on this platform.\n"
                    "Antainer requires a POSIX user environment to ensure safe execution."
                ),
            )
    
    if is_root_user:
        return CheckResult(
            available=False,
            message=(
                "Antainer was launched directly as root/sudo.\n"
                "For system safety, Antainer must be run as an unprivileged user.\n"
                "It will request root privileges via 'su' internally when needed."
            ),
        )
    
    return CheckResult(
        available=True,
        message="Running as an unprivileged user.",
    )

def check_chroot_availability() -> CheckResult:
    """
    Check if root access (via su) and the chroot binary are available on the device.
    Does not enforce that the current Python script itself is run as root.
    """
    # 1. Verify 'su' executable exists in PATH
    if shutil.which("su") is None:
        return CheckResult(
            available=False,
            message=(
                "Root privilege utility ('su') was not found on this device.\n"
                "Antainer currently relies on chroot and requires a rooted Android device.\n"
                "Non-rooted support via PRoot is planned for future updates."
            ),
        )

    # 2. Test if 'su' can actually grant execution access
    try:
        res = subprocess.run(
            ["su", "-c", "id -u"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if res.returncode != 0 or res.stdout.strip() != "0":
            return CheckResult(
                available=False,
                message=(
                    "Found 'su', but root access was denied or failed to respond.\n"
                    "Please ensure root permissions are granted to your shell/terminal emulator.\n"
                    "Non-rooted support via PRoot will be available in future updates."
                ),
            )
    except (subprocess.SubprocessError, OSError):
        return CheckResult(
            available=False,
            message=(
                "Failed to execute 'su' to verify root privileges.\n"
                "Non-rooted support via PRoot will be available in future updates."
            ),
        )

    # 3. Check for 'chroot' binary availability via su
    try:
        chroot_check = subprocess.run(
            ["su", "-c", "which chroot"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if chroot_check.returncode != 0 or not chroot_check.stdout.strip():
            return CheckResult(
                available=False,
                message=(
                    "Root access is present, but the 'chroot' binary could not be located in PATH.\n"
                    "Ensure BusyBox or equivalent userland utilities are installed."
                ),
            )
    except (subprocess.SubprocessError, OSError):
        return CheckResult(
            available=False,
            message="Error while checking for 'chroot' binary via su.",
        )

    return CheckResult(
        available=True,
        message="Root and chroot environments are available.",
    )
