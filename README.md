# WebSocket ↔ Minitel GUI

Interface graphique Python permettant de connecter un **Minitel (ou émulateur)** via un **port série** à un **serveur WebSocket** (MiniPAVI, BBS, etc.).

L’application assure une communication bidirectionnelle :
- WebSocket → Minitel
- Minitel → WebSocket

Elle est compatible **Windows, Linux et macOS**.

---

## Fonctionnalités

- Interface graphique Tkinter simple
- Détection automatique des ports série
- Paramétrage complet :
  - Vitesse (baudrate)
  - Parité
  - Bits de données
  - Bits de stop
- Liste de serveurs WebSocket prédéfinis
- Support `ws://` et `wss://`
- Journalisation en temps réel
- Gestion asynchrone (WebSocket + Série)

---

## Prérequis

- **Python 3.14** (ou ≥ 3.10 recommandé)
- Un Minitel réel ou un émulateur série
- Accès à un serveur WebSocket Minitel

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/labbej27websocket-minitel.git
cd websocket-minitel
```
- Créer un environnement virtuel (recommandé)
```bash
python3.14 -m venv venv
```
### 2. Activation :

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```
### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```
### 5. Lancement du programme
```bash
python websocket_minitel.py
pip install -r requirements.txt
```

Une fenêtre graphique s’ouvre permettant de configurer et lancer la connexion.

## Compilation en exécutable
La compilation permet d’obtenir un binaire autonome (sans Python requis).

Outil utilisé
PyInstaller

### Installation :


```bash
pip install pyinstaller
```

### Compilation Windows
```bash
pyinstaller ^
  --onefile ^
  --windowed ^
  --name websocket-minitel ^
  websocket_minitel.py
  ```
  ### Résultat :

- dist/websocket-minitel.exe
### Compilation Linux
```bash
pyinstaller \
  --onefile \
  --windowed \
  --name websocket-minitel \
  websocket_minitel.py
```

### Résultat :

- dist/websocket-minitel
- 
### L’exécutable est spécifique à l’OS :

- Un .exe Windows doit être compilé sous Windows, idem pour Linux/macOS.

## Compilation macOS

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name websocket-minitel \
  websocket_minitel.py
```
### Résultat :

- dist/websocket-minitel.app
#### Note macOS (SSL) :
- Le script utilise un contexte SSL non vérifié pour éviter certains problèmes de certificats (wss://) sur macOS.

#### Ports série – Permissions
- Linux
Ajouter l’utilisateur au groupe dialout :

```bash
sudo usermod -a -G dialout $USER
```

Puis redémarrer la session.

#### macOS
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

#### Licence
Projet libre – utilisation et modification autorisées.
---
