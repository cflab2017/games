import socket
import pickle
import struct

# --- Network Protocol Helpers ---
def send_msg(sock, msg):
    """Prefixes a message with a 4-byte length before sending."""
    msg = pickle.dumps(msg)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    """Reads a message with a 4-byte length prefix."""
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Now read the full message
    return pickle.loads(recvall(sock, msglen))

def recvall(sock, n):
    """Helper function to recv n bytes or return None if EOF is hit."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# --- Main Network Class ---
class Network:
    def __init__(self,host=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host is None:
            host = self.get_host_ip()
        # self.server = "127.0.0.1"
        self.port = 9993
        self.addr = (host, self.port)
        self.player_id = self.connect()

        
    def get_host_ip(self):        
        with open("host.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n','')
                line = line.replace(' ','')
                if line.find('#')>=0:
                    continue
                if len(line.split('.')) != 4:
                    print(line)
                    continue
                print(line)
                return line
        
    def get_player_id(self):
        return self.player_id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return recv_msg(self.client)
        except socket.error as e:
            print(f"Connection Error: {e}")
            return None

    def send_and_receive(self, data):
        """Sends data to the server and waits for a direct reply."""
        try:
            send_msg(self.client, data)
            return recv_msg(self.client)
        except socket.error as e:
            print(f"Send/Receive Error: {e}")
            return None

    def send_only(self, data):
        """Sends data to the server without waiting for a reply."""
        try:
            send_msg(self.client, data)
            return True
        except socket.error as e:
            print(f"Send Only Error: {e}")
            return False

    def receive(self):
        """Waits for and receives data from the server (blocking)."""
        try:
            return recv_msg(self.client)
        except socket.error as e:
            print(f"Receive Error: {e}")
            return None
        except (pickle.UnpicklingError, EOFError, struct.error) as e:
            print(f"Data Error: {e}")
            return None
