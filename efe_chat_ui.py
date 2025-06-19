import toml
import os
import sys

class ChatClientUI:
    CONFIG_FILE = "efe-config.toml"
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
        for key in self.config:
            new_value = input(f"{key} (aktuell: {self.config[key]}): ")
            if new_value.strip():
                self.config[key] = int(new_value) if key in ["port", "whoisport"] else new_value
        self.save_config(self.config)
        print("Gespeichert!")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Wähle eine Option: ")
            if choice == "1":
                self.show_config()
            elif choice == "2":
                self.change_config()
            elif choice == "3":
                print(f"\nStarte Chat-Client mit Handle: {self.config['handle']} auf Port {self.config['port']}...\n")
                print("[Simulation] Nachricht empfangen von Bob: \"Hey, bist du da?\"")
                print("[Simulation] Nachricht empfangen von Alice: \"Bild empfangen: cat.jpg\"")
                print(f"[Simulation] Autoreply gesendet: \"{self.config['autoreply']}\"")
                input("\nDrücke Enter, um zurückzukehren...")
            elif choice == "4":
                print("Beenden...")
                sys.exit()
            else:
                print("Ungültige Eingabe.")

if __name__ == "__main__":
    ui = ChatClientUI()
    ui.run()
