#!/usr/bin/env python3
"""
ghidra-open: import a binary with Ghidra's headless analyzer, then open it in
the GUI. Also opens .gpr projects, or just launches the bare GUI.

Cross-platform: Linux, macOS, and Windows. The only OS-specific bits are the
launcher name (.bat on Windows), how a .bat is invoked, the temp directory,
and the fallback search locations. Ghidra's project-name rules are the same
everywhere, so the sanitization below is universal.
"""

import os
import re
import sys
import time
import shutil
import platform
import tempfile
import subprocess
from pathlib import Path

import click

IS_WINDOWS = os.name == "nt"
LAUNCHER = "ghidraRun.bat" if IS_WINDOWS else "ghidraRun"
HEADLESS = "analyzeHeadless.bat" if IS_WINDOWS else "analyzeHeadless"


def run(cmd) -> subprocess.CompletedProcess:
    """subprocess.run that also works for Windows .bat launchers."""
    cmd = [str(c) for c in cmd]
    if IS_WINDOWS and cmd[0].lower().endswith(".bat"):
        cmd = ["cmd", "/c", *cmd]
    return subprocess.run(cmd)


def search_bases():
    home = Path.home()
    if IS_WINDOWS:
        pf = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        return [home, pf, Path(os.environ.get("SystemDrive", "C:") + os.sep)]
    bases = [home, Path("/opt"), Path("/usr/share"), Path("/usr/local")]
    if platform.system() == "Darwin":
        bases += [Path("/Applications"), Path("/opt/homebrew")]
    return bases


def find_ghidra() -> Path:
    """Locate the Ghidra install directory (the one containing the launcher)."""
    for var in ("GHIDRA_INSTALL_DIR", "GHIDRA_PATH", "GHIDRA_HOME"):
        val = os.environ.get(var)
        if val and (Path(val) / LAUNCHER).is_file():
            return Path(val)

    on_path = shutil.which(LAUNCHER) or shutil.which("ghidraRun")
    if on_path:
        return Path(on_path).resolve().parent

    for base in search_bases():
        if not base.is_dir():
            continue
        for match in sorted(base.glob("ghidra_*_PUBLIC"), reverse=True):
            if (match / LAUNCHER).is_file():
                return match

    raise click.ClickException(
        "Ghidra not found. Point the script at your install, e.g.:\n"
        "  Linux/macOS: export GHIDRA_INSTALL_DIR=/home/cyberghost/ghidra_12.1.2_PUBLIC\n"
        "  Windows:     set GHIDRA_INSTALL_DIR=C:\\Tools\\ghidra_12.1.2_PUBLIC"
    )


def sanitize_project_name(name: str) -> str:
    """Ghidra project names may not contain  . / \\ :  or control chars."""
    cleaned = re.sub(r"[^A-Za-z0-9_+\-]", "_", name).strip("_")
    return cleaned or "project"


def unique_name(project_dir: Path, base: str) -> str:
    name, n = base, 0
    while (project_dir / f"{name}.gpr").exists() or (project_dir / f"{name}.rep").exists():
        n += 1
        name = f"{base}_{n}"
    return name


def confirm_run(seconds: int = 2) -> bool:
    if not sys.stdin.isatty():
        return True
    click.secho(f"Analyzing in {seconds}s — press Ctrl-C to cancel", fg="green")
    try:
        for _ in range(seconds):
            time.sleep(1)
    except KeyboardInterrupt:
        click.secho("\nCancelled.", fg="yellow")
        return False
    return True


@click.command()
@click.argument("target", type=click.Path(exists=True))
@click.option("-t", "--temp", is_flag=True, help="Put the project in the system temp dir.")
@click.option("-o", "--overwrite", is_flag=True, help="Re-analyze even if the project already exists.")
@click.option("-y", "--yes", is_flag=True, help="Skip the confirmation delay.")
def main(target, temp, overwrite, yes):
    ghidra = find_ghidra()
    ghidra_run = ghidra / LAUNCHER
    analyze_headless = ghidra / "support" / HEADLESS

    target = Path(target)

    # 1. Directory -> just open the GUI.
    if target.is_dir():
        run([ghidra_run])
        return

    # 2. Existing project -> open it.
    if target.suffix == ".gpr":
        run([ghidra_run, target.resolve()])
        return

    # 3. Binary -> headless import + analysis, then open.
    project_dir = Path(tempfile.gettempdir()) if temp else target.resolve().parent
    project_dir.mkdir(parents=True, exist_ok=True)

    base_name = sanitize_project_name(target.name)   # a.out -> a_out
    gpr = project_dir / f"{base_name}.gpr"
    rep = project_dir / f"{base_name}.rep"

    if gpr.exists() and not overwrite:
        click.secho(f"Project exists, opening: {gpr}", fg="cyan")
        run([ghidra_run, gpr])
        return

    if overwrite:
        for p in (gpr, rep):
            if p.is_dir():
                shutil.rmtree(p)
            elif p.exists():
                p.unlink()
        project_name = base_name
    else:
        project_name = unique_name(project_dir, base_name)

    try:
        info = subprocess.run(
            ["file", str(target)], capture_output=True, text=True, check=True
        ).stdout.strip()
        click.secho(info, fg="yellow")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # `file` isn't on Windows; harmless to skip.

    if not (yes or confirm_run()):
        return

    result = run([analyze_headless, project_dir, project_name, "-import", target])
    if result.returncode != 0:
        raise click.ClickException(
            "Headless analysis failed — not opening the GUI. See the output above."
        )

    run([ghidra_run, project_dir / f"{project_name}.gpr"])


if __name__ == "__main__":
    main()
