# Antainer Usage Documentation

Antainer provides a Command Line Interface (CLI) to pull OCI images, manage local container instances, and launch interactive `chroot` shell environments.

---

## Global CLI Invocation

Antainer can be executed as a Python module:

```bash
python -m antainer.main [COMMAND] [OPTIONS]

```

---

## Commands and Options

### 1. `pull`

Downloads an OCI image from a registry, resolves architecture, extracts layers, and registers it in the local image store.

**Syntax:**

```bash
python -m antainer.main pull <image> [--name <custom_name>]

```

**Arguments and Options:**

* `<image>` *(Required)*: The OCI image reference (e.g., `alpine`, `ubuntu:22.04`, `library/alpine:latest`).
* `-n, --name <custom_name>` *(Optional)*: Custom name override for the stored local image directory.

**Examples:**

```bash
# Pull Alpine Linux (stored as 'alpine')
python -m antainer.main pull alpine

# Pull Ubuntu with a custom target name
python -m antainer.main pull ubuntu:22.04 --name ubuntu-base

```

---

### 2. `create`

Instantiates a new container rootfs from a pulled local image and writes a `config.json` manifest.

**Syntax:**

```bash
python -m antainer.main create <image> [--name <container_name>]

```

**Arguments and Options:**

* `<image>` *(Required)*: Name of the existing local image to instantiate from.
* `-n, --name <container_name>` *(Optional)*: Custom name for the created container. Defaults to the base image name if omitted.

**Examples:**

```bash
# Create a container named 'alpine' from local image 'alpine'
python -m antainer.main create alpine

# Create a container with a custom name 'dev-env'
python -m antainer.main create alpine --name dev-env

```

---

### 3. `enter`

Mounts required pseudo-filesystems (`/proc`, `/sys`, `/dev`, `/dev/pts`) into the specified rootfs, elevates privileges to root, and launches an interactive `chroot` shell. Upon exit, all mounts are automatically unmounted.

**Syntax:**

```bash
python -m antainer.main enter <target> [--shell <path_to_shell>]

```

**Arguments and Options:**

* `<target>` *(Required)*: Container name, local image name, or explicit filesystem path to a rootfs.
* `-s, --shell <path_to_shell>` *(Optional)*: Shell executable to run inside the chroot environment. Default is `/bin/sh`.

**Target Resolution Order:**

1. Direct filesystem directory path.
2. Container matching `<ctx.containers_dir>/<target>`.

**Examples:**

```bash
# Enter container 'dev-env' with default shell (/bin/sh)
python -m antainer.main enter dev-env

# Enter container 'dev-env' using bash
python -m antainer.main enter dev-env --shell /bin/bash

# Enter a direct rootfs path
python -m antainer.main enter /data/local/my_rootfs

```

---
### 5. `build`
> [!IMPORTANT]
> This has not yet been implemented

Builds an image from a Containerfile or Dockerfile.

**Syntax:**

```bash
python -m antainer.main build -t <tag> [-f <file>]

```

**Arguments and Options:**

* `-t, --tag <tag>` *(Required)*: Name and tag for the resulting image.
* `-f, --file <file>` *(Optional)*: Path to the build file. Default is `Dockerfile`.

---

## Directory & Storage Layout

Default storage locations on Android systems (`/data/local/.antainer`):

```
/data/local/.antainer/
├── images/
│   └── alpine/
│       ├── bin/
│       ├── etc/
│       └── ... (rootfs contents)
└── containers/
    └── dev-env/
        ├── config.json
        └── rootfs/
            ├── proc/
            ├── sys/
            ├── dev/
            └── ...

```

---

## Technical Details: Android Root Operations

Operations modifying or entering environments located under protected paths (e.g., `/data/local/`) utilize `antainer.core.exec.run_command`:

* **Unprivileged Mode:** Direct Python standard library operations or native `/bin/sh` subprocess calls.
* **Privileged Mode (Android Root):** Command execution wrapped via `su -c` to maintain full POSIX ownership, device node capabilities, and permissions.
