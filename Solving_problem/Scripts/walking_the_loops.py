# Script that helps in visualising how code 
# can show movement, and how understanding 
# it can help in solving challenges
print("Objective: To show Movement and Direction change in code")

# Movement must have a start point in space
start = int(input("Provide a starting point: (say 0) "))
# and a end point
end = int(input("Provide a ending point: (say 10) "))

for i in range(end - start):
    print("#", end=' ')

print("\n")

print("Lets make a fork in the walk.\n")

fork = int(input(f"After how many steps, you want to turn (< {end}): "))

for i in range(end - start):
    # check if the fork has been reached
    if i + start <= fork:
        # no, then continue straight
        print("#", end=" ")

    else:
        # yes, then start going down
        print(" ", end='\n')
        print(" " * 2 * fork + "*", end='\n')

obj = input("Do you want to see endless loop? (yes / no) ")
obj = obj.lower()

if obj == 'yes' or obj == 'y':
    # start from 0 steps
    steps = 0
    # get user input
    print(steps)
    while True:
        print("#", end=" ")
        # add to steps
        steps += 1
        # sleep(2) 