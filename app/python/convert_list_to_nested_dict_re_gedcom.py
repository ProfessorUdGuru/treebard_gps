# convert_list_to_nested_dict


import dev_tools as dt
from dev_tools import looky, seeline



head_list = [
	[1, 'SOUR', 'FAMILY_HISTORIAN'], 
	[2, 'VERS', '6.2.6'], 
	[2, 'NAME', 'Family Historian'], 
	[2, 'CORP', 'Calico Pie Limited'], 
	[1, 'FILE', 'D:\\genealogy databases\\gedcom files\\todd_boyett_connections.ged'], 
	[1, 'GEDC'], 
	[2, 'VERS', '5.5'], 
	[2, 'FORM', 'LINEAGE-LINKED'], 
	[1, 'CHAR', 'UTF-8']
]

# goal = {'SOUR': {'VERS': '6.2.6', 'NAME': 'Genbox Blah', 'CORP': 'Unlimited'}, 'FILE': 'd:/blah', 'GEDC': '5.5', 'CHAR': 'UTF-8'}

dkt = {'SOUR': {'VERS': '', 'NAME': '', 'CORP': ''}, 'FILE': '', 'GEDC': '', 'CHAR': ''}

def get_value(lst, x, tag):
    value = None
    w = x + 1
    for lst in head_list[w:]:
        if lst[1] == tag:
            value = lst[2]
            break
        w += 1
    return value

def parse_head(head_list):
    x = 0
    for lst in head_list:
        n = lst[0] 
        if n != 1:
            x += 1
            continue
        else:
            tag = lst[1]
            if tag == 'SOUR':
                for tagg in ('VERS', 'NAME', 'CORP'):
                    dkt[tag][tagg] = get_value(lst, x, tagg)
            elif tag == 'GEDC':
                dkt[tag] = get_value(lst, x, 'VERS')
            elif tag in ('FILE', 'CHAR'):
                dkt[tag] = lst[2]
            x += 1

parse_head(head_list)


print("line", looky(seeline()).lineno, "dkt:", dkt)
                

