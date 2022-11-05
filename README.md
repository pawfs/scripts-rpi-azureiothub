# scripts-rpi-azureiothub
sample python scripts for using raspberry pi with a temperature sensor and Azure IoT Hub

Inside the TemperatureSensor folder is a python project that can send telemetry to Azure IoT Hub about the temperature sensed by the Raspberry Pi and send commands to HVAC thanks to the IR sensor.
Scripts Explained:
1. Configuration (ConfigFile.py)
This file contains the main configurable variables used in the project.

2. Main program (MainProg.py)
This program creates a client that connects to the IoT hub and sends temperature telemetry.
Before running the program, run this command from the command prompt :
cmd/sh pip3 install azure-iot-device

In the main function, first the client is initialized from the create_client function, the LEDs are turned are turned on to signal the start of the program.
Then starts the run_telemetry_sample function, the LEDs are turned off to avoid wrong signaling (of high or low temperature that might occur later).
If an interruption occurs the client is shut down safely.
The create_client function creates the client (as its name suggests) but it also has the handlers our app needs such as: method request handler, message received handler, twin patch handler.
This project relies on method request handlers to give customizable access. The program reads the method’s name to know which method will be used and uses the method’s payload whenever needed.
The client is always listening to events from the IoT Hub.
The run_telemetry_sample function loops sending temperature telemetry until an interruption occurs.
In each iteration:
 The program gets the temperature from the function read_temp.
 It runs the choose_action function which is responsible for HVAC control.
 It checks if there are any triggered alerts by the current temperature.
 It sends the message containing the temperature and custom properties (alerts) to the IoT hub.
 Finally it waits for a certain set INTERVAL to start over these last steps again.
 
3. HVAC unit control (ControlAirCon.py)
This program automatically chooses the logical action to send signals from the IR transmitter to the HVAC unit depending on the given minimum and maximum temperature (depending from the current season) and the time.

4. LED lights control (LedLight.py)
This program controls the state of the LEDs.
When called, the functions led_on and led_off can turn on and off the LEDs connected to the GPIO number passed gp_input.

5. Temperature reading (TempReading.py)
This program reads the temperature from the temperature sensor.
It gets the raw temperature from the sensor then the temperature is converted to degrees Celsius.

The other scripts are separate programs each testing a certain functionality related to the temperature sensor or Azure IoT Hub from the client side (the Raspberry Pi).

The keys used in the project are no longer functional make sure you change them if you want to test.

Used the Azure IoT Hub python samples (client side) for reference.
