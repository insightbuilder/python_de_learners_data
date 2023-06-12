with open('hyperskill-dataset-83046399.txt','r') as hyp:
    x = hyp.read().splitlines()
count = 0
print(x)
for l in x:
    if l == 'summer':
        count += 1

print(count)
