import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import random

def get_data(num=1):
    fake = Faker()
    devices = ['CPU', 'RAM', 'GPU', 'Fan1', 'Fan2']
    rows = [{
        "id": fake.uuid4(),
        "device": random.choice(devices),
        "temperature": 
    }]