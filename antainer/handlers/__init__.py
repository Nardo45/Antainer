"""Package initialization and dispatch mapping for command handlers."""

from antainer.handlers.commands import (
    handle_pull,
    handle_enter,
    handle_create,
    handle_build,
)

COMMAND_HANDLERS = {
    "pull": handle_pull,
    "enter": handle_enter,
    "create": handle_create,
    "build": handle_build,
}

__all__ = ["COMMAND_HANDLERS"]
