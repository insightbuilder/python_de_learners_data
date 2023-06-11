# Write your code here
water = 400
milk = 540 
coffee = 120
cups = 9
money = 550

def display_stat():
    global water
    global milk
    global coffee
    global cups
    global money
    print(f"""
The coffee machine has:
{water} ml of water
{milk} ml of milk
{coffee} g of coffee beans
{cups} disposable cups
${money} of money""")

def check_resource(w,m,co,cu):
    if w <= 0:
        print("Sorry, not enough water!")
        return False
    elif m <= 0:
        print("Sorry, not enough milk!")
        return False
    elif co <= 0:
        print("Sorry, not enough coffee!")
        return False
    elif cu <= 0:
        print("Sorry, not enough cups!")
        return False
    else:
        print("I have enough resources, making you a coffee!")
        return True
        
def calc_espresso():
    global water
    global milk
    global coffee
    global cups
    global money

    tw = water - 250
    tm = milk - 0
    tc = coffee - 16
    tcu = cups - 1

    if check_resource(tw,tm,tc,tcu):
        water -= 350
        milk -= 75
        coffee -= 20
        cups -= 1
        money += 4

def calc_latte():
    global water
    global milk
    global coffee
    global cups
    global money
    
    tw = water - 350
    tm = milk - 75
    tc = coffee - 20
    tcu = cups - 1
    
    if check_resource(tw,tm,tc,tcu):
        water -= 350
        milk -= 75
        coffee -= 20
        cups -= 1
        money += 7

def calc_cappuccino():
    global water
    global milk
    global coffee
    global cups
    global money

    tw = water - 250
    tm = milk - 0
    tc = coffee - 16
    tcu = cups - 1

    if check_resource(tw,tm,tc,tcu):
        water -= 200
        milk -= 100
        coffee -= 12
        cups -= 1
        money += 6
        
def fill():
    global water
    global milk
    global coffee
    global cups

    water += int(input("Write how many ml of water you want to add:\n"))
    milk += int(input("Write how many ml of milk you want to add:\n"))
    coffee += int(input("Write how many grams of coffee beans you want to add:\n")) 
    cups += int(input("Write how many disposable cups you want to add:\n"))

def take():
    global money
    print(f"I gave you ${money}")
    money = 0

def buy():
    while True:
        what = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")

        if what == "1":
            calc_espresso()
        elif what == "2":
            calc_latte()
        elif what == "3":
            calc_cappuccino()
        else:
            return

while True:

    action = input("Write action (buy, fill, take, remaining, exit):\n")
    
    if action == 'buy':
        buy()
            
    elif action == 'fill':
        fill()

    elif action == 'remaining':
        display_stat()
    
    elif action == 'take':
        take()

    else:
        break
