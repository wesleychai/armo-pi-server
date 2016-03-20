import config

from flask import Flask

import os


app = Flask("armo-server")


def validate_angle(angle):
    return angle >= config.MIN_LOCK_ANGLE and angle <= MIN_LOCK_ANGLE


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/position/<angle>")
def set_position(angle):
    if validate_angle(angle):
        pin = config.PWM_PIN
        pwm_position = int(MIN_LOCK_ANGLE - (angle * (config.MAX_LOCK_POSITION - config.MIN_LOCK_POSITION) / (MAX_LOCK_ANGLE - MIN_LOCK_ANGLE)))

        os.system("gpio pwm {} {}".format(pin, pwm_position))
        return "OK"
    else:
        return "Error: Invalid angle"


@app.route("/unlock")
def unlock():
    pin = config.PWM_PIN
    pwm_position = config.UNLOCK_POSITION
    os.system("gpio pwm {} {}".format(pin, pwm_position))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
