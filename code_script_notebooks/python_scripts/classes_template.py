#!/usr/bin/env python
'''This script introduces the python classes using the rocket Example'''
import my_module

class Rocket:
    def __init__(self,name,height,weight,diameter):
        self.name = name
        self.height = height
        self.weight = weight
        self.diameter = diameter
        self.load = None

    def launch(self,altitude):
        position = self.height + altitude
        return f'Position of {self.name} is {position}'

    def rotate(self,angle):
        if angle > 90:
            print(f'Rocket {self.name} is headed to Moon')
        elif angle > 180:
            print(f'Rocket {self.name} is headed to Earth')
        else:
            print('I see, the target is sun')

    def take_load(self, other):
        self.load = other.name
        print(f'{self.name} has taken a load!!!')

    def calculate_weight(self,other):
        return self.weight + other.weight

    def have_load(self):
        if self.load:
            print(f'Yes. Load is {self.load}')
            #print(f'{self.name} weight is now {self.calculate_weight(other)}')
        else:
            print(f'No Load. {self.name} is Free')

    def turn(self,direction):
        print(f'Direction of {self.name} is {direction}')
        if direction == 'up':
            print(f'Rocket {self.name} is ready for launch')
        elif direction == 'right':
            print(f'Rocket {self.name} is in production')
        elif direction == 'left':
            print(f'Call the floor manager')
        else:
            print('You guys must be crazy...')

rocket1 = Rocket('solum',250,7807,125)
rocket2 = Rocket('prime',157,5267,170)

rocket1.rotate(150)
rocket2.launch(588)
rocket1.turn('down')
rocket2.turn('up')

rocket1.take_load(rocket2)
rocket1.have_load()
rocket2.have_load()
print('\n')
print("Lets print from the module.")
print(my_module.mod_name)
my_module.print_name()
