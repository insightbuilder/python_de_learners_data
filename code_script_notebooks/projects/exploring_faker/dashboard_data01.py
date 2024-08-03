import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import random


def cpu_temp(ts: int):
    if ts < 5:
        # if below 5 make it 0
        return 20
    if ts > 150:
        # if above 82 then fluctuate between 82 and 95
        return random.randint(102, 125)
    # rest of the duration keep ramping up with time step
    return 2 * ts + 2.2


def fan1_temp(ts: int):
    if ts < 5:
        # if below 5 make it 0
        return 10
    if ts > 85:
        # if above 82 then fluctuate between 82 and 95
        return random.randint(90, 105)
    # rest of the duration keep ramping up with time step
    return 1.7 * ts + 15


def fan2_temp(ts: int):
    if ts < 7:
        # if below 5 make it 0
        return 12
    if ts > 90:
        # if above 82 then fluctuate between 82 and 95
        return random.randint(97, 125)
    # rest of the duration keep ramping up with time step
    return 1.5 * ts + 17


def gpu_temp(ts: int):
    if ts < 10:
        # if below 5 make it 0
        return 22
    if ts > 150:
        # if above 82 then fluctuate between 82 and 95
        return random.randint(187, 250)
    # rest of the duration keep ramping up with time step
    return 2.5 * ts + 27


def ram_temp(ts: int):
    if ts < 10:
        # if below 5 make it 0
        return 19
    if ts > 150:
        # if above 82 then fluctuate between 82 and 95
        return random.randint(157, 170)
    # rest of the duration keep ramping up with time step
    return 1.3 * ts + 17


devices = ['CPU', 'RAM', 'GPU', 'Fan1', 'Fan2']
temp_funcs = {"CPU": cpu_temp, "RAM": ram_temp, "GPU": gpu_temp,
              "Fan1": fan1_temp, "Fan2": fan2_temp}

temp_limits = {"CPU": 82, "RAM": 85, "GPU": 200,
               "Fan1": 120, "Fan2": 120}


def get_data(num: int = 1,
             dev_id: int = 0):
    fake = Faker()
    # create a timeseries dataset based on simple timesteps 
    # measured in seconds
    rows = [{
        "id": fake.uuid4().split('-')[0],
        "timestep": x,
        "device": devices[dev_id],
        "temperature": temp_funcs[devices[dev_id]](x),
        "threshold": temp_limits[devices[dev_id]],
    } for x in range(num)]

    return pd.DataFrame(rows)


# test1 = get_data(num=5, dev_id=1)
# test2 = get_data(num=5, dev_id=2)
# test3 = get_data(num=5, dev_id=3)
# test4 = get_data(num=5, dev_id=4)

# print(test1)
# print(test2)
# print(test3)
# print(test4)

fulldf = pd.concat([get_data(num=5, dev_id=x) for x in range(5)])

print(fulldf.head())
print(fulldf.tail())
