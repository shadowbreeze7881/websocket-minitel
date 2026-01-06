# WebSocket ↔ Minitel GUI

(This is just an English translation of the program. I will not respond to any technical questions)

Python graphical interface that allows you to connect a **Minitel (or emulator)** via a **serial port** to a **WebSocket server** (MiniPAVI, BBS, etc.).

The application provides two-way communication:
- WebSocket → Minitel
- Minitel → WebSocket

It is compatible with **Windows, Linux and macOS**.

## Demonstration

Screenshot - (https://github.com/labbej27/websocket-minitel/raw/master/Capture%20d%E2%80%99e%CC%81cran%202025-12-11%20a%CC%80%2023.17.08.png)

---

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

---

## Prerequisites

- **Python 3.14** (or 3.10 or later recommended)
- A real Minitel terminal or a serial emulator
- Access to a Minitel WebSocket server

---

The steps below were tested and performed in a bash shell environment.

## 1. Installation

- Clone the project
git clone https://github.com/labbej27websocket-minitel.git
cd websocket-minitel

- Create a virtual environment (recommended)
python3 -m venv venv

---

## 2. Activation

- Windows (using bash shell in Cygwin or any other Unix-like environment program)
venv\Scripts\activate

- Linux / macOS
source venv/bin/activate

---

### 3. Install the dependencies

pip install -r requirements.txt

---

### 4. Launch the program

python websocket_minitel.py
pip install -r requirements.txt

A graphical window opens, allowing you to configure and initiate the connection.

## Compiling an executable file
The compilation process produces a standalone binary (no Python required), using PyInstaller.

---

### Installation :

pip install pyinstaller

### Windows Compilation

pyinstaller ^
  --onefile ^
  --windowed ^
  --name websocket-minitel ^
  websocket_minitel.py

### Result: 

dist/websocket-minitel.exe
### Compilation Linux
```bash
pyinstaller \
  --onefile \
  --windowed \
  --name websocket-minitel \
  websocket_minitel.py
```

### Résultat :

dist/websocket-minitel
  
### L’exécutable est spécifique à l’OS :

Un .exe Windows doit être compilé sous Windows, idem pour Linux/macOS.

## Compilation macOS

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name websocket-minitel \
  websocket_minitel.py
```
### Résultat :

dist/websocket-minitel.app

### Ports série – Permissions
Linux
Ajouter l’utilisateur au groupe dialout :

```bash
sudo usermod -a -G dialout $USER
```

Puis redémarrer la session.
### Note macOS (SSL) :
Le script utilise un contexte SSL non vérifié pour éviter certains problèmes de certificats (wss://) sur macOS.

### macOS
Autoriser l’accès au port série dans :

-Réglages → Sécurité et confidentialité → Confidentialité → Accès complet au disque

###  Serveurs WebSocket intégrés
- MiniPAVI (officiel)

- Hacker

- Annuaire

- 3615

- Retrocampus

- LABBEJ27

- Saisie manuelle

### Dépannage
- Vérifier le port série sélectionné

- Vérifier la vitesse (souvent 1200 bauds pour Minitel)

- Tester sans SSL (ws://) si possible

- Lancer depuis un terminal pour voir les erreurs

## Licence

Ce projet est libre d'utilisation, de modification et de redistribution
à des fins non commerciales.

Toute utilisation commerciale est interdite sans autorisation explicite
de l'auteur.

Ce projet a été développé à des fins personnelles et éducatives,
en s’inspirant de projets existants de la communauté Minitel.

## Crédits / Sources

Ce projet s’appuie sur et s’inspire des travaux suivants :

- **websocket2minitel** par @cquest  
  https://github.com/cquest/websocket2minitel
  
---
