import config

from flask import Flask

import os


app = Flask("armo-server")


def validate_angle(angle):
    # Note: Our min angle is the arm extended, so its less than MIN_LOCK_ANGLE
    return angle <= config.MIN_LOCK_ANGLE and angle >= config.MAX_LOCK_ANGLE


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/position/<angle>")
def set_position(angle):
    angle = int(angle)
    if validate_angle(angle):
        pin = config.PWM_PIN

        pwm_position = int(config.MIN_LOCK_POSITION + (((angle - config.MIN_LOCK_ANGLE) * (config.MAX_LOCK_POSITION - config.MIN_LOCK_POSITION) / (config.MAX_LOCK_ANGLE - config.MIN_LOCK_ANGLE)))) 

        os.system("gpio pwm {} {}".format(pin, pwm_position))
        return "OK: Moved to angle{} (PWM: {})".format(angle, pwm_position)
    else:
        return "Error: Invalid angle"


@app.route("/unlock")
def unlock():
    pin = config.PWM_PIN
    pwm_position = config.UNLOCK_POSITION
    os.system("gpio pwm {} {}".format(pin, pwm_position))
    return "OK"


if __name__ == "__main__":
    os.system("gpio pwm-ms")
    os.system("gpio mode 1 pwm")
    os.system("gpio pwmc 400")
    os.system("gpio pwmr 1000")
    app.run(host="0.0.0.0")
