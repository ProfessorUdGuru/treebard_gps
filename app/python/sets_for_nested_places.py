# sets_for_nested_places

x = "114 Main Street, Paris, Lamar County, Texas, USA"
y = "114 Main Street, Paris, Bear Lake County, Idaho, USA"
z = "Paris, Tennessee, USA"

lists = []
for stg in (x, y, z):
    lst = stg.split(", ")
    print(lst)
    lists.append(lst)

l = len(set(lists[0]).intersection(lists[1]))
print(l)
l = len(set(lists[0]).intersection(lists[1], lists[2]))
print(l)

all_place_strings = ["114 Main Street", "Paris", "Lamar County", "Texas", "USA", "Bear Lake County", "Idaho", "Tennessee", "Garfield County", "Colorado", "Aspen", "Pitkin County", "Greece", "Arizona", "Europe", "Antarctica"]

q = ["Paris", "Ile-de-France", "France"]

new_places = set(q).difference(all_place_strings)
print(new_places)

a = ["Maine", "Maine", "USA"]
if len(a) != len(set(a)):
    print("Places with same name in single nesting.")

b = ["Sassari", "Sassari", "Sardegna", "Italy"]
c = ["Sassari", "Sardegna", "Italy"]

print(c in b)
print(c == b[1:])