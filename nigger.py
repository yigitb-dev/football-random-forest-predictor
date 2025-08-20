import random
door1 = False 
door2 = False
door3 = False
found_door = False
doors = [1, 2, 3]

x = int(input("Enter a number: "))

for i in range(x):
    selected_door = random.choice(doors)
    guess = random.choice(doors)
    if guess == selected_door:
        found_door = True
    
    if guess != selected_door:
        remove_door = random.choice(doors)
        



    