# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import uuid
import time
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
import glob
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
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return temp_c


def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    #conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    conn_str = "HostName=iot-aztest726-ay220726.azure-devices.net;DeviceId=pi-requiem;SharedAccessKey=PKQ+YFcoZCykKaU/1/XtsflK/Vu2xDbtl8fsF+2Q9Tc="

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    print("IoTHub Device Client Recurring Telemetry Sample")
    print("Press Ctrl+C to exit")
    try:
        # Connect the client.
        device_client.connect()

        # Send recurring telemetry
        #i = 0
        temp_str = ""
        while True:
            #i += 1
            temp_str = str(read_temp())
            #msg = Message("test wind speed " + str(i))
            msg = Message("test temperature " + temp_str)
            msg.message_id = uuid.uuid4()
            msg.correlation_id = "correlation-1234"
            #msg.custom_properties["tornado-warning"] = "yes"
            msg.custom_properties["temperature-alert"] = "yes"
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"
            #print("sending message #" + str(i))
            print("Ambient temperature: " + temp_str)
            device_client.send_message(msg)
            time.sleep(10)
    except KeyboardInterrupt:
        print(" User initiated exit")
    except Exception:
        print("Unexpected exception!")
        raise
    finally:
        device_client.shutdown()


if __name__ == "__main__":
    main()
