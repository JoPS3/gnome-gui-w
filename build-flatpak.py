#!/usr/bin/env python3

import shutil
import subprocess
import tempfile
from pathlib import Path


APP_ID = "com.jfscorreia.usersList"
RUNTIME = "org.gnome.Platform"
RUNTIME_VERSION = "50"
FLATHUB = "https://dl.flathub.org/repo/flathub.flatpakrepo"
PROJECT_DIR = Path(__file__).resolve().parent


def run(*args):
    subprocess.run(args, check=True)


def main():
    with tempfile.TemporaryDirectory(prefix="gnome-w-flatpak-") as temp_dir:
        temp_path = Path(temp_dir)
        build_dir = temp_path / "build"
        repo_dir = temp_path / "repo"

        # This application only installs files, so it does not need the SDK.
        run("flatpak", "build-init", str(build_dir), APP_ID, RUNTIME, RUNTIME, RUNTIME_VERSION)

        binary = build_dir / "files" / "bin" / "gnome-w-viewer"
        binary.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_DIR / "main.py", binary)
        binary.chmod(0o755)

        applications = build_dir / "files" / "share" / "applications"
        applications.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_DIR / f"{APP_ID}.desktop", applications / f"{APP_ID}.desktop")

        icons = build_dir / "files" / "share" / "icons" / "hicolor" / "scalable" / "apps"
        icons.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_DIR / f"{APP_ID}.svg", icons / f"{APP_ID}.svg")

        run(
            "flatpak", "build-finish",
            "--command=gnome-w-viewer",
            "--share=ipc",
            "--socket=wayland",
            "--socket=fallback-x11",
            "--system-talk-name=org.freedesktop.login1",
            str(build_dir),
        )
        run("flatpak", "build-export", str(repo_dir), str(build_dir), "stable")
        bundle = PROJECT_DIR / f"{APP_ID}.flatpak"
        run(
            "flatpak", "build-bundle",
            f"--runtime-repo={FLATHUB}",
            str(repo_dir), str(bundle), APP_ID, "stable",
        )
        print(f"Pacote criado: {bundle}")


if __name__ == "__main__":
    main()
