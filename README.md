# ghidra-open

A small wrapper around Ghidra. Point it at a binary and it runs the headless
analyzer, then opens the result in the GUI. Point it at a `.gpr` (or a folder)
and it just opens Ghidra. Works on Linux, macOS, and Windows.

It exists to avoid the classic breakage where a binary named `a.out` becomes a
Ghidra project named `a.out` — Ghidra forbids `.` `/` `\` `:` in project names,
so the headless analyzer aborts and the project is never created. This script
sanitizes the name (`a.out` → `a_out`), auto-detects the Ghidra install, and
refuses to launch the GUI if analysis failed.

## Requirements

- Python 3.8+
- [`click`](https://pypi.org/project/click/) — `pip install click`
- A Ghidra install (the folder containing `ghidraRun` / `ghidraRun.bat`)

## Install

### 1. Grab the script and dependency

```bash
pip install --user click            # or: pipx install click
chmod +x ghidra-open.py             # Linux / macOS
```

### 2. Tell it where Ghidra lives

Set `GHIDRA_INSTALL_DIR` (the script also accepts `GHIDRA_PATH` / `GHIDRA_HOME`,
and can auto-detect, but the env var is the reliable path).

**Linux / macOS** — add to `~/.bashrc` or `~/.zshrc`:

```bash
export GHIDRA_INSTALL_DIR="$HOME/ghidra_12.1.2_PUBLIC"
```

**Windows (PowerShell, persistent):**

```powershell
setx GHIDRA_INSTALL_DIR "C:\Tools\ghidra_12.1.2_PUBLIC"
```

> On Windows, prefer a path without spaces (e.g. `C:\Tools\...` rather than
> `C:\Program Files\...`) so the `.bat` launcher invokes cleanly.

### 3. Make a `ghidra` command

Pick one. (`ghidra` is safe to use — Ghidra's real launcher is `ghidraRun`, so
nothing collides.)

**Option A — symlink into your PATH (system-wide command):**

```bash
sudo ln -s "$(pwd)/ghidra-open.py" /usr/local/bin/ghidra
```

**Option B — shell alias (per-user, no sudo):**

```bash
# ~/.bashrc or ~/.zshrc
alias ghidra='python3 ~/bin/ghidra-open.py'
```

Reload the shell afterward:

```bash
source ~/.bashrc     # or: source ~/.zshrc
```

## Usage

```bash
ghidra ./a.out            # headless-analyze, then open in the GUI
ghidra ./project.gpr      # open an existing project
ghidra ./somedir          # just launch the Ghidra GUI
```

### Options

| Flag              | Effect                                                         |
|-------------------|----------------------------------------------------------------|
| `-t`, `--temp`    | Put the project in the system temp dir instead of next to the binary |
| `-o`, `--overwrite` | Re-analyze even if a project of that name already exists     |
| `-y`, `--yes`     | Skip the 2-second confirmation delay                           |

If a project already exists it is reopened instead of re-analyzed, unless you
pass `--overwrite`.

## Notes

- The `file` command is used only to print a quick binary summary; it's absent
  on Windows and simply skipped there.
- On Windows, running inside WSL uses the clean Linux path if you'd rather avoid
  the native `.bat` handling.
