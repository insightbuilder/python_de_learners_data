from faker import Faker
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

Faker.seed(56)


def generate_persona(num = 1):
    # Create the faker object
    fake = Faker()
    # create dictionary of names, ids, address, dob and ssn
    rows = [{
        "person_id": fake.uuid4(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.address(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=68)
    } for x in range(num)]
    return pd.DataFrame(rows)


# persons = generate_persona(num=5)
# print(persons)

def generate_persons(num=1):
    fake = Faker()
    # create a tuple of ages between 3 and 8, make it np int32
    ages = ((np.random.beta(3, 8, size=num+1)) * 100).astype(np.int32)
    rows = [{
        "person_id": fake.uuid4(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "dob": fake.date_this_year() - relativedelta(years=ages[x]),
        "ssn": fake.ssn(),
        "DUP": fake.boolean(5)
    } for x in range(num)]
    return pd.DataFrame(rows)


persons_01 = generate_persons(num=5) 
# print(persons_01)

persons_02 = generate_persons(num=5)
concat_person = pd.concat([persons_01, persons_02], ignore_index=True)

print(concat_person.shape)
print(concat_person.head())
