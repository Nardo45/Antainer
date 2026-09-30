import os
from antainer.core import get_context
from antainer.storage import mount_pseudo_filesystems
from antainer.core import run_command

def resolve_target_rootfs(target: str) -> str:
    """
    Resolves target into an absolute rootfs directory path.
    Checks direct filesystem path and Container directory (<ctx.containers_dir>/<target>)
    """
    ctx = get_context()

    # Direct path check
    if os.path.exists(target):
        sub_rootfs = os.path.join(target, "rootfs")
        if os.path.exists(sub_rootfs):
            return os.path.abspath(sub_rootfs)
        return os.path.abspah(target)

    # Check containers directory
    container_dir = os.path.join(ctx.containers_dir, target)
    if os.path.exists(container_dir):
        container_rootfs = os.path.join(container_dir, "rootfs")
        if os.path.exists(container_rootfs):
            return container_rootfs
        return container_dir

    print(container_dir)

    raise FileNotFoundError(
        f"Target '{target}' not found. Specified target must be an existing container name "
        f"or directory path."
    )

def enter_environment(target: str, shell: str = "bin/sh") -> None:
    """
    Mounts pseudo-filesystems and spawns an interactive chroot shell in target environment.
    """
    ctx = get_context()
    rootfs_path = resolve_target_rootfs(target)
    """
    Performing a chroot on Android or GNU/Linux always needs root.
    This will change once proot is implemented.
    """
    needs_root = True

    # Sanity check for shell presence inside target rootfs
    shell_rel_path = shell.lstrip("/")
    shell_check_path = os.path.join(rootfs_path, shell_rel_path)
    if not (os.path.exists(shell_check_path) or os.path.islink(shell_check_path)):
        print(f"[Antainer] Warning: Shell executable '{shell}' not found at '{shell_check_path}' inside rootfs.")

    print(f"[Antainer] Entering '{target}' ({rootfs_path}) using shell '{shell}'...")

    with mount_pseudo_filesystems(rootfs_path, is_android=ctx.is_android, requires_root=needs_root):
        # Setup environment variables inside chroot
        env_cmd = (
            "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; "
            "export HOME=/root; "
            "export TERM=xterm-256color; "
            f"exec {shell}"
        )
        chroot_cmd = f"chroot '{rootfs_path}' /bin/sh -c '{env_cmd}'"

        run_command(
            chroot_cmd,
            is_android=ctx.is_android,
            requires_root=needs_root,
            interactive=True,
        )
    print(f"\n[Antainer] Exited environment: {target}")
