# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import time
import datetime
import os
#import logging
import ConfigFile
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from pyparsing import empty
from TempReading import *
from LedLight import *
from ControlAirCon import *

# temperature sensor input pin is set on GPIO 4
# IR sensor output is set on GPIO  18

# telemetry interval
INTERVAL = int(ConfigFile.interval)

#summer temperature range
MAX_SUM = int(ConfigFile.max_sum)
MIN_SUM = int(ConfigFile.min_sum)

#winter temperature range
MAX_WIN = int(ConfigFile.max_win)
MIN_WIN = int(ConfigFile.min_win)

#Leds used to signal high/low temperature
RED_LED = ConfigFile.red_led    # high temperature
GREEN_LED = ConfigFile.green_led  # low temperature


# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
#CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
CONNECTION_STRING = ConfigFile.cnx_str

TEMPERATURE = ConfigFile.temp
AC_STATE = ConfigFile.ac_state

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"temperature": {temperature} }}' #, "ac_state": {ac_state}}}'
MSG_LOG = '{{"Name": {name},"Payload": {payload}}}'

#uncomment this for extra logging
#logging.basicConfig(level=logging.INFO)


def create_client():
    # Create an IoT Hub client

    #model_id = "dtmi:com:example:NonExistingController;1"

    client = IoTHubDeviceClient.create_from_connection_string(
                CONNECTION_STRING,
                websockets=True)
    # used for communication over websockets (port 443)

    # *** Direct Method ***
    #
    # Define a method request handler
    def method_request_handler(method_request):
        global AC_STATE
        print(MSG_LOG.format(name=method_request.name, payload=method_request.payload))

        if method_request.name == "SetTelemetryInterval":
            try:
                global INTERVAL
                INTERVAL = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}, interval updated".format(method_request.name)}
                response_status = 200
                
        elif method_request.name == "RestartDevice":
            # Act on the method by restarting the program
            print("Restarting Device..")
            
            # ...and patching the reported properties
            current_time = str(datetime.datetime.now())
            reported_props = {"restartTime": current_time, "reportedValue": TEMPERATURE}
            client.patch_twin_reported_properties(reported_props)
            print( "Device twins updated with latest restartTime")
            
            # Create a method response indicating the method request was resolved
            response_status = 200
            response_payload = {"Response": "Restarted Device"}
            method_response = MethodResponse(method_request.request_id, response_status, response_payload)
            client.send_method_response(method_response)
            print("Shutting down IoTHubClient")
            led_off(GREEN_LED)
            led_off(RED_LED)
            client.shutdown()
            time.sleep(2)
            os.execv(sys.argv[0], sys.argv)
            
        elif method_request.name == "turnOnHeat":
            turn_on_heat()
            AC_STATE = "ON_HEAT"
            response_status = 200
            response_payload = {"Response": "AC On Heat Mode"}
            
        elif method_request.name == "turnOffHeat":
            turn_off_heat()
            AC_STATE = "OFF"
            response_status = 200
            response_payload = {"Response": "AC OFF"}
            
        elif method_request.name == "turnOnCool":
            turn_on_cool()
            AC_STATE = "ON_COOL"
            response_status = 200
            response_payload = {"Response": "AC On Cool Mode"}
            
        elif method_request.name == "turnOffCool":
            turn_off_cool()
            AC_STATE = "OFF"
            response_status = 200
            response_payload = {"Response": "AC OFF"}

        elif method_request.name == "SetMaxSummer":
            try:
                global MAX_SUM
                MAX_SUM = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}, MAX_SUM updated".format(method_request.name)}
                response_status = 200
                
        elif method_request.name == "SetMinSummer":
            try:
                global MIN_SUM
                MIN_SUM = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}, MIN_SUM updated".format(method_request.name)}
                response_status = 200

        elif method_request.name == "SetMaxWinter":
            try:
                global MAX_WIN
                MAX_WIN = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}, MAX_WIN updated".format(method_request.name)}
                response_status = 200
                
        elif method_request.name == "SetMinWinter":
            try:
                global MIN_WIN
                MIN_WIN = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}, MIN_WIN updated".format(method_request.name)}
                response_status = 200
                
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404
        
        method_response = MethodResponse.create_from_method_request(method_request, response_status, response_payload)
        client.send_method_response(method_response)

    # *** Cloud message ***
    #
    # define behavior for receiving a message
    def message_received_handler(message):
        print("the data in the message received was ")
        print(message.data)
        print("custom properties are")
        print(message.custom_properties)

    # *** Device Twin ***
    #
    # define behavior for receiving a twin patch
    # NOTE: this could be a function or a coroutine
    def twin_patch_handler(patch):
        print("the data in the desired properties patch was: {}".format(patch))
        # Update reported properties with information
        print ( "Sending data as reported property..." )
        reported_patch = {"reportedValue": TEMPERATURE}
        client.patch_twin_reported_properties(reported_patch)
        print ( "Reported properties updated" )

    try:
        # Attach the direct method request handler
        client.on_method_request_received = method_request_handler

        # Attach the cloud message request handler
        client.on_message_received = message_received_handler

        # Attach the Device Twin Desired properties change request handler
        client.on_twin_desired_properties_patch_received = twin_patch_handler

        client.connect()

        twin = client.get_twin()
        print ( "Twin at startup is" )
        print ( twin )
        
    except:
        # Clean up in the event of failure
        client.shutdown()
        raise

    return client


def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    client.connect()
    while True:
        # *** Sending a message ***
        # making sure the leds are off
        led_off(GREEN_LED)
        led_off(RED_LED)
        global TEMPERATURE
        global AC_STATE
        try :
            temperature = read_temp()
            TEMPERATURE = temperature
        except:
            print("Something unexpected happened")
            raise
        
        ac_state = choose_action(temperature,MAX_SUM,MIN_SUM,MAX_WIN,MIN_WIN)
        if ac_state == "no_change":
            ac_state = AC_STATE
        
        AC_STATE = ac_state
        
        msg_txt_formatted = MSG_TXT.format(temperature=temperature) # , ac_state=ac_state)
        message = Message(msg_txt_formatted)

        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        message.custom_properties["ac_state"] = ac_state

        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        if temperature > MAX_SUM:
            message.custom_properties["tempHighAlert"] = "true"
            message.custom_properties["tempLowAlert"] = "false"
            led_on(RED_LED)
            led_off(GREEN_LED)
        elif temperature < MIN_WIN:
            message.custom_properties["tempHighAlert"] = "false"
            message.custom_properties["tempLowAlert"] = "true"
            led_on(GREEN_LED)
            led_off(RED_LED)
        else:
           message.custom_properties["tempHighAlert"] = "false"
           message.custom_properties["tempLowAlert"] = "false"
           led_off(RED_LED)
           led_off(GREEN_LED)
        # Send the message.
        print("Sending message: {}".format(message))
        client.send_message(message)

        print("Message sent")
        time.sleep(INTERVAL)
        
def main():
    print ("IoT Hub: Connect Temperature Sensor ")
    print ("Press Ctrl-C to exit")
    led_on(GREEN_LED)
    led_on(RED_LED)
    
    
    # Instantiate the client. Use the same instance of the client for the duration of
    # your application
    client = create_client()
    led_off(GREEN_LED)
    led_off(RED_LED)
    # Send telemetry
    try:
        run_telemetry_sample(client)
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        print("Shutting down IoTHubClient")
        led_off(GREEN_LED)
        led_off(RED_LED)
        client.shutdown()


if __name__ == '__main__':
    main()
