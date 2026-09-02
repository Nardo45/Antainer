# Antainer

Antainer is a lightweight solution designed to execute standard Containerfile and Dockerfile container environments natively on Android using chroot, with potential proot support planned for future iterations.

The primary goal of this project is to enable local software development directly on Android devices without relying on virtual machines or remote development servers.

> **Note:** This project is in early active development. API, CLI, and internal structures are subject to change.

---

## Features and Goals

* **Root-First Execution:** Leverages `chroot` for zero-overhead, near-native performance and direct hardware/kernel access on rooted Android devices.
* **Standard Container Target:** Engineered around `Dockerfile` and `Containerfile` workflows.
* **On-Device Toolchains:** Enables compiling, building, and running developer environments directly on Android hardware.
* **Optional `proot` Support:** Future support for `proot` is under consideration to explore non-rooted sandboxing and learning opportunities.

---

## Prerequisites

* **Rooted Android Device:** Root access via Magisk, KernelSU, APatch, or equivalent.
* **Environment Utilities:** A working installation of `busybox` or modern Android userland utilities containing `chroot`.
* **Storage:** Sufficient space on internal storage (`/data/local/tmp` or similar) to store target rootfs layouts.

---

## Project Structure and Concept

Antainer bootstraps a minimal target Linux rootfs (e.g., Alpine, Debian, Arch) onto Android's filesystem, configures essential pseudo-filesystems, and enters the chroot environment:

1. Target environment directory allocation.
2. Mounting core filesystems (`/proc`, `/sys`, `/dev`, `/dev/pts`).
3. Execution of the `chroot` command targeting the isolated environment.
4. Clean teardown and unmounting upon exit.

---

## Roadmap

- [ ] Core rootfs bootstrapping and directory layout scripts
- [ ] Mount lifecycle management (mount/unmount hooks for `/proc`, `/sys`, `/dev`)
- [ ] Container image/rootfs pull and unpack automation
- [ ] User and permission mapping within the chroot environment
- [ ] Dockerfile/Containerfile directive parsing or compatibility execution
- [ ] Experimental `proot` backend exploration

---

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for details.
