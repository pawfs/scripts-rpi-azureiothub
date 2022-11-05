# temperature sensor input pin is set on GPIO 4
# IR sensor transmitter output is set on GPIO  18

# telemetry interval
interval = 60*60

# summer temperature range
max_sum = 28
min_sum = 21

# winter temperature range
max_win = 26
min_win = 15

# GPIO can be changed
red_led = 15    # high temperature
green_led = 14  # low temperature


# The device connection string to authenticate the device with your IoT hub.
cnx_str = "HostName=iot-aztest726-ay220726.azure-devices.net;DeviceId=berry-pi;SharedAccessKey=HNW6Ojih/taD6RylhnYnhn1hQef4fPReLrlTe8WJrBU="

temp = 0.0
ac_state = "OFF"
