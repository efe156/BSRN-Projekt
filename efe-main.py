from chat_ui import ChatClientUI

def main():
    ui = ChatClientUI()
    config = ui.run()
    # Hier können dann Netzwerk + Discovery starten:
    # start_network(config)
    # start_discovery(config)
    print(f"Starte Chat-Client mit Handle: {config['handle']} auf Port {config['port']}")

if __name__ == "__main__":
    main()

