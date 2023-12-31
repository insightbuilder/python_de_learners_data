# Script introduces the 8 ways Logic helps to breath life into code

# Taking input from user
user_input = int(input("Choose between 1 and 2: (1:Fwd/2:Bwd)"))

# checking user has entered number
if isinstance(user_input, int):
    print("I see you have entered a number...")
else:
    print("I can only see numbers")
# Using only equal to
if user_input == 1:
    print('Move Forward')
elif user_input == 2:
    print('Move Backward')
else:
    print("Waiting...")


# Using Greater than and less than

container_cap = 15

container_avbl = 8

print(f"Fuel Tank Capacity: {container_cap}")

print(f"Available Space: {container_cap - container_avbl}")

print("_" * container_cap, end='')
print(container_cap)
print("|" * container_avbl, end='')
print(container_avbl)

# check if there is available space in tank
if container_avbl <= container_cap:
    # get the input from user
    want_fill = int(input(f"How many liters you want to fill: "))
    # after filling update the available space
    container_avbl += want_fill
    # check container is overflowing
    if container_avbl > container_cap:
        # if overflowing
        print("Tank Overflowing...")
        print("_" * container_cap, end='')  # Show the container capacity 
        print(container_cap)  # print the value of container capacity
        print("|" * container_avbl)  # Show the available material
        print(f"Wasted {(container_avbl - container_cap)} litre fuel...")  # alert if capacity exceeded
    else:  # if not overflowing
        print(f"There is {container_avbl - container_cap} litre space available")
        print("_" * container_cap, end='')
        print(container_cap)
        print("|" * (container_avbl), end='')
        print(container_avbl)

# comparing strings
print("Even strings can be compared...")

flower = input("I have jasmine / sunflower / lily, which flower you want (use lower-case): ")

if flower == 'jasmine' or flower == 'sunflower' or flower == 'lily':
    print("Here you go.. Enjoy")
elif flower == '':
    print("Type a flower name...")
else:
    print(f"Sorry don't have {flower} flower with me...")


flower = input("I have jasmine / sunflower / lily, which flower you want (use lower-case): ")

if flower != 'jasmine' and flower != 'sunflower' and flower != 'lily':
    print(f"Sorry don't have {flower} flower with me...")
elif flower == '':
    print("Type a flower name...")
else:
    print("Here you go.. Enjoy")


# catching errors and informing to user

flower_qty = input("How many flowers you want (enter numbers only): ")

try:
    qty = int(flower_qty)
    print(f"I am sending {qty} flower to you right away.")
except Exception as e:
    print("Enter a number only...")


if int(flower_qty) != 3:
    print("I can send only 3 numbers of flowers, so throwing error...")
    assert flower == 3
