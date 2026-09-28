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
from antainer.core.exec import (
    run_command,
)

__all__ = [
    "CheckResult",
    "check_chroot_availability",
    "check_unprivileged_execution",
    "is_android_environment",
    "get_context",
    "init_context",
    "run_command",
]
