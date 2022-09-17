from time import sleep

import utime
from machine import Pin

WAITING_TIME_BETWEEN_SEQUENCE_CHANGES = 0.001
NUM_OF_SLICES = 8
NUMBER_OF_STEPPER_FULL_STEPS_PER_REVOLUTION = 512
NUM_OF_TEETH_SMALL_WHEEL = 7  # same wheel in the platform, and the cake wheel
CAKE_HEIGHT_CM = 4

# CAKE WHEEL
NUM_OF_TEETH_BIG_WHEEL = 70

NUM_OF_BIG_WHEEL_TEETH_PER_SLICE = (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_SLICES)
NUMBER_OF_FULL_STEPS_PER_TOOTH = (NUMBER_OF_STEPPER_FULL_STEPS_PER_REVOLUTION /
                                  (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_TEETH_SMALL_WHEEL))
NUM_OF_FULL_STEPS_PER_SLICE = NUM_OF_BIG_WHEEL_TEETH_PER_SLICE * NUMBER_OF_FULL_STEPS_PER_TOOTH

# PLATFORM LIFTER
NUM_OF_FULL_STEPS_PER_CM = 85  # FIXME please improve, should be calculated

cake_wheel_pins = [
    Pin(15, Pin.OUT),  # IN1
    Pin(14, Pin.OUT),  # IN2
    Pin(16, Pin.OUT),  # IN3
    Pin(17, Pin.OUT)  # IN4
]

lowering_mechanism_pins = [
    Pin(18, Pin.OUT),  # IN1
    Pin(19, Pin.OUT),  # IN2
    Pin(13, Pin.OUT),  # IN3
    Pin(12, Pin.OUT)  # IN4
]

led_pin = Pin(25, Pin.OUT)

FULL_STEP_SEQUENCE = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]


def spin_big_cake_wheel_one_slice():
    """ spin the cake wheel the required distance to change a slice """
    print('[ STARTING ] changing slice')
    led_pin.value(1)
    for full_step in range(int(NUM_OF_FULL_STEPS_PER_SLICE)):  # this is not optimal please fix
        for iteration in FULL_STEP_SEQUENCE:
            for pin_num in range(len(cake_wheel_pins)):
                cake_wheel_pins[pin_num].value(iteration[pin_num])
                utime.sleep(WAITING_TIME_BETWEEN_SEQUENCE_CHANGES)
    led_pin.value(0)
    print('[ DONE ] changing slice')


def lower_platform():
    move_platform(1, CAKE_HEIGHT_CM)


def raise_platform():
    move_platform(0, CAKE_HEIGHT_CM)


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
        raise NameError("WTF R U TRYING TO DO BRUV! it's 0 for up and 1 for down")

    print(f'[ STARTING ] moving platform {direction_str}')
    led_pin.value(1)
    for cm_index in range(distance_cm):
        print(f'  - moved {cm_index + 1} centimeters')
        for full_step in range(NUM_OF_FULL_STEPS_PER_CM):
            for iteration in curr_sequence:
                for pin_num in range(len(lowering_mechanism_pins)):
                    lowering_mechanism_pins[pin_num].value(iteration[pin_num])
                    utime.sleep(WAITING_TIME_BETWEEN_SEQUENCE_CHANGES)
    led_pin.value(0)
    print(f'[ DONE ] moving platform {direction_str}')


def change_slice():
    """ full instructions to change a slice """
    lower_platform()
    sleep(2)
    spin_big_cake_wheel_one_slice()
    sleep(2)
    raise_platform()


if __name__ == '__main__':
    raise_platform()
    lower_platform()
