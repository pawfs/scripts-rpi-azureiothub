import time
from azure.iot.device import IoTHubModuleClient

CONNECTION_STRING = "HostName=iot-aztest726-ay220726.azure-devices.net;DeviceId=pi-requiem;SharedAccessKey=PKQ+YFcoZCykKaU/1/XtsflK/Vu2xDbtl8fsF+2Q9Tc="

def create_client():
    # Instantiate client
    client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)

    # Define behavior for receiving twin desired property patches
    def twin_patch_handler(twin_patch):
        print("Twin patch received:")
        print(twin_patch)

    try:
        # Set handlers on the client
        client.on_twin_desired_properties_patch_received = twin_patch_handler
    except:
        # Clean up in the event of failure
        client.shutdown()

    return client

def main():
    print ( "Starting the Python IoT Hub Device Twin device sample..." )
    client = create_client()
    print ( "IoTHubModuleClient waiting for commands, press Ctrl-C to exit" )

    try:
        # Update reported properties with cellular information
        print ( "Sending data as reported property..." )
        reported_patch = {"connectivity": "wi-fi"}
        client.patch_twin_reported_properties(reported_patch)
        print ( "Reported properties updated" )

        # Wait for program exit
        while True:
            time.sleep(1000000)
    except KeyboardInterrupt:
        print ("IoT Hub Device Twin device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()

if __name__ == '__main__':
    main()
