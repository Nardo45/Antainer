"""Core system infrastructure, environment checks, and runtime state management for Antainer."""

from antainer.core.checker import (
    CheckResult,
    check_chroot_availability,
    check_unprivileged_execution,
    is_android_environment,
)
from antainer.core.context import (
    RuntimeContext,
    get_context,
    init_context,
)

__all__ = [
    "CheckResult",
    "check_chroot_availability",
    "check_unprivileged_execution",
    "is_android_environment",
    "get_context",
    "init_context",
]