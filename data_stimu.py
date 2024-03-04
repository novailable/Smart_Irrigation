import random

# FREEZE = -10
# SCORCHING = 50

MIN_TEMP = 20
MAX_TEMP = 30

MIN_MOISTURE = 10
MAX_MOISTURE = 30

STIMU_TEMP = random.uniform(MIN_TEMP, MAX_TEMP)
STIMU_MOISTURE = random.uniform(MIN_MOISTURE, MAX_MOISTURE)


def temperature_stimulation(watering=0):
    global STIMU_TEMP

    if watering == 0:
        variation = random.uniform(0.5, 1.5)
        STIMU_TEMP += variation
    else:
        variation = random.uniform(1, 2)
        STIMU_TEMP -= variation

    return STIMU_TEMP


def moisture_stimulation(watering=0):
    global STIMU_MOISTURE

    if watering == 0:
        variation = random.uniform(1, 3)
        STIMU_MOISTURE -= variation
    else:
        variation = random.uniform(2, 5)
        STIMU_MOISTURE += variation
    return STIMU_MOISTURE


def data_stimulation(watering=0):
    return moisture_stimulation(watering), temperature_stimulation(watering)
