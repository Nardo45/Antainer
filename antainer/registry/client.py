import json
import os
import platform
import urllib.request
from typing import Tuple
from antainer.core import get_context
from antainer.storage import ensure_dir, extract_layer, get_staging_dir


def parse_image_ref(image_ref: str) -> Tuple[str, str, str]:
    """
    Parse an image reference string like 'alpine', 'ubuntu:22.04', or
    'ghcr.io/owner/repo:tag' into (registry, repository, tag).
    """
    if "/" not in image_ref:
        registry = "registry-1.docker.io"
        repository = f"library/{image_ref}"
    elif image_ref.count("/") == 1 and "." not in image_ref.split("/")[0]:
        registry = "registry-1.docker.io"
        repository = image_ref
    else:
        parts = image_ref.split("/", 1)
        registry = parts[0]
        repository = parts[1]

    if ":" in repository:
        repository, tag = repository.split(":", 1)
    else:
        tag = "latest"

    return registry, repository, tag


def get_bearer_token(registry: str, repository: str) -> str:
    """Acquire an anonymous OCI bearer token for reading images."""
    if registry == "registry-1.docker.io":
        auth_url = (
            f"https://auth.docker.io/token?"
            f"service=registry.docker.io&scope=repository:{repository}:pull"
        )
        req = urllib.request.Request(auth_url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("token", "")
    return ""


def resolve_architecture() -> str:
    """Map system machine architecture to OCI specification names."""
    arch = platform.machine().lower()
    if arch in ("aarch64", "arm64"):
        return "arm64"
    if arch in ("x86_64", "amd64"):
        return "amd64"
    if arch.startswith("arm"):
        return "arm"
    return "arm64"  # Default fallback for Android devices


def pull_and_extract_oci_image(image_ref: str, custom_name: str | None = None) -> str:
    """
    Download OCI image layers and extract them into the resolved rootfs directory.
    Supports multi-architecture OCI indexes and Docker manifest lists.
    """
    ctx = get_context()
    registry, repository, tag = parse_image_ref(image_ref)
    target_name = custom_name if custom_name else repository.split("/")[-1]

    output_dir = os.path.join(ctx.images_dir, target_name)
    staging_dir = get_staging_dir()

    # Flag if destination path requires elevated permissions on Android
    needs_root = output_dir.startswith("/data/local")
    ensure_dir(output_dir, is_android=ctx.is_android, requires_root=needs_root)

    print(f"[Antainer] Connecting to registry: {registry}")
    token = get_bearer_token(registry, repository)
    headers = {
        "Accept": (
            "application/vnd.docker.distribution.manifest.v2+json, "
            "application/vnd.oci.image.manifest.v1+json, "
            "application/vnd.docker.distribution.manifest.list.v2+json, "
            "application/vnd.oci.image.index.v1+json"
        ),
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # 1. Fetch Manifest or Index
    manifest_url = f"https://{registry}/v2/{repository}/manifests/{tag}"
    req = urllib.request.Request(manifest_url, headers=headers)

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    # Resolve manifest if response is a Multi-Arch Index/List
    media_type = data.get("mediaType", "")
    if "list" in media_type or "index" in media_type or "manifests" in data:
        target_arch = resolve_architecture()
        matching_digest = None

        for manifest_item in data.get("manifests", []):
            platform_info = manifest_item.get("platform", {})
            if platform_info.get("architecture") == target_arch:
                matching_digest = manifest_item.get("digest")
                break

        if not matching_digest and data.get("manifests"):
            # Fallback to first available manifest if exact arch isn't matched
            matching_digest = data["manifests"][0]["digest"]

        if not matching_digest:
            raise ValueError(f"Could not resolve manifest for architecture: {target_arch}")

        # Fetch platform-specific child manifest
        child_url = f"https://{registry}/v2/{repository}/manifests/{matching_digest}"
        child_req = urllib.request.Request(child_url, headers=headers)
        with urllib.request.urlopen(child_req) as resp:
            data = json.loads(resp.read().decode("utf-8"))

    layers = data.get("layers", [])
    if not layers:
        raise ValueError("No layers found in image manifest.")

    print(f"[Antainer] Fetching {len(layers)} OCI layer(s)...")

    # 2. Download to unprivileged staging and unpack sequentially into rootfs
    for idx, layer in enumerate(layers, start=1):
        digest = layer["digest"]
        print(f"[Antainer] Layer {idx}/{len(layers)}: Unpacking {digest[:12]}...")

        blob_url = f"https://{registry}/v2/{repository}/blobs/{digest}"
        blob_req = urllib.request.Request(blob_url, headers=headers)

        staging_tar_path = os.path.join(staging_dir, f"layer_{idx}.tar.gz")
        with urllib.request.urlopen(blob_req) as response, open(staging_tar_path, "wb") as out_file:
            out_file.write(response.read())

        extract_layer(staging_tar_path, output_dir, is_android=ctx.is_android, requires_root=needs_root)

        if os.path.exists(staging_tar_path):
            os.remove(staging_tar_path)

    print(f"[Antainer] Successfully populated rootfs at: {output_dir}")
    return output_dir
