import tkinter as tk
from tkinter import messagebox, scrolledtext
import toml
import os
from efe_chat_ui import ChatClientUI

class ChatUIVisualizer:
    def __init__(self, master):
        self.master = master
        self.chat_ui = ChatClientUI()

        master.title("Chat-Client Benutzeroberfläche")
        master.geometry("800x500")

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Konfiguration (links) ===
        config_frame = tk.Frame(main_frame, bd=2, relief="groove")
        config_frame.pack(side="left", fill="y", padx=5, pady=5)

        tk.Label(config_frame, text="Konfiguration", font=("Arial", 12, "bold")).pack(pady=5)
        self.entries = {}

        for key, value in self.chat_ui.config.items():
            tk.Label(config_frame, text=key).pack(anchor="w", padx=5)
            entry = tk.Entry(config_frame, width=25)
            entry.insert(0, str(value))
            entry.pack(padx=5, pady=2)
            self.entries[key] = entry

        tk.Button(config_frame, text="Konfiguration speichern", command=self.save_config).pack(pady=5)
        tk.Button(config_frame, text="Konfiguration anzeigen", command=self.show_config).pack(pady=2)

        # === Chatbereich (rechts) ===
        chat_frame = tk.Frame(main_frame, bd=2, relief="groove")
        chat_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.chat_display = scrolledtext.ScrolledText(chat_frame, font=("Arial", 10), state="disabled")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)

        # === Eingabezeile ===
        input_frame = tk.Frame(chat_frame)
        input_frame.pack(fill="x", padx=5, pady=5)

        self.message_entry = tk.Entry(input_frame, width=80)
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(input_frame, text="Senden", command=self.send_message)
        send_btn.pack(side="right")

    def save_config(self):
        for key, entry in self.entries.items():
            value = entry.get().strip()
            if key in ["port", "whoisport"]:
                self.chat_ui.config[key] = int(value)
            else:
                self.chat_ui.config[key] = value
        self.chat_ui.save_config(self.chat_ui.config)
        self.add_system_message("Konfiguration gespeichert.")

    def show_config(self):
        text = "\n--- Aktuelle Konfiguration ---\n"
        for key, value in self.chat_ui.config.items():
            text += f"{key}: {value}\n"
        self.add_system_message(text)

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, f"[Du] {message}\n")
            self.chat_display.config(state="disabled")
            self.chat_display.see(tk.END)
            self.message_entry.delete(0, tk.END)

    def add_system_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"[System] {message}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatUIVisualizer(root)
    root.mainloop()