import toml
import os
import sys

class ChatClientUI:
    CONFIG_FILE = "config.toml"
    DEFAULT_CONFIG = {
        "handle": "User",
        "port": 5000,
        "whoisport": 4000,
        "autoreply": "Ich bin gerade nicht da.",
        "imagepath": "./images"
    }

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.CONFIG_FILE):
            self.save_config(self.DEFAULT_CONFIG)
        with open(self.CONFIG_FILE, "r") as f:
            return toml.load(f)

    def save_config(self, config):
        with open(self.CONFIG_FILE, "w") as f:
            toml.dump(config, f)

    def show_menu(self):
        print("\n=== Chat-Client Menü ===")
        print("1. Konfiguration anzeigen")
        print("2. Konfiguration ändern")
        print("3. Programm starten")
        print("4. Beenden")

    def show_config(self):
        print("\n--- Aktuelle Konfiguration ---")
        for key, value in self.config.items():
            print(f"{key}: {value}")

    def change_config(self):
        print("\n--- Konfiguration ändern ---")
        for key in self.config:
            new_value = input(f"{key} (aktuell: {self.config[key]}): ")
            if new_value.strip():
                if key in ["port", "whoisport"]:
                    self.config[key] = int(new_value)
                else:
                    self.config[key] = new_value
        self.save_config(self.config)
        print("Konfiguration gespeichert.")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Wähle eine Option: ")
            if choice == "1":
                self.show_config()
            elif choice == "2":
                self.change_config()
            elif choice == "3":
                print("Programm wird gestartet...")
                return self.config
            elif choice == "4":
                print("Beenden...")
                sys.exit()
            else:
                print("Ungültige Auswahl, bitte erneut versuchen.")
