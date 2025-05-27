from chat_ui import ChatClientUI

def main():
    ui = ChatClientUI()
    config = ui.run()
    print(f"Starte Chat-Client mit Handle: {config['handle']} auf Port {config['port']}")

if __name__ == "__main__":
    main()
