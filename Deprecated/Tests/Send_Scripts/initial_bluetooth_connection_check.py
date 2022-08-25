import pygatt
import bluetooth

adapter = pygatt.GATTToolBackend()
adapter.start()

devices = adapter.scan()
for device in devices:
    rssi = device['rssi']
    address = device['address']
    print('{} - rssi = {}'.format(address, rssi))
