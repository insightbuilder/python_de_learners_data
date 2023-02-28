#!/usr/bin/env python

'''The script will print the various data structures...'''

#First the variables are created

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

