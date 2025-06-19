"""
main.py

Startet die Chat-Client-Anwendung mit:
1) einer Benutzeroberfläche (UI)
2) einem Netzwerk-Prozess, der beim Start einen JOIN-Broadcast schickt
   und beim Ende einen LEAVE-Broadcast.
"""

import toml
import sys
import signal
from multiprocessing import Process, Queue

from efe_chat_ui import ChatClientUI
from import_socket import send_join_broadcast, send_leave_broadcast

def send_join(port: int, handle: str):
    """Schickt einen JOIN-Broadcast an alle Geräte im Netzwerk."""
    try:
        print(f"Sende JOIN-Broadcast: Handle={handle}, Port={port}")
        send_join_broadcast(handle, port)
    except Exception as e:
        print(f"[Fehler beim JOIN-Broadcast] {e}")

def cleanup_and_exit(handle: str, port: int, processes: list):
    """
    Sendet einen LEAVE-Broadcast
    undbeendet das Hauptprogramm.
    """
    try:
        print(f"Sende LEAVE-Broadcast: Handle={handle}")
        send_leave_broadcast(handle, port)
    except Exception as e:
        print(f"[Fehler beim LEAVE-Broadcast] {e}")
    finally:
        for proc in processes:
            print(f"Beende Prozess {proc.name} …")
            proc.terminate()
        sys.exit(0)

def main():
    config = toml.load("config.toml")
    ui = ChatClientUI(config_path="config.toml")

    ui_to_net = Queue()
    net_to_ui = Queue()

    processes = [
        Process(target=ui.run, args=(ui_to_net, net_to_ui), name="UI-Prozess"),
        Process(target=send_join, args=(config["port"], config["handle"]), name="JOIN-Prozess")
    ]

    # Prozesse starten
    for proc in processes:
        proc.start()

    # Auf Ende warten
    for proc in processes:
        proc.join()
        
if __name__ == "__main__":
    main()
