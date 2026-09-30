# Antainer

Antainer is a lightweight container runtime designed to pull OCI images, manage isolated container instances, and execute containerized environments directly on Android devices using `chroot`.

The primary objective of Antainer is to provide an efficient local container workflow on Android without requiring heavy virtual machines or remote development instances.

---

## Key Capabilities

- **OCI Registry Integration:** Direct pulling and extraction of multi-architecture OCI images (e.g., Docker Hub, GHCR).
- **Zero-Overhead Execution:** Leverages `chroot` and kernel namespaces for native speed and direct system resource access.
- **Automated Storage Management:** Manages storage roots, configuration tracking, and container directory trees transparently.
- **Android Privilege Escalation:** Unified command execution interface that handles root (`su`) elevation when accessing restricted paths such as `/data/local`.
- **Mount Lifecycle Safety:** Automatically mounts and lazy-unmounts essential pseudo-filesystems (`/proc`, `/sys`, `/dev`, `/dev/pts`) during interactive sessions.

---

## Prerequisites

- **Android System:** Android device rooted via Magisk, KernelSU, APatch, or equivalent.
- **Userland Tools:** Termux or similar terminal emulator equipped with `python3` (3.10+), `tar`, and `su`.
- **Storage:** Read/write access to internal storage paths (such as `/data/local/.antainer`).

---

## Architecture Overview

Antainer abstracts container operation through a structured module hierarchy:

1. **Core (`antainer.core`):** Provides central context model and process execution capabilities, managing privileged Android execution, interactive shells, and command output handling.
2. **Registry (`antainer.registry`):** Fetches OCI image manifests, resolves target architectures (ARM64, x86_64, etc.), downloads blob layers, and extracts them to local storage.
3. **Runtime (`antainer.runtime`):** Instantiates runnable container instances, manages metadata configurations, handles target environment entry, and manages pseudo-filesystem mounts.
4. **Storage (`antainer.storage`):** Centralizes cross-platform filesystem operations, storage directory creation, directory copying, layer extraction, and rootfs management.
5. **Handlers (`antainer.handlers`):** Command-line dispatchers mapping user inputs to runtime workflows.

---

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for details.
