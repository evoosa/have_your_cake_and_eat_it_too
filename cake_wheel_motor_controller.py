from time import sleep

import utime
from machine import Pin

WAITING_TIME = 0.001
NUM_OF_SLICES = 8
NUMBER_OF_FULL_STEPS_PER_REVOLUTION = 512

# CAKE WHEEL
NUM_OF_TEETH_BIG_WHEEL = 70
NUM_OF_TEETH_SMALL_WHEEL = 7

NUM_OF_BIG_WHEEL_TEETH_PER_SLICE = (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_SLICES)
NUMBER_OF_FULL_STEPS_PER_TOOTH = (NUMBER_OF_FULL_STEPS_PER_REVOLUTION /
                                  (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_TEETH_SMALL_WHEEL))
NUM_OF_FULL_STEPS_PER_SLICE = NUM_OF_BIG_WHEEL_TEETH_PER_SLICE * NUMBER_OF_FULL_STEPS_PER_TOOTH

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
    print('[ STARTING ] change slice')
    led_pin.value(1)
    for full_step in range(int(NUM_OF_FULL_STEPS_PER_SLICE)):  # this is not optimal please fix
        for iteration in FULL_STEP_SEQUENCE:
            for pin_num in range(len(cake_wheel_pins)):
                cake_wheel_pins[pin_num].value(iteration[pin_num])
                utime.sleep(WAITING_TIME)
    led_pin.value(0)
    print('[ DONE ] change slice')


def lower_cake_platform():
    pass


def raise_cake_platform():
    pass


def change_slice():
    lower_cake_platform()
    sleep(2)
    spin_big_cake_wheel_one_slice()
    sleep(2)
    raise_cake_platform()


# for slice_num in range(NUM_OF_SLICES):
#     print(f'{slice_num + 1}\'st slice BEGIN')

if __name__ == '__main__':
    spin_big_cake_wheel_one_slice()
