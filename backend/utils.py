import socket
import socks
from config import Config

# Save the original socket class to bypass proxy later if needed
original_socket = socket.socket

def setup_proxy():
    """Configures the global socket to use the SOCKS5 proxy."""
    socks.set_default_proxy(socks.SOCKS5, Config.PROXY_HOST, Config.PROXY_PORT)
    socket.socket = socks.socksocket

# Context manager to temporarily disable proxy
class NoProxy:
    def __enter__(self):
        self.patched_socket = socket.socket
        socket.socket = original_socket
    
    def __exit__(self, exc_type, exc_value, traceback):
        socket.socket = self.patched_socket
