from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import RPi.GPIO as GPIO
import time
from time import sleep

PWM_DRIVE_LEFT = 13
PWM_DRIVE_RIGHT = 12
# Define GPIO for Motors
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 40)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 40)

# Define GPIO for ultrasonic central
GPIO_TRIGGER_CENTRAL = 21
GPIO_ECHO_CENTRAL = 23
GPIO.setup(GPIO_TRIGGER_CENTRAL, GPIO.OUT)
GPIO.setup(GPIO_ECHO_CENTRAL, GPIO.IN)

# Define GPIO for ultrasonic right
GPIO_TRIGGER_RIGHT = 22
GPIO_ECHO_RIGHT = 20
GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)

# Define GPIO for ultrasonic left
GPIO_TRIGGER_LEFT = 17
GPIO_ECHO_LEFT = 14
GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)


# Functions for driving
def goforward():
    GPIO.output(26, True)
    GPIO.output(5, True)
    GPIO.output(16, False)
    GPIO.output(6, False)
    driveLeft.value = 0.3
    driveRight.value = 0.3


def turnleft():
    GPIO.output(5, True)
    GPIO.output(6, False)
    GPIO.output(26, False)
    GPIO.output(16, False)
    time.sleep(0.8)
    GPIO.output(5, False)
    driveLeft.value = 0.3
    driveRight.value = 0.3


def turnright():
    GPIO.output(26, True)
    GPIO.output(5, False)
    GPIO.output(16, False)
    GPIO.output(6, False)
    time.sleep(0.8)
    GPIO.output(26, False)
    driveLeft.value = 0.3
    driveRight.value = 0.3


def gobackward():
    GPIO.output(16, True)
    GPIO.output(6, True)
    GPIO.output(26, False)
    GPIO.output(5, False)
    driveLeft.value = 0.3
    driveRight.value = 0.3


def stopmotors():
    GPIO.output(6, False)
    GPIO.output(16, False)
    GPIO.output(26, False)
    GPIO.output(5, False)
    driveLeft.value = 0.5
    driveRight.value = 0.5


# Detect front obstacle
def frontobstacle():
    GPIO.output(GPIO_TRIGGER_CENTRAL, False)
    time.sleep(0.2)
    GPIO.output(GPIO_TRIGGER_CENTRAL, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_CENTRAL, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO_CENTRAL) == 0:
        start = time.time()

    while GPIO.input(GPIO_ECHO_CENTRAL) == 1:
        stop = time.time()

    #   Calculate pulse length
    elapsed = stop - start

    distance = elapsed * 34000 / 2
    print("Front Distance : %.1f")
    return distance


def rightobstacle():
    GPIO.output(GPIO_TRIGGER_RIGHT, False)
    time.sleep(0.2)
    GPIO.output(GPIO_TRIGGER_RIGHT, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_RIGHT, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO_RIGHT) == 0:
        start = time.time()

    while GPIO.input(GPIO_ECHO_RIGHT) == 1:
        stop = time.time()

    #   Calculate pulse length
    elapsed = stop - start

    distance = elapsed * 34000 / 2
    print("Right Distance : %.1f")
    return distance


def leftobstacle():
    GPIO.output(GPIO_TRIGGER_LEFT, False)
    time.sleep(0.2)
    GPIO.output(GPIO_TRIGGER_LEFT, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_LEFT, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO_LEFT) == 0:
        start = time.time()

    while GPIO.input(GPIO_ECHO_LEFT) == 1:
        stop = time.time()

    #   Calculate pulse length
    elapsed = stop - start

    distance = elapsed * 34000 / 2
    print("Left Distance : %.1f")
    return distance


def checkanddrivefront():
    while frontobstacle() < 40:
        stopmotors()
        gobackward()
        time.sleep(1)
        turnright()
    goforward()


def checkanddriveright():
    while rightobstacle() < 40:
        stopmotors()
        gobackward()
        time.sleep(1)
        turnleft()
    goforward()


def checkanddriveleft():
    while leftobstacle() < 40:
        stopmotors()
        gobackward()
        time.sleep(1)
        turnright()
    goforward()


def obstacleavoiddrive():
    goforward()
    start = time.time()

    while start > time.time() - 300:
        if frontobstacle() < 15:
            stopmotors()
            checkanddrivefront()
        elif rightobstacle() < 15:
            stopmotors()
            checkanddriveright()
        elif leftobstacle() < 15:
            stopmotors()
            checkanddriveleft()

    cleargpios()


def cleargpios():
    print("clearing GPIO")
    GPIO.output(13, False)
    GPIO.output(26, False)
    GPIO.output(16, False)
    GPIO.output(12, False)
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.output(21, False)
    GPIO.output(22, False)
    GPIO.output(17, False)
    print("All GPIOs cleared ")


def main():
    cleargpios()
    print("Start Driving: ")
    obstacleavoiddrive()


if __name__ == "__main__":
    main()

GPIO.cleanup()

