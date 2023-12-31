# Script introduces how functions supercharge problem solving

def show_status(capacity: int, available: int, is_overflown=False, *args, **kwargs) -> None:
    """Shows tank fuel status graphically"""
    print("_" * capacity, end='')  # Show the container capacity 
    print(capacity)  # print the value of container capacity
    print("|" * available, end='')  # Show the available material
    if is_overflown:
        print('\n')
        # alert if capacity exceeded
        print(f"Wasted {(available - capacity)} litre fuel...")  
    else:
        print(available)  # else just print available
    # return None


def expend(fuel_cost: int, purchase: int) -> int:
    """Returns the total expenditure on fuel"""
    return fuel_cost * purchase


# check if the function is working correctly
assert expend(50, 5) == 20
assert expend(95, 62) == 5890

print(__name__)

if __name__ == "__main__":

    container_cap = int(input("What is the container capacity : (Numbers) "))

    container_avbl = int(input("How much fuel is available: (Number) "))

    show_status(container_cap, container_avbl)

    # check if there is available space in tank
    if container_avbl <= container_cap:
        # get the input from user
        want_fill = int(input("How many liters you want to fill: "))
        # after filling update the available space
        container_avbl += want_fill
        # provide status
        if container_avbl > container_cap:
            show_status(container_cap, container_avbl, is_overflown=True)
        else:  # if not overflowing
            show_status(container_cap, container_avbl)
        # show expediture
        print(f"{expend(50, want_fill)} INR")
