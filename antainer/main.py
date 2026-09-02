import sys
from antainer.backend import check_chroot_availability

def main() -> None:
    print("[Antainer] Initializing system checks...")

    result = check_chroot_availability()

    if result.available:
        print(f"[Antainer] Success: {result.message}")
    else:
        print(f"[Antainer] Error:\n{result.message}")
        sys.exit(1)

if __name__ == "__main__":
    main()