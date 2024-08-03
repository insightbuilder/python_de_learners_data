# Pydantic is extensively used for type checking and data parsing.
# Script will contain the details of how they are implemented, by way of comparison
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from typing import List, Optional, Any
import pydantic
from pydantic import (
    BaseModel,
    EmailStr,
    PositiveInt,
    conlist,
    Field,
    HttpUrl,
    field_validator,  # validates a field
    model_validator,  # validates entire model
    Field,
    computed_field,
    ValidationError
)
print(pydantic.__version__)


# implementing the class with manual type checking
class User:
    def __init__(self, id: int, name='jane doe') -> None:
        if not isinstance(id, int):
            raise TypeError(f"Expected id to be an int, got {type(id).__name__}")

        if not isinstance(name, str):
            raise TypeError(f"Expected name to be str, got {type(name).__name__}")

        self.id = id
        self.name = name


# try:
    # user = User(id=125)
    # user = User(id='125')
# except Exception as e:
    # print(e)


class UserPy(BaseModel):
    id: int
    name: str = 'jane doe'


try:
    # print("Reaching here")
    user = UserPy(id='556')  # Even if it is string, it will still pass
    user = UserPy(id='66', name='locomotiv')
    user = UserPy(id='66', name='locomotiv')
    # user = UserPy(id='ax556')
except Exception as e:
    print(e)

try:
    UserPy.model_validate({'id':'42', 'username': 'john_doe'}, strict=True)
except ValidationError as exc:
    print(exc)

# get the attributes instantiated
# print(user.model_fields_set)  # will require the object instance instantiated with {'id', 'name'} 

# dumping specs
# print(user.model_dump())  # {'id': 66, 'name': 'locomotiv'}
# print(user.model_dump_json())  # {"id":66,"name":"locomotiv"}
# print(user.model_json_schema()) 
# {'properties': {'id': {'title': 'Id', 'type': 'integer'}, 'name': {'default': 'jane doe', 'title': 'Name', 'type': 'string'}}, 'required': ['id'], 'title': 'UserPy', 'type': 'object'}


# Nested Model creation
class Food(BaseModel):
    name: str
    price: float
    ingredients: Optional[List[str]] = None


class Restaurant(BaseModel):
    name: str
    location: str
    foods: List[Food]


res_inst = Restaurant(
    name="Tasty Bites",
    location="123, Flavor Street",
    foods=[
        {"name": "Cheese Pizza",
         "price": 12.50,
         "ingredients": ["Cheese", "Tomato Sauce", "Dough"]},
        {"name": "Veggie Burger",
         "price": 8.55}
    ]
)

# print(res_inst)
# print(res_inst.model_dump())


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Employee(BaseModel):
    name: str
    position: str
    email: EmailStr


class Owner(BaseModel):
    name: str
    email: EmailStr


class Restaurant(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9-' ]+$")
    owner: Owner
    address: Address
    employees: conlist(Employee, min_length=2)  # Constrained List
    number_of_seats: PositiveInt
    delivery: bool
    website: HttpUrl


res_inst1 = Restaurant(
    name="Tasty Bites",
    owner={
        "name":"Jane Doe",
        "email": "John.doe@example.com"
    },
    address={
        "street":"123, Flavor Street",
        "city": "TastyTown",
        "state": "NRS",
        "zip_code": "12345",
    },
    employees=[{
        "name": "Mike",
        "position": "Boss",
        "email": "mike@boss.com"
    }, {
        "name": "Mike",
        "position": "Boss",
        "email": "mike@boss.com"
    }],
    number_of_seats=50,
    delivery=True,
    website="http://tastybites.com"
)

print(res_inst1.model_dump_json())
print(res_inst1.model_fields_set)


class Owner(BaseModel):
    name: str
    email: EmailStr

    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("Owner name must contain a space.")
        return v.title()


try:
    owner_instance = Owner(name="jane doe", email="john@boss.com")
except ValueError as e:
    print(e)


class Owner(BaseModel):
    name: str
    email: EmailStr

    @model_validator(mode='before')
    @classmethod
    def check_sensitive_info_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'password' in data:
                raise ValueError('Password should not be included')
            if 'card_number' in data:
                raise ValueError('Card number must be removed')
        return data

    @model_validator(mode='after')
    def name_must_contain_space(self) -> Owner:  # this is regular method, 
        if " " not in self.name:  # check the name
            raise ValueError("Owner name must contain a space.")
        return self

# newOwner = Owner(name='New John', password='56therto', email='boss@the.com')
# newOwner = Owner(name='New John', email='boss@the.com', location="marus")
newOwner = Owner(name='New John', email='boss@the.com')
print(newOwner)


# with field we can use default factory
class User(BaseModel):
    id: int = Field(default_factory=lambda: uuid4().hex)


user = User()
# print(user)


class User(BaseModel):
    username: str = Field(..., min_length=5,
                          max_length=10,
                          pattern=r'^\w+$')
    email: EmailStr = Field(...)
    age: int = Field(..., gt=0, le=120)
    height: float = Field(..., gt=0.0)
    is_active: bool = Field(True)
    balance: Decimal = Field(..., max_digits=10, decimal_places=2)
    favorite_numbers: List[int] = Field(..., min_items=1)


user_inst = User(
    username="johndoes",
    age=30,
    height=5.9,
    weight=160.5,
    email="john.doe@example.com",
    password="securepassword",
    balance=9999.77,
    favorite_numbers=[1, 2, 3]
)

# print(user_inst.model_dump())


class Person(BaseModel):
    name: str
    birth_year: int

    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year


print(Person(name="J Doe", birth_year=2000).model_dump())  # {'name': 'J Doe', 'birth_year': 2000, 'age': 24}
