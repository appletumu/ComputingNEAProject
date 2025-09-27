import random

items = input("Enter items separated by commas: ").split(', ')
randomised_items = []
change_pos = []

i = 0
for i in range(len(items)):
    possible_pos = random.randint(0, len(items)-1)
    
    if possible_pos in change_pos:
        continue

    change_pos.append(possible_pos)
    i += 1

for item in items:
    randomised_items.append(items[change_pos[len(randomised_items)]])

print(randomised_items)