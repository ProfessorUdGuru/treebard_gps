# convert_numbered_lines_to_nested_dict_re_gedcom
# https://stackoverflow.com/questions/24975310/python-nested-dictionary-with-arbitrary-number-of-levels

import dev_tools as dt
from dev_tools import looky, seeline

# input: 
'''
[
    [1, 'NAME', 'David /Todd/'], 
    [2, 'SOUR', '@S2@'], 
    [3, 'PAGE', 'page 2'], 
    [1, 'SEX', 'M'], 
    [1, 'RESI'], 
    [2, 'DATE', '1962'], 
    [2, 'PLAC', 'Meridian'], 
    [2, 'SOUR', '@S2@'], 
    [3, 'PAGE', 'page 2'], 
    [1, 'RESI'], 
    [2, 'DATE', '1962'], 
    [2, 'PLAC', 'Gulfport'], 
    [2, 'SOUR', '@S2@'], 
    [3, 'PAGE', 'page 2'], 
    [1, 'RESI'], 
    [2, 'DATE', '1985'], 
    [1, 'CHAN'], 
    [2, 'DATE', '17 AUG 2015'], 
    [3, 'TIME', '20:56:36']]

output goal:  [
{'NAME': {
    'David /Todd/': {
        'SOUR': {
            '@S2@': {
                'PAGE': 'page 2'}}}}},
{'SEX': 'M'}] etc...
'''
# EXAMPLE 1 FROM STACK OVERFLOW DLunin:

lst1 = ['big', 'red', 'fat', 'smelly', 'hairy', 'noisy', 'dog']

def nested_dict1(lst1, value='Fido'):
    if len(lst1) == 1:
        return {lst1[0]: value}
    return {lst1[0]: nested_dict1(lst1[1:], value=value)}

print(nested_dict1(lst1))
# {'big': {'red': {'dog': 'Fido'}}}

# EXAMPLE 2 GET THE INNERMOST VALUE FROM THE LIST
lst2 = ['little', 'black', 'fat', 'smelly', 'hairy', 'noisy', 'dog', 'Silly Sally']

value2 = lst2[len(lst2) - 1]

def nested_dict2(lst2):
    if len(lst2) == 2:

        return {lst2[0]: value2}
    return {lst2[0]: nested_dict2(lst2[1:])}
print(nested_dict2(lst2))

# # EXAMPLE 3 USE A LIST OF LISTS

# lst3 = [[0, 'little'], [1, 'black'], [2, 'fat'], [1, 'smelly'], [1, 'hairy'], [1, 'noisy'], [2, 'dog'], [3, 'Silly Sally']]

# value3 = lst3[len(lst3) - 1][1]

# def nested_dict2(lst3):
    # if len(lst3) == 2:
        # return {lst3[0]: value3}
    # return {lst3[0][1]: nested_dict2(lst3[1:][1])}
# print(nested_dict2(lst3))

# EXAMPLE 3 NON-RECURSIVE VERSION

t = ('cat','dog','bone')
answer = {}
temp = answer
for key in t[0:-1]:
    if key not in temp:
        temp[key] = {}
    temp = temp[key]
temp[t[-1]] = 10
print(answer)
# {'cat': {'dog': {'bone': 10}}}

# EXAMPLE 4 GET INNER VALUE FROM LIST

t = ('cat','dog','bone', 10)
answer4 = {}
temp4 = answer4
for key in t[0:-2]:
    if key not in temp4:
        temp4[key] = {}
    temp4 = temp4[key]
temp4[t[-2]] = t[-1]
print(answer4)
# {'cat': {'dog': {'bone': 10}}}

# EXAMPLE 5 GET INNER VALUE FROM FRONT OF LIST

t = (3, 'cat','dog','bone')
answer5 = {}
temp5 = answer5
for key in t[1:-1]:
    if key not in temp5:
        temp5[key] = {}
    temp5 = temp5[key]
temp5[t[-1]] = t[0]
print(answer5)
# {'cat': {'dog': {'bone': 3}}}

# EXAMPLE 6 IGNORE VALUE AT FRONT OF LIST

t = (3, 'fruit', 'cat','dog','bone')
answer6 = {}
temp6 = answer6
for key in t[1:-2]:
    if key not in temp6:
        temp6[key] = {}
    temp6 = temp6[key]
temp6[t[-2]] = t[-1]
print(answer6)

# EXAMPLE 7 USE A LIST OF LISTS

t = ([0, 'fruit'], [1, 'cat'], [0, 'dog'],[0, 'bone'])
answer7 = {}
temp7 = answer7
for lst in t[0:-2]:
    key = lst[1]
    if key not in temp7:
        temp7[key] = {}
    temp7 = temp7[key]
temp7[t[-2][1]] = t[-1][1]
print(answer7)

# EXAMPLE 8 GET NESTING LEVEL FROM LIST

t = (
    [0, 'fruit'], [1, 'cat'], [0, 'dog'],[0, 'bone'], [1, 'cow'], 
    [2, 'horse'], [3, 'frog'], [0, 'tiger'])

answer8 = {}
temp8 = answer8
for lst in t[0:-2]:
    key = lst[1]
    level = lst[0]
    temp8[t[level][1]] = {}
    temp8 = temp8[t[level][1]]
temp8[t[-2][1]] = t[-1][1]
print(answer8)
# {'fruit': {'cat': {'fruit': {'fruit': {'cat': {'dog': {'frog': 'tiger'}}}}}}}





