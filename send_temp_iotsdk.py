import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return temp_c

async def main():
    #print temperature
    temp_str = str(read_temp())
    print("Ambient temperature: " + temp_str)

    # Fetch the connection string from an enviornment variable
    #conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    conn_str = "HostName=iot-aztest726-ay220726.azure-devices.net;DeviceId=pi-requiem;SharedAccessKey=PKQ+YFcoZCykKaU/1/XtsflK/Vu2xDbtl8fsF+2Q9Tc="
    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()
    
    # Send a single message
    print("Sending message...")
    await device_client.send_message(temp_str)
    print("Message successfully sent!")

    # finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
