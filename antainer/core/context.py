import os
from dataclasses import dataclass
from typing import Optional
from antainer.core.checker import (
    check_chroot_availability,
    check_unprivileged_execution,
    is_android_environment,
)
from antainer.storage import resolve_storage_base

@dataclass
class RuntimeContext:
    is_android: bool
    is_root_available: bool
    images_dir: str
    containers_dir: str

# Global in-memory instance
_CONTEXT: Optional[RuntimeContext] = None

def init_context() -> RuntimeContext:
    """
    Initializes system checks and populates global runtime context in memory.
    Must be called during main.py startup.
    """
    global _CONTEXT

    # 1. Assert unprivileged execution
    unprivileged_check = check_unprivileged_execution()
    if not unprivileged_check.available:
        raise RuntimeError(unprivileged_check.message)
    
    # 2. Assert root/chroot environment availability
    chroot_check = check_chroot_availability()
    is_root = chroot_check.available
    if not is_root:
        raise RuntimeError(chroot_check.message)
    
    # 3. Resolve environment flags and storage paths
    is_android = is_android_environment()
    images_path = resolve_storage_base(
        is_android=is_android,
        is_root_available=is_root,
        subfolder="images",
    )
    containers_path = resolve_storage_base(
        is_android=is_android,
        is_root_available=is_root,
        subfolder="containers",
    )

    _CONTEXT = RuntimeContext(
        is_android=is_android,
        is_root_available=is_root,
        images_dir=images_path,
        containers_dir=containers_path,
    )
    return _CONTEXT

def get_context() -> RuntimeContext:
    """Retrieves the cached runtime context from memory."""
    global _CONTEXT
    if _CONTEXT is None:
        return init_context()
    return _CONTEXT
