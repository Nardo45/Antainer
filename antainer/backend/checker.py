import shutil
import subprocess
from dataclasses import dataclass

@dataclass
class CheckResult:
    available: bool
    message: str

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
