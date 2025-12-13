import tkinter as tk
from tkinter import ttk, scrolledtext
import serial.tools.list_ports
import asyncio
import threading
import serial
import websockets
import time
import ssl

# SSL macOS workaround
ssl_context = ssl._create_unverified_context()

ser = None
ws = None
running = False

# ─────────────────────────────────────────────
# LOG
# ─────────────────────────────────────────────
def log(text, log_widget):
    timestamp = time.strftime("%H:%M:%S")
    log_widget.configure(state="normal")
    log_widget.insert(tk.END, f"[{timestamp}] {text}\n")
    log_widget.see(tk.END)
    log_widget.configure(state="disabled")


# ─────────────────────────────────────────────
# ASYNC TASK : WebSocket ↔ Minitel
# ─────────────────────────────────────────────
async def websocket_task(url, tty, speed, parity, databits, stopbits, status_label, log_widget):
    global ser, ws, running

    STOPBITS_MAP = {
        "1": serial.STOPBITS_ONE,
        "1.5": serial.STOPBITS_ONE_POINT_FIVE,
        "2": serial.STOPBITS_TWO
    }

    try:
        # Ouverture port série
        log(f"Ouverture du port série {tty} à {speed} bauds…", log_widget)
        ser = serial.Serial(
            tty,
            int(speed),
            parity=parity,
            bytesize=int(databits),
            stopbits=STOPBITS_MAP[stopbits],
            timeout=1
        )

        # Connexion WebSocket
        log(f"Connexion au WebSocket {url}…", log_widget)

        if url.startswith("wss://"):
            log("Utilisation d’un contexte SSL non vérifié (wss)…", log_widget)
            ws = await websockets.connect(url, ssl=ssl_context)
        else:
            ws = await websockets.connect(url)

        log("Connexion établie.", log_widget)
        status_label.config(text="Connecté")

        # Message test Minitel
        ser.write(b"\x07\x0c\x1f\x40\x41connexion\x0a")
        ser.write(b"\x1b\x3b\x60\x58\x52")

        # WebSocket → Minitel
        async def w2m():
            while running:
                try:
                    data = await ws.recv()
                    if isinstance(data, bytes):
                        ser.write(data)
                        log(f"[WS→Minitel] {len(data)} octets", log_widget)
                    else:
                        ser.write(data.encode("latin1", "replace"))
                        log(f"[WS→Minitel] {data}", log_widget)
                except:
                    break

        # Minitel → WebSocket
        async def m2w():
            while running:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    await ws.send(data.decode("latin1", "replace"))
                    log(f"[Minitel→WS] {data}", log_widget)
                else:
                    await asyncio.sleep(0.05)

        await asyncio.gather(w2m(), m2w())

    except Exception as e:
        log(f"Erreur : {e}", log_widget)
        status_label.config(text="Erreur")

    finally:
        running = False
        log("Déconnexion…", log_widget)
        try:
            if ws:
                await ws.close()
        except:
            pass
        try:
            if ser:
                ser.close()
        except:
            pass
        status_label.config(text="Déconnecté")
        log("Connexions fermées.", log_widget)


# ─────────────────────────────────────────────
# THREAD RUNNER
# ─────────────────────────────────────────────
def start_async(url, tty, speed, parity, databits, stopbits, status_label, log_widget):
    global running
    if running:
        return
    running = True

    loop = asyncio.new_event_loop()
    threading.Thread(
        target=loop.run_until_complete,
        args=(websocket_task(url, tty, speed, parity, databits, stopbits, status_label, log_widget),),
        daemon=True
    ).start()


def stop_connection(status_label, log_widget):
    global running
    running = False
    status_label.config(text="Déconnecté")
    log("Arrêt demandé.", log_widget)


# ─────────────────────────────────────────────
# Port detection refresh
# ─────────────────────────────────────────────
def update_ports(combo):
    current_ports = set(combo["values"])
    detected = {p.device for p in serial.tools.list_ports.comports()}

    if detected != current_ports:
        combo["values"] = list(detected)
        if detected:
            combo.set(list(detected)[0])


# ─────────────────────────────────────────────
# GUI
# ─────────────────────────────────────────────
def build_gui():
    root = tk.Tk()
    root.title("WebSocket ↔ Minitel")

    # LISTE DE SERVEURS
    SERVERS = {
        "MiniPAVI (officiel)": "wss://go.minipavi.fr:8181",
        "Hacker": "ws://mntl.joher.com:2018",
        "Annuaire": "ws://3611.re/ws",
        "3615": "ws://3615co.de/ws",
        "Retrocampus": "wss://bbs.retrocampus.com:8051",
        "LABBEJ27": "wss://minitel.labbej.fr:8182",
        "Saisie manuelle…": ""
    }

    tk.Label(root, text="Serveur prédéfini").grid(row=0, column=0)
    server_combo = ttk.Combobox(root, values=list(SERVERS.keys()), width=40)
    server_combo.set("MiniPAVI (officiel)")
    server_combo.grid(row=0, column=1)

    # Champ URL modifiable
    tk.Label(root, text="Adresse WebSocket").grid(row=1, column=0)
    url_entry = tk.Entry(root, width=40)
    url_entry.insert(0, SERVERS["MiniPAVI (officiel)"])
    url_entry.grid(row=1, column=1)

    def on_server_change(event):
        url = SERVERS.get(server_combo.get(), "")
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)

    server_combo.bind("<<ComboboxSelected>>", on_server_change)

    # PORT SERIE
    tk.Label(root, text="Port série").grid(row=2, column=0)
    ports = [p.device for p in serial.tools.list_ports.comports()]
    port_combo = ttk.Combobox(root, values=ports, width=20)
    if ports:
        port_combo.set(ports[0])
    port_combo.grid(row=2, column=1)

    # VITESSE
    tk.Label(root, text="Vitesse").grid(row=3, column=0)
    speeds = ["1200", "4800", "9600", "19200"]
    speed_combo = ttk.Combobox(root, values=speeds, width=20)
    speed_combo.set("1200")
    speed_combo.grid(row=3, column=1)

    # PARITÉ
    tk.Label(root, text="Parité").grid(row=4, column=0)
    parity_map = {
        "Even (pair)": serial.PARITY_EVEN,
        "Odd (impair)": serial.PARITY_ODD,
        "None": serial.PARITY_NONE,
        "Mark": serial.PARITY_MARK,
        "Space": serial.PARITY_SPACE
    }
    parity_combo = ttk.Combobox(root, values=list(parity_map.keys()), width=20)
    parity_combo.set("Even (pair)")
    parity_combo.grid(row=4, column=1)

    # DATABITS
    tk.Label(root, text="Bits de données").grid(row=5, column=0)
    databits_combo = ttk.Combobox(root, values=["7", "8"], width=20)
    databits_combo.set("7")
    databits_combo.grid(row=5, column=1)

    # STOPBITS
    tk.Label(root, text="Bits de stop").grid(row=6, column=0)
    stopbits_combo = ttk.Combobox(root, values=["1", "1.5", "2"], width=20)
    stopbits_combo.set("1")
    stopbits_combo.grid(row=6, column=1)

    # LOG
    log_widget = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
    log_widget.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    # STATUT
    status_label = tk.Label(root, text="En attente…")
    status_label.grid(row=9, column=0, columnspan=2)

    # BOUTONS
    tk.Button(
        root,
        text="Connecter",
        command=lambda: start_async(
            url_entry.get(),
            port_combo.get(),
            speed_combo.get(),
            parity_map[parity_combo.get()],
            databits_combo.get(),
            stopbits_combo.get(),
            status_label,
            log_widget
        )
    ).grid(row=7, column=0)

    tk.Button(
        root,
        text="Déconnecter",
        command=lambda: stop_connection(status_label, log_widget)
    ).grid(row=7, column=1)

    # REFRESH PORTS
    def refresh_ports():
        update_ports(port_combo)
        root.after(1000, refresh_ports)

    refresh_ports()

    root.mainloop()


if __name__ == "__main__":
    build_gui()
