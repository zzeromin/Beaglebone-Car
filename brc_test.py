# Import the library:
from bbio import *

# L298N(Motor Driver)4 PIN
IN1 = GPIO2_2
IN2 = GPIO2_5
IN3 = GPIO2_3
IN4 = GPIO2_4

# HC-SR04(Ultrasonic ranging module) 2PIN
TrigPin = GPIO1_12
EchoPin = GPIO1_13


def motor_control(i1, i2, i3, i4):
    digitalWrite(IN1, i1)
    digitalWrite(IN2, i2)
    digitalWrite(IN3, i3)
    digitalWrite(IN4, i4)


def pulseIn(gpio_pin, value, timeout=400):
    """ pulseIn by Bence Magyar. """
    """ timeout default value represents 400 cm sonar distance signal length. $
    """ Returns length of chosen signal in microseconds. """
#    assert (gpio_pin in bbio), "*Invalid GPIO pin: '%s'" % gpio_pin
    assert (value in [HIGH, LOW]), "*Invalid value parameter: '%d'" % value
    endSig = value
    startSig = LOW if value==HIGH else HIGH
    start = micros()
    while digitalRead(gpio_pin) == startSig and (micros()-start) < timeout:
        delayMicroseconds(30)
        if micros()-start > timeout:
            return timeout
    start = micros()
    while digitalRead(gpio_pin) == endSig and (micros()-start) < timeout:
        delayMicroseconds(30)
        return micros() - start


def setup():
    pinMode(IN1, OUTPUT)
    pinMode(IN2, OUTPUT)
    pinMode(IN3, OUTPUT)
    pinMode(IN4, OUTPUT)
    pinMode(TrigPin, OUTPUT)
    pinMode(EchoPin, INPUT)


def loop():
    duration = 0
    distance = 0
    digitalWrite(TrigPin, LOW)
    delayMicroseconds(3);
    digitalWrite(TrigPin, HIGH)
    delayMicroseconds(10)
    digitalWrite(TrigPin, LOW)
    duration = pulseIn(EchoPin, HIGH)
#    distance =  duration / 2 / 29

#    print(distance)
#    delay(500)

    motor_control(0, 0, 0, 0) # STOP
    delay(500)
    motor_control(1, 0, 1, 0) # FORWARD
    delay(300)
    motor_control(0, 1, 0, 1) # BACK
    delay(300)
    motor_control(1, 0, 0, 0) # RIGHT
    delay(300)
    motor_control(0, 0, 1, 0) # LEFT
    delay(300)

run (setup, loop)
