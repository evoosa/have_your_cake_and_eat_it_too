from machine import Pin
import utime

WAITING_TIME = 0.001
NUM_OF_TEETH_BIG_WHEEL = 70
NUM_OF_TEETH_SMALL_WHEEL = 7
NUM_OF_SLICES = 8

NUM_OF_TEETH_PER_SLICE = (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_SLICES)
NUMBER_OF_FULL_STEPS_PER_REVOLUTION = 512
NUMBER_OF_FULL_STEPS_PER_TOOTH = (NUMBER_OF_FULL_STEPS_PER_REVOLUTION /
                                  (NUM_OF_TEETH_BIG_WHEEL / NUM_OF_TEETH_SMALL_WHEEL))
NUM_OF_FULL_STEPS_PER_SLICE = NUM_OF_TEETH_PER_SLICE * NUMBER_OF_FULL_STEPS_PER_TOOTH

pins = [
    Pin(15, Pin.OUT),  # IN1
    Pin(14, Pin.OUT),  # IN2
    Pin(16, Pin.OUT),  # IN3
    Pin(17, Pin.OUT)  # IN4
]

FULL_STEP_SEQUENCE = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]


def change_slice():
    """ spin the required distance to change a slice """
    print('[ STARTING ] change slice')
    for full_step in range(NUM_OF_FULL_STEPS_PER_SLICE):
        for iteration in FULL_STEP_SEQUENCE:
            for pin_num in range(len(pins)):
                pins[pin_num].value(iteration[pin_num])
                utime.sleep(WAITING_TIME)
    print('[ DONE ] change slice')


# for slice_num in range(NUM_OF_SLICES):
#     print(f'{slice_num + 1}\'st slice BEGIN')
#

if __name__ == '__main__':
    change_slice()
