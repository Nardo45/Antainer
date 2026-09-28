import json
import os
import time
from typing import Any, Dict
from antainer.core import get_context
from antainer.storage import copy_dir_tree, ensure_dir, write_json_file

def create_container(image_name: str, container_name: str | None = None) -> Dict[str, Any]:
    """
    Instantiates a runnable container directory from an existing local image base.
    """
    ctx = get_context()

    source_image_dir = os.path.join(ctx.images_dir, image_name)
    if not os.path.exists(source_image_dir):
        raise FileNotFoundError(
            f"Image '{image_name}' not found locally. Pull it first using 'antainer pull {image_name}'."
        )

    target_name = container_name if container_name else image_name
    container_dir = os.path.join(ctx.containers_dir, target_name)

    if os.path.exists(container_dir):
        raise FileExistsError(f"Container '{target_name}' already exists at {container_dir}.")

    ensure_dir(container_dir, is_android=ctx.is_android)

    target_rootfs = os.path.join(container_dir, "rootfs")
    copy_dir_tree(source_image_dir, target_rootfs, is_android=ctx.is_android)

    config: Dict[str, Any] = {
        "name": target_name,
        "image": image_name,
        "created_at": time.time(),
        "status": "created",
        "rootfs": target_rootfs,
    }

    config_path = os.path.join(container_dir, "config.json")
    write_json_file(config_path, config, is_android=ctx.is_android)

    return config
