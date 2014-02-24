import bluetooth
import error
import communication


class BlueSocket(communication.Communication):
    def __init__(self):
        communication.Communication.__init__(self)
        self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    @staticmethod
    def get_nearby_devices():
        return bluetooth.discover_devices(lookup_names=True)

    def connect_by_hostname(self, hostname, port):
        devices = self.get_nearby_devices()
        for bluetooth_address, name in devices:
            if hostname.lower() == name.lower():
                break
        else:
            raise error.BrickNotFoundException("No brick by name {0} found".format(hostname))
        self.connect(bluetooth_address, port)

