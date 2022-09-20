from time import sleep

import utime
from machine import Pin

WAITING_TIME_BETWEEN_SEQUENCE_CHANGES = 0.001
NUM_OF_SLICES = 8
NUMBER_OF_STEPPER_FULL_STEPS_PER_REVOLUTION = 512
NUM_OF_TEETH_SMALL_WHEEL = 7  # same wheel in the platform, and the cake wheel
CAKE_HEIGHT_CM = 7.5

# CAKE WHEEL
NUM_OF_TEETH_BIG_WHEEL = 70

NUM_OF_BIG_WHEEL_TEETH_PER_SLICE = (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_SLICES)
NUMBER_OF_FULL_STEPS_PER_TOOTH = (NUMBER_OF_STEPPER_FULL_STEPS_PER_REVOLUTION /
                                  (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_TEETH_SMALL_WHEEL))
NUM_OF_FULL_STEPS_PER_SLICE = NUM_OF_BIG_WHEEL_TEETH_PER_SLICE * NUMBER_OF_FULL_STEPS_PER_TOOTH

# PLATFORM LIFTER
NUM_OF_FULL_STEPS_PER_CM = 53  # FIXME please improve, should be calculated

cake_wheel_servo_pins = [
    Pin(15, Pin.OUT),  # IN1
    Pin(14, Pin.OUT),  # IN2
    Pin(16, Pin.OUT),  # IN3
    Pin(17, Pin.OUT)  # IN4
]

platform_servo_pins = [
    Pin(18, Pin.OUT),  # IN1
    Pin(19, Pin.OUT),  # IN2
    Pin(13, Pin.OUT),  # IN3
    Pin(12, Pin.OUT)  # IN4
]

led_pin = Pin(25, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

FULL_STEP_SEQUENCE = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]


def turn_off_stepper(pins: list):
    """ reset the stepper pins, turn them off """
    [pins[pin_idx].value(0) for pin_idx in range(len(pins))]
    print(f'[ !!! ] turned off stepper motor')


def spin_big_cake_wheel_one_slice():
    """ spin the cake wheel the required distance to change a slice """
    print('[ STARTING ] changing slice')
    led_pin.value(1)
    for full_step in range(int(NUM_OF_FULL_STEPS_PER_SLICE)):  # this is not optimal please fix
        for iteration in FULL_STEP_SEQUENCE:
            for pin_num in range(len(cake_wheel_servo_pins)):
                cake_wheel_servo_pins[pin_num].value(iteration[pin_num])
                utime.sleep(WAITING_TIME_BETWEEN_SEQUENCE_CHANGES)
    led_pin.value(0)
    turn_off_stepper(cake_wheel_servo_pins)
    print('[ DONE ] changing slice')


def lower_platform():
    move_platform(0, CAKE_HEIGHT_CM)
    turn_off_stepper(platform_servo_pins)


def raise_platform():
    move_platform(1, CAKE_HEIGHT_CM)
    turn_off_stepper(platform_servo_pins)


def move_platform(direction: int, distance_cm: int):
    """ move platform in the given direction, the given amount of centimeters """
    if direction == 0:
        direction_str = 'up'
        curr_sequence = FULL_STEP_SEQUENCE.copy()
        curr_sequence.reverse()
    elif direction == 1:
        direction_str = 'down'
        curr_sequence = FULL_STEP_SEQUENCE
    else:
        raise NameError("WTF R U TRYING TO DO BRUV! it's 1 for up and 0 for down")

    print(f'[ STARTING ] moving platform {direction_str}')
    led_pin.value(1)
    for cm_index in range(distance_cm):
        print(f'  - moved {cm_index + 1} centimeters')
        for full_step in range(NUM_OF_FULL_STEPS_PER_CM):
            for iteration in curr_sequence:
                for pin_num in range(len(platform_servo_pins)):
                    platform_servo_pins[pin_num].value(iteration[pin_num])
                    utime.sleep(WAITING_TIME_BETWEEN_SEQUENCE_CHANGES)
    led_pin.value(0)
    print(f'[ DONE ] moving platform {direction_str}')


def change_slice():
    """ full instructions to change a slice """
    lower_platform()
    spin_big_cake_wheel_one_slice()
    raise_platform()


if __name__ == '__main__':
    while True:
        if button.value():
            change_slice()


# TODO
# 12V instead of 5V
# make sure with dror if he's going to help with wifi
# to cake
# fix wifi
# to sand the plastic parts and make sure it runs smoothly
# add a minimal functinality to "push a a button" for step change
# FIX NUMBER OF TEETH IN SMALL WHEEL!!!!!
