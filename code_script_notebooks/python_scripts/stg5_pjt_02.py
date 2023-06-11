# Write your code here
class Coffeemachine:
    def __init__(self):
        self.water = 400
        self.milk = 540 
        self.coffee = 120
        self.cups = 9
        self.money = 550

    def display_stat(self):
       print(f"""
    The coffee machine has:
    {self.water} ml of water
    {self.milk} ml of milk
    {self.coffee} g of coffee beans
    {self.cups} disposable cups
    ${self.money} of money""")

    def check_resource(self,w,m,co,cu):
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
            
    def calc_espresso(self):
        tw = self.water - 250
        tm = self.milk - 0
        tc = self.coffee - 16
        tcu = self.cups - 1

        if self.check_resource(tw,tm,tc,tcu):
            self.water -= 250
            self.milk -= 0
            self.coffee -= 16
            self.cups -= 1
            self.money += 4

    def calc_latte(self):
        tw = self.water - 350
        tm = self.milk - 75
        tc = self.coffee - 20
        tcu = self.cups - 1
        
        if self.check_resource(tw,tm,tc,tcu):
            self.water -= 350
            self.milk -= 75
            self.coffee -= 20
            self.cups -= 1
            self.money += 7

    def calc_cappuccino(self):
        tw = self.water - 200
        tm = self.milk - 100
        tc = self.coffee - 12
        tcu = self.cups - 1

        if self.check_resource(tw,tm,tc,tcu):
            self.water -= 200
            self.milk -= 100
            self.coffee -= 12
            self.cups -= 1
            self.money += 6
            
    def fill(self):
        self.water += int(input("Write how many ml of water you want to add:\n"))
        self.milk += int(input("Write how many ml of milk you want to add:\n"))
        self.coffee += int(input("Write how many grams of coffee beans you want to add:\n")) 
        self.cups += int(input("Write how many disposable cups you want to add:\n"))

    def take(self):
        print(f"I gave you ${self.money}")
        self.money = 0

    def buy(self):
        what = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")

        if what == "1":
            self.calc_espresso()
        elif what == "2":
            self.calc_latte()
        elif what == "3":
            self.calc_cappuccino()
        else:
            return 

    def top_level(self,action):
        if action == 'buy':
            self.buy()
                
        elif action == 'fill':
            self.fill()
    
        elif action == 'remaining':
            self.display_stat()
        
        elif action == 'take':
            self.take()

        else:
            return 

machine = Coffeemachine()

while True:
    action = input("Write action (buy, fill, take, remaining, exit):\n")
    
    if action != 'exit':
        call = machine.top_level(action)

    else:
        break

