# Script that takes the input through CLI, 
# using input function, reading file

import sys

data1 = sys.argv[0]
data2 = sys.argv[1]

print(f'Command line arg1: {data1}')
print(f'Command line arg2: {data2}')

data3 = input("Give your input here: ")

print(f"Text recieved from input function: {data3}")

print("we will see the input from data.txt file")
path = "D:\\gitFolders\\python_de_learners_data\\Solving_problem\\Scripts\\data.txt"

with open(file=path, mode='r', encoding='utf-8') as raw:
    lines = raw.readlines()
    for l in lines:
        print(l)
