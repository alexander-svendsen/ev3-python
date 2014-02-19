import bluetooth

target_name = "My Phone"
target_address = None


class BlueSocket():
    def __init__(self):
        self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def _get_device_address_by_name(self, hostname):
        nearby_devices = bluetooth.discover_devices()
        for bluetooth_address in nearby_devices:
            if target_name == bluetooth.lookup_name(bluetooth_address):
                return bluetooth_address

    def connect_by_hostname(self, hostname, port):
        #review port number
        bluetooth_address = self._get_device_address_by_name(hostname)
        self.connect(bluetooth_address, port)

    def connect(self, addr, port):
        self._socket.connect((addr, port))

    def send(self, data):
        self._socket.send(data)

    def receive(self, length, timeout=None):
        self._socket.settimeout(timeout)
        self._socket.recv(length)

    def close(self):
        self._socket.close()
