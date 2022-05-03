# convert_numbered_lines_to_list_of_dicts_re_gedcom
import dev_tools as dt
from dev_tools import looky, seeline



# {'@I4@': [[1, 'NAME', 'David /Todd/'], [2, 'SOUR', '@S2@'], [3, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary'], [1, 'SEX', 'M'], [1, 'RESI'], [2, 'DATE', '1962'], [2, 'PLAC', 'Meridian, Lauderdale County, Mississippi'], [2, 'SOUR', '@S2@'], [3, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary'], [1, 'RESI'], [2, 'DATE', '1962'], [2, 'PLAC', 'Gulfport, Harrison County, Mississippi'], [2, 'SOUR', '@S2@'], [3, 'PAGE', '26 June 1962, page 2, obituary, "Mrs. Lora Grace Smith"'], [1, 'RESI'], [2, 'DATE', '1985'], [2, 'PLAC', 'Gulfport, Harrison County, Mississippi'], [2, 'SOUR', '@S3@'], [3, 'PAGE', '"MRS. NORA NAOMI TODD", obituary, date and place of publication unknown'], [2, 'SOUR', '@S4@'], [3, 'PAGE', 'findagrave member no. 48611078'], [1, 'FAMC', '@F2@'], [1, 'SOUR', '@S2@'], [2, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary'], [1, 'CHAN'], [2, 'DATE', '17 AUG 2015'], [3, 'TIME', '20:56:36']], '@I5@': [...]...}

# input: 

record = [
    [1, 'NAME', 'David /Todd/'], 
    [2, 'SOUR', '@S2@'], 
    [3, 'PAGE', 'page 2'], 
    [1, 'SEX', 'M'], 
    [1, 'RESI'], 
    [2, 'DATE', '1962'], 
    [2, 'PLAC', 'Meridian'], 
    [2, 'SOUR', '@S3@'], 
    [3, 'PAGE', 'page 3'], 
    [1, 'RESI'], 
    [2, 'DATE', '1962'], 
    [2, 'PLAC', 'Gulfport'], 
    [2, 'SOUR', '@S4@'], 
    [3, 'PAGE', 'page 4'], 
    [1, 'RESI'], 
    [2, 'DATE', '1985'], 
    [1, 'CHAN'], 
    [2, 'DATE', '17 AUG 2015'], 
    [3, 'TIME', '20:56:36']]
'''
output goal: [
    
]


output goal:  [
{'NAME': {
    'David /Todd/': {
        'SOUR': {
            '@S2@': {
                'PAGE': 'page 2'}}}}},
{'SEX': 'M'}] etc...
'''
# EXAMPLE 1 :

levels = [i[0] for i in record]
print("line", looky(seeline()).lineno, "levels:", levels)

unique_levels = list(set(levels))
print("line", looky(seeline()).lineno, "unique_levels:", unique_levels)

levels_dict = {}

for x in unique_levels:
    count = levels.count(x)
    print("line", looky(seeline()).lineno, "x, count:", x, count)
    levels_dict[x] = count
print("line", looky(seeline()).lineno, "levels_dict:", levels_dict)

# line 52 levels_dict: {1: 6, 2: 9, 3: 4}

for k,v in levels_dict.items():
    if k == 1:
        lst = []
        outer_list = [lst] * v
        break

# print("line", looky(seeline()).lineno, "outer_list:", outer_list)
# line 69 outer_list: [[], [], [], [], [], []]

outer = []

def add_subrecords():

    current_nest = -1
    for lst in record:    
        n = lst[0]
        data = lst[1:]
        print("line", looky(seeline()).lineno, "n, data:", n, data)
        if n == 1:  
            current_nest += 1     
            print("line", looky(seeline()).lineno, "current_nest:", current_nest)
            # outer_list[current_nest].append(data)
            outer.append([data])
        else:
            pass
            # print("line", looky(seeline()).lineno, "current_nest:", current_nest)
            # outer_list[current_nest].append(data)
    print("line", looky(seeline()).lineno, "outer:", outer)
# line 90 outer: [
# [['NAME', 'David /Todd/']], 
# [['SEX', 'M']], 
# [['RESI']], 
# [['RESI']], 
# [['RESI']], 
# [['CHAN']]]

    subrecords = []
    x = -1
    for lst in record:
        n = lst[0]
        data = lst[1:]
        if n == 1:
            x += 1
        elif n != 2:
            continue
        else:
            print("line", looky(seeline()).lineno, "n, data, subrecords:", n, data, subrecords)
            subrecords.append(data)
            outer[x].append(list(subrecords))
            subrecords = []
            
            

        
            
    # print("line", looky(seeline()).lineno, "outer_list:", outer_list)

add_subrecords()
    





# DO LIST

#




