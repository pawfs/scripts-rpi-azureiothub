import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)


        
def led_on(gp_input):
    gp_nb = int(gp_input)
    # set GPIO14 pin to HIGH
    GPIO.output(gp_nb,GPIO.HIGH)
    # show message to Terminal
##    print ("LED is ON")
    
def led_off(gp_input):
    gp_nb = int(gp_input)
    # set GPIO14 pin to HIGH
    GPIO.output(gp_nb,GPIO.LOW)
    # show message to Terminal
##    print ("LED is OFF")


def main():
    while True:
        led_off(14)
        led_off(15)
        led_on(14)
        time.sleep(1)
        led_off(14)
        time.sleep(1)
        led_on(15)
        time.sleep(1)
        led_off(15)
        time.sleep(1)
        
if __name__ == '__main__':
    main()
