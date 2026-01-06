# WebSocket ↔ Minitel GUI

(This is just an English translation of the program. I will not respond to any technical questions)

Python graphical interface that allows you to connect a **Minitel (or emulator)** via a **serial port** to a **WebSocket server** (MiniPAVI, BBS, etc.).

The application provides two-way communication:
- WebSocket → Minitel
- Minitel → WebSocket

It is compatible with **Windows, Linux and macOS**.

---

## Demonstration

Screenshot - (https://github.com/labbej27/websocket-minitel/raw/master/Capture%20d%E2%80%99e%CC%81cran%202025-12-11%20a%CC%80%2023.17.08.png)

## Features

- Simple Tkinter graphical interface
- Automatic serial port detection
- Comprehensive settings:
  - Baud rate
  - Parity
  - Data bits
  - Stop bits
- List of predefined WebSocket servers
- Supports `ws://` and `wss://`
- Real-time logging
- Asynchronous handling (WebSocket + Serial)

## Prerequisites

- **Python 3.14** (or 3.10 or later recommended)
- A real Minitel terminal or a serial emulator
- Access to a Minitel WebSocket server

---

## Installation

### 1. Clone the project

```bash
git clone https://github.com/shadowbreeze7881/websocket-minitel.git
cd websocket-minitel
```
### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
```

### 3. Activate the environment

- Windows (using Cygwin or any other unix-like environment program under Windows)
```bash
venv\Scripts\activate
```

- Linux / macOS
```bash
source venv/bin/activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch the program

```bash
python websocket_minitel.py
```

A graphical window opens, allowing you to configure and initiate the connection.

---

## Compiling an executable file
The compilation process produces a standalone binary (no Python required), using PyInstaller.

### To install pyinstall, pip is needed :

```bash
pip install pyinstaller
```

### Compiling under Windows

```bash
pyinstaller ^
  --onefile ^
  --windowed ^
  --name websocket-minitel ^
  websocket_minitel.py
```

#### Result: 
```bash
dist/websocket-minitel.exe
```

### Compiling under Linux
```bash
pyinstaller \
  --onefile \
  --windowed \
  --name websocket-minitel \
  websocket_minitel.py
```

#### Result :

dist/websocket-minitel
  
### Note :
A Windows .exe file must be compiled on Windows, and the same applies to Linux/macOS.

## Compiling under macOS

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name websocket-minitel \
  websocket_minitel.py
```

### Result :

dist/websocket-minitel.app

### Serial Port – Permissions
#### Linux
Add the user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

Then restart the session.

### macOS
Allow access to the serial port in:

-Settings → Security and Privacy → Privacy → Full Disk Access

#### Note macOS (SSL) :
The script uses an unverified SSL context to avoid certain certificate issues (wss://) on macOS.

###  Integrated WebSocket servers
- MiniPAVI (officiel)

- Hacker

- Annuaire

- 3615

- Retrocampus

- LABBEJ27

- Saisie manuelle

### Troubleshooting
- Verify the selected serial port.

- Check the baud rate (often 1200 baud for Minitel).

- Test without SSL (ws://) if possible.

- Run from a terminal to see any error messages.

## Licence
This project is free to use, modify, and redistribute
for non-commercial purposes.

Any commercial use is prohibited without the explicit permission
of the author.

This project was developed for personal and educational purposes,
inspired by existing projects from the Minitel community.

## Crédits / Sources

This project is based on and inspired by the following works:

- **websocket2minitel** par @cquest  
  https://github.com/cquest/websocket2minitel
  
---
