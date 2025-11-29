import random

def randomise(items):
    while True:
        shuffled = items[:]
        random.shuffle(shuffled)
        if all(a != b for a, b in zip(items, shuffled)):
            return shuffled

items = input("Enter items separated by commas: ").split(', ')
result = randomise(items)
print(result)