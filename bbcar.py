"""
Title        : Autonomous Driving Car using Beaglebone Black
Author       : genonfire, zzeromin
Creation Date: Aug 1, 2017
Cafe         : http://cafe.naver.com/dswise
Reference    : PyBBIO, Adafruit_BBIO
* https://github.com/graycatlabs/PyBBIO
* https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/using-the-bbio-library
Free and open for all to use. But put credit where credit is due.
"""

# Import the library:
import Adafruit_BBIO.GPIO as GPIO
import time

# L298N(Motor Driver)4 PIN
IN1 = "P8_13"
IN2 = "P8_15"
IN3 = "P8_14"
IN4 = "P8_16"

# HC-SR04(Ultrasonic ranging module) 2PIN
TrigPin = "P8_12"
EchoPin = "P8_11"

# GPIO Setup
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(TrigPin, GPIO.OUT)
GPIO.setup(EchoPin, GPIO.IN)

START_TIME_MS = time.time()*1000

def millis():
    """ Returns roughly the number of millisoconds since program start. """
    return time.time()*1000 - START_TIME_MS

def micros():
    """ Returns roughly the number of microsoconds since program start. """
    return time.time()*1000000 - START_TIME_MS*1000
  
def delay(ms):
    """ Sleeps for given number of milliseconds. """
    time.sleep(ms/1000.0)

def delayMicroseconds(us):
    """ Sleeps for given number of microseconds > ~30; still working
      on a more accurate method. """
    t = time.time()
    while (((time.time()-t)*1000000) < us): pass


def motor_control(i1, i2, i3, i4):
    GPIO.output(IN1, i1)
    GPIO.output(IN2, i2)
    GPIO.output(IN3, i3)
    GPIO.output(IN4, i4)


def pulseIn(gpio_pin, value, timeout=400):
    """https://community.particle.io/t/pulsein-function-for-hc-sr04-sensor/27028/2"""
    now = micros()
    while GPIO.input(gpio_pin) == GPIO.HIGH:
        if micros() - now > 38000:
            return 0

    now = micros()
    while GPIO.input(gpio_pin) == GPIO.LOW:
        if micros() - now > 38000:
            return 0

    now = micros()
    while GPIO.input(gpio_pin) == GPIO.HIGH:
        if micros() - now > 38000:
            return 0

    return micros() - now


while True:

    duration = 0
    distance = 0
    GPIO.output(TrigPin, GPIO.LOW)
    delayMicroseconds(3)
    GPIO.output(TrigPin, GPIO.HIGH)
    delayMicroseconds(10)
    GPIO.output(TrigPin, GPIO.LOW)
    duration = pulseIn(EchoPin, GPIO.HIGH)
    distance = duration / 58

    if distance >= 200 or distance <= 4:
        print "Out of range"
    else:
        print distance, "cm", duration, "us"

    motor_control(1, 0, 1, 0)  # FORWARD
    # delay(300)
    # motor_control(0, 1, 0, 1)  # BACK
    # delay(300)
    # motor_control(1, 0, 0, 0)  # RIGHT
    # delay(300)
    # motor_control(0, 0, 1, 0)  # LEFT
    # delay(300)

    if distance < 10:
        print "stop", distance, "cm"
        motor_control(0, 0, 0, 0)  # STOP
        delay(1000)
        motor_control(0, 1, 1, 0)  # LEFT
        delay(200)
        motor_control(0, 0, 0, 0)  # STOP
        delay(500)

    delay(100)
