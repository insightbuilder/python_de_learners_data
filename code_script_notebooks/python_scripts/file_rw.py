#!/usr/bin/env python

"""This file is the example for the file_io activity"""

print("The trial_file.txt is shared with you in the Repo. It is same folder as this script")

#Reading the entire file and printing it as a whole

with open('trial_file.txt','r') as tfile:
    data_is = tfile.read()
    print('Printing the complete file',end='\n')
    print(data_is)

print("File can be read a list of lines.That is why Data Structures are important")

with open("trial_file.txt",'r') as fil:
    data_line = fil.readlines()
    line_num = len(data_line)
    print('Total lines in the file',line_num)
    for line in data_line:
        print(line)
    
print("Will now see writing to files. We will be reusing the data from ds_file.py")

#int/str/float
a = 1
b = 2
c = 'c-letter'
d = 'f-flo'
e = 79
f = 9.85
g = 75.62

#creating list
list1 = [1,2,3,4,5,8,90]
list2 = [a,b,c,d,e,f,g]

print('List 1 is created manually.',list1)
print('List 2 is created using existing variables',list2)

#creating dict
dict1 = {'a':1,'b':75,'k':756,'f':97}
dict_vars = {'a':a, 'b':b,'k':c,'c':c,'d':d}
dict2 = {'list1':list2,'list2':list1}

print('Dict 1 is created manually by entering value', dict1)
print('Dict 2 is created using existing list of vars',dict2)
print('dict_vars is created using existing vars',dict_vars)

#creating set
set1 = set(list1)
set2 = set(['a','f','e','a',1,5,78,98,565])

list_complex = [list2, list1, dict1, dict2,set1,set2]

print("Set 1 is A simple set", set1)
print("Set 2 is mix of variable types",set2)
print("Sets of list or dict is not possible, since they cannot be hashed")
print("List_complex is mix of data structures",list_complex)

print("The above printed files will all be written inside the output_file.txt")

with open('output_file.txt','w') as w_f:
    w_f.write("This file is written by the script... \n")
    w_f.write("Starting to write the lists \n")

    w_f.write(f'List 1 is created manually.: {list1} \n')
    w_f.write(f'List 2 is created using existing variables : {list2} \n')

    w_f.write(f'Starting to write the dictionaries')
    w_f.write(f'Dict 1 is created manually by entering value : {dict1} \n')
    w_f.write(f'Dict 2 is created using existing list of vars : {dict2} \n')
    w_f.write(f'dict_vars is created using existing vars :{dict_vars} \n')
    
    w_f.write("Starting to write the sets")
    w_f.write(f"Set 1 is A simple set :{set1} \n")
    w_f.write(f"Set 2 is mix of variable types {set2} \n")
    w_f.write(f"Sets of list or dict is not possible, since they cannot be hashed \n")

    w_f.write(f"List_complex is mix of data structures {list_complex} \n")
   
