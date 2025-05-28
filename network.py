import socket
try:
    import toml
except ImportError:
    print("Error: toml library not found. Please install it with 'pip install toml'")
    exit(1)

# Funktion zum Laden der Konfiguration aus der config.toml-Datei
def load_config(config_path: str = 'config.toml') -> dict:
    try:
        # Öffne die Konfigurationsdatei und lade sie mit toml
        with open(config_path, 'r') as f:
            config = toml.load(f)
            return config
    except FileNotFoundError:
        print(f"Error: Config file {config_path} not found.")
        return {}
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

# Funktion zum Senden des JOIN-Broadcasts
def send_join_broadcast(handle: str, port: int) -> None:
    try:
        # Erstelle einen UDP-Socket und aktiviere Broadcast
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Erstelle die Nachricht im Format "JOIN <Handle> <Port>\n"
        message = f"JOIN {handle} {port}\n" 
        # Sende die Nachricht an alle Geräte im Netzwerk
        udp_socket.sendto(message.encode('utf-8'), ('255.255.255.255', port))
        print(f"Sent JOIN broadcast: {message.strip()}")
    except Exception as e:
        print(f"Error sending JOIN broadcast: {e}")

# Funktion zum Senden der LEAVE-Nachricht per UDP-Broadcast
def send_leave_broadcast(handle: str, port: int) -> None:
    try:
        # Erstelle UDP-Socket und aktiviere Broadcast
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        message = f"LEAVE {handle}\n"
        udp_socket.sendto(message.encode('utf-8'), ('255.255.255.255', port))
        print(f"Sent LEAVE broadcast: {message.strip()}")
    except Exception as e:
        print(f"Error sending LEAVE broadcast: {e}")

# Funktion zum Senden der LEAVE-Nachricht per TCP an alle Peers
def send_leave_tcp(handle: str, peers: dict) -> None:
    for peer_handle, (ip, port) in peers.items():
        try:
            # Erstelle TCP-Socket und verbinde zum Peer
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((ip, port))
            message = f"LEAVE {handle}\n"
            tcp_socket.sendall(message.encode('utf-8'))
            tcp_socket.close()
            print(f"Sent LEAVE to {peer_handle} at {ip}:{port}")
        except Exception as e:
            print(f"Error sending LEAVE to {peer_handle}: {e}")

# Funktion zum Senden einer Nachricht an einen Peer
def send_msg(handle: str, text: str, peer_ip: str, peer_port: int) -> None:
    try:
        # Erstelle TCP-Socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Verbinde zum Peer
        tcp_socket.connect((peer_ip, peer_port))
        # Erstelle die Nachricht im Format "MSG <Handle> <Text>\n"
        message = f"MSG {handle} {text}\n"
        # Sende die Nachricht als UTF-8 kodierten Text
        tcp_socket.sendall(message.encode('utf-8'))
        tcp_socket.close()
        print(f"Sent MSG to {handle} at {peer_ip}:{peer_port}")
    except Exception as e:
        print(f"Error sending MSG to {handle}: {e}")

# Temporäre Liste der bekannten Peers (noch nicht implementiert)
peers = {
    'Bob': ('127.0.0.1', 12001)  # Beispiel-Peer für Testzwecke
}

if _name_ == "_main_":
    config = load_config()
    if config:
        # Test JOIN
        send_join_broadcast(config.get('handle', 'DefaultHandle'), 4000)
        # Test LEAVE
        send_leave_broadcast(config.get('handle', 'DefaultHandle'), 4000)  # UDP an Port 4000
        send_leave_tcp(config.get('handle', 'DefaultHandle'), peers)  # TCP an alle Peers
        # Test MSG
        send_msg(
            config.get('handle', 'DefaultHandle'),
            "Hallo Bob, wie geht's?",
            peers['Bob'][0],  # IP-Adresse von Bob
            peers['Bob'][1]    # Port von Bob
        )
