from faker import Faker
from faker.providers import internet

obj = Faker()

# Understand how individual methods of Faker object works

print(obj.name())

print(obj.address())
print(obj.building_number())
print(obj.city())
print(obj.city_suffix())
print(obj.current_country())
print(obj.country())
print(obj.postcode())
print(obj.street_address())

# We can add data providers
obj.add_provider(internet)

print(obj.ipv4_private())

print(obj.license_plate())
print(obj.vin())

# work on the Bank data 

print(obj.aba())  # ABA routing transit number
print(obj.bank_country())  # Bank Country
print(obj.bban())  # Basic Bank Number
print(obj.iban())  # International BAN

print(obj.swift())  # Swift Code

# work on bar code

print(obj.ean8(prefixes=('36')))
print(obj.localized_ean())

# color 

print(obj.color(hue=(300, 28), luminosity = "random", color_format="hsl"))
print(obj.color_name())
print(obj.rgb_color())
print(obj.rgb_css_color())
 
# companies or organisation

print(obj.bs())
print(obj.catch_phrase())
print(obj.company())

# credit card details
print(obj.credit_card_security_code())
print(obj.credit_card_provider())
print(obj.credit_card_number())
print(obj.credit_card_full())
print(obj.credit_card_expire())

# crypto currency 

print(obj.cryptocurrency())
print(obj.cryptocurrency_code())
print(obj.cryptocurrency_name())
print(obj.currency())
print(obj.pricetag())

# Date and time

print(obj.date())
print(obj.date_object())
print(obj.date_this_month())
print(obj.date_time())

# emoji
print(obj.emoji())

# file related
print(obj.file_name())

# python
print(obj.pylist())
print(obj.pydict())
print(obj.pyint())
print(obj.pytuple())

# name
print(obj.name())
print(obj.first_name())
print(obj.last_name())
print(obj.language_name())
print(obj.name_male())
print(obj.name_female())