import socket


class IP:
    ip = None
    user_id = None
    port = 23905

    @classmethod
    def set_ip(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        cls.ip = s.getsockname()[0]
