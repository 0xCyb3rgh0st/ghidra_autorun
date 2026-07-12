# ⚡ ghidra-open

<p align="center">

<img src="assets/banner.png" alt="ghidra-open Banner" width="100%">

</p>

<p align="center">
<b>One command. One binary. Instant reverse engineering.</b><br>
A lightweight launcher that automates Ghidra project creation, headless analysis, and GUI startup.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Supported-success?style=for-the-badge\&logo=linux)
![macOS](https://img.shields.io/badge/macOS-Supported-black?style=for-the-badge\&logo=apple)
![Windows](https://img.shields.io/badge/Windows-Supported-0078D6?style=for-the-badge\&logo=windows)
![License](https://img.shields.io/github/license/0xCyb3rgh0st/ghidra-open?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/0xCyb3rgh0st/ghidra-open?style=for-the-badge)

</p>

---

## 🚀 Overview

**ghidra-open** is a zero-configuration launcher for **Ghidra** that eliminates repetitive setup and fixes common project creation failures.

Instead of manually creating projects, importing binaries, and running analysis every time, simply point `ghidra-open` at your target.

```text
Target Binary
      │
      ▼
Filename Sanitization
      │
      ▼
Create Project
      │
      ▼
Run Headless Analyzer
      │
      ▼
Launch Ghidra GUI
```

---

## ✨ Features

* ⚡ One-command workflow
* 🔍 Automatic headless analysis
* 🛡️ Safe filename sanitization
* 📂 Existing project detection
* 🔄 Optional overwrite mode
* 💾 Temporary project support
* 🖥 Cross-platform
* 🔎 Automatic Ghidra detection
* 🚫 Prevents launching GUI after failed analysis
* 🪶 Lightweight with minimal dependencies

---

# 📸 Demo

> Replace this section with a GIF.

```text
$ ghidra ./a.out

[+] Detecting Ghidra...
[✓] Ghidra 12.1.2 found

[+] Creating Project
[✓] a_out.gpr

[+] Running Headless Analysis
██████████████████████████ 100%

[✓] Analysis Complete

Launching Ghidra...
```

---

# ❓ Why does this exist?

Ghidra cannot create projects whose names contain characters such as:

```text
.
/
\
:
```

Example:

```text
a.out
```

becomes

```text
a_out
```

Without sanitization, the headless analyzer aborts before creating the project.

`ghidra-open` fixes this automatically so analysis always succeeds.

---

# 📦 Requirements

| Requirement | Version            |
| ----------- | ------------------ |
| Python      | 3.8+               |
| click       | Latest             |
| Ghidra      | 10.x / 11.x / 12.x |

Install dependency:

```bash
pip install click
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/0xCyb3rgh0st/ghidra-open

cd ghidra-open
```

Install dependency

```bash
pip install click
```

Linux/macOS

```bash
chmod +x ghidra-open.py
```

---

## Configure Ghidra

Linux/macOS

```bash
export GHIDRA_INSTALL_DIR="$HOME/ghidra_12.1.2_PUBLIC"
```

Windows

```powershell
setx GHIDRA_INSTALL_DIR "C:\Tools\ghidra_12.1.2_PUBLIC"
```

---

## Create Command

Linux

```bash
sudo ln -s "$(pwd)/ghidra-open.py" /usr/local/bin/ghidra
```

or

```bash
alias ghidra='python3 ~/bin/ghidra-open.py'
```

Reload shell

```bash
source ~/.bashrc
```

---

# 🚀 Usage

Analyze Binary

```bash
ghidra ./a.out
```

Open Existing Project

```bash
ghidra ./project.gpr
```

Open Project Directory

```bash
ghidra ./projects/
```

---

# 📖 Command Examples

| Command                       | Description           |
| ----------------------------- | --------------------- |
| `ghidra ./binary`             | Analyze binary        |
| `ghidra ./project.gpr`        | Open project          |
| `ghidra ./folder`             | Open directory        |
| `ghidra --temp ./binary`      | Store project in temp |
| `ghidra --overwrite ./binary` | Force re-analysis     |

---

# 🧰 CLI Options

| Option             | Description                                |
| ------------------ | ------------------------------------------ |
| `-t` `--temp`      | Store project inside system temp directory |
| `-o` `--overwrite` | Overwrite existing project                 |
| `-y` `--yes`       | Skip confirmation delay                    |
| `-h` `--help`      | Show help                                  |

---

# 🏗 Workflow

```text
              Binary
                 │
                 ▼
      Sanitize Project Name
                 │
                 ▼
      Create Ghidra Project
                 │
                 ▼
      Headless Analysis
                 │
                 ▼
      Analysis Successful?
          │           │
          │           │
         Yes          No
          │           │
          ▼           ▼
 Launch GUI      Exit Safely
```

---

# 📁 Project Structure

```text
ghidra-open/

├── ghidra-open.py
├── README.md
├── LICENSE
├── assets/
│   ├── banner.png
│   ├── demo.gif
│   ├── screenshot.png
│   └── logo.svg
└── examples/
```

---

# 🛣 Roadmap

* ✅ Cross-platform support
* ✅ Automatic project creation
* ✅ Filename sanitization
* ✅ Existing project detection
* ✅ Headless analysis
* ⏳ Batch imports
* ⏳ Plugin installer
* ⏳ Theme manager
* ⏳ Project cache
* ⏳ TUI interface
* ⏳ Interactive launcher

---

# 🤝 Contributing

Contributions are always welcome.

If you discover bugs or have feature ideas, feel free to open an issue or submit a pull request.

---

# 📜 License

This project is licensed under the MIT License.

---

<p align="center">

### Built for Reverse Engineers ⚡

*"Spend time reversing binaries, not creating projects."*

Made with ❤️ by **0xCyb3rgh0st**

</p>
