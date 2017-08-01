"""
* reference: https://github.com/graycatlabs/PyBBIO
"""

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
    """https://community.particle.io/t/pulsein-function-for-hc-sr04-sensor/27028/2"""
    now = micros()
    while digitalRead(gpio_pin) == HIGH:
        if micros() - now > 38000:
            return 0

    now = micros()
    while digitalRead(gpio_pin) == LOW:
        if micros() - now > 38000:
            return 0

    now = micros()
    while digitalRead(gpio_pin) == HIGH:
        if micros() - now > 38000:
            return 0

    return micros() - now


def setup():
    pinMode(IN1, OUTPUT)
    pinMode(IN2, OUTPUT)
    pinMode(IN3, OUTPUT)
    pinMode(IN4, OUTPUT)
    pinMode(TrigPin, OUTPUT)
    pinMode(EchoPin, INPUT)


def loop():
    print "loop"
    duration = 0
    distance = 0
    digitalWrite(TrigPin, LOW)
    delayMicroseconds(3)
    digitalWrite(TrigPin, HIGH)
    delayMicroseconds(10)
    digitalWrite(TrigPin, LOW)
    duration = pulseIn(EchoPin, HIGH)
    distance = duration / 58

    if distance >= 200 or distance <= 4:
        print "Out of range"
    else:
        print distance, "cm", duration, "us"

    # delay(500)
    motor_control(1, 0, 1, 0)  # FORWARD
    # delay(300)
    # motor_control(0, 1, 0, 1)  # BACK
    # delay(300)
    # motor_control(1, 0, 0, 0)  # RIGHT
    # delay(300)
    # motor_control(0, 0, 1, 0)  # LEFT
    # delay(300)
    if distance < 10:
        motor_control(0, 0, 0, 0)  # STOP

    delayMicroseconds(100)

run(setup, loop)
