# In this play, you move the letter P with the keys w, a, s and d. If you want to color the terminal,
# remove the comment from the lines below.

import os
import time
import random
# from colorama import init, Fore, Back, Style

# init()

points = 0
auxiliar_point = 0
end_of_play = False


def erase_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_play():
    erase_screen()
    for lines in play:
        for element in lines:
            # if element == "P":
              #  print(Fore.GREEN + element + Style.RESET_ALL, end=" ")
            # elif element == "!":
             #   print(Fore.RED + element + Style.RESET_ALL, end=" ")
            # elif element == "*":
             #   print(Fore.YELLOW + element + Style.RESET_ALL, end=" ")
            # else:
            print(element, end=" ")
        print()
    print(f"Points: {points}")
    print("Instructions: You are player P; collect the *s and dodge the !s. Press q to quit, w, a, s and d to move")


def end_play():
    for k in play:
        for p in k:
            if p == "P":
                return False
    return True


def add_point():
    for i in play:
        for o in i:
            if o == "*":
                return False
    return True


# Initial play:
coluns_number = 10
lines_number = 7
play = [["." for _ in range(coluns_number)] for _ in range(lines_number)]
level_up = 4

index_player_x = 0
index_player_y = 0
play[index_player_x][index_player_y] = "P"

enemys = [{"x": lines_number-1, "y": coluns_number-1}]
play[lines_number-1][coluns_number-1] = "!"

index_fruit_x = random.choice([i for i in range(0, lines_number) if i != index_player_x])
index_fruit_y = random.choice([i for i in range(0, coluns_number) if i != index_player_y])
play[index_fruit_x][index_fruit_y] = "*"

print_play()

while not end_of_play:
    key = input("Digit your next movement: ")
    if key == "d":
        play[index_player_x][index_player_y] = "."
        index_player_y += 1
        if index_player_y == coluns_number:
            index_player_y -= 1

    elif key == "a":
        play[index_player_x][index_player_y] = "."
        index_player_y -= 1
        if index_player_y == -1:
            index_player_y += 1

    elif key == "w":
        play[index_player_x][index_player_y] = "."
        index_player_x -= 1
        if index_player_x == -1:
            index_player_x += 1

    if key == "s":
        play[index_player_x][index_player_y] = "."
        index_player_x += 1
        if index_player_x == lines_number:
            index_player_x -= 1
    play[index_player_x][index_player_y] = "P"

    if key == "s" or key == "w" or key == "a" or key == "d":
        for enemy in enemys:
            play[enemy["x"]][enemy["y"]] = "."
            direction = random.randint(1, 4)
            if direction == 1:
                enemy["y"] += 1
                if enemy["y"] >= coluns_number:
                    enemy["y"] -= 2
            elif direction == 2:
                enemy["y"] -= 1
                if enemy["y"] <= 0:
                    enemy["y"] += 2
            elif direction == 3:
                enemy["x"] -= 1
                if enemy["x"] <= 0:
                    enemy["x"] += 2
            elif direction == 4:
                enemy["x"] += 1
                if enemy["x"] >= lines_number:
                    enemy["x"] -= 2
            if play[enemy["x"]][enemy["y"]] == "*":
                if index_fruit_x == 0:
                    index_fruit_x += 1
                else:
                    index_fruit_x -= 1
                play[index_fruit_x][index_fruit_y] = "*"
            play[enemy["x"]][enemy["y"]] = "!"
        erase_screen()
        print_play()
        time.sleep(0.1)

    if key == "q" or end_play():
        print(f"Game over: you ended up with {points} points")
        end_of_play = True
    if points % level_up == 0 and points != 0 and points != auxiliar_point:
        auxiliar_point = points
        enemys.append({"x": lines_number-1, "y": coluns_number-1})
        play[enemys[-1]["x"]][enemys[-1]["y"]] = "!"
    if add_point():
        points += 1
        boolean = True
        while boolean:
            index_fruit_x = random.randint(0, lines_number - 1)
            index_fruit_y = random.randint(0, coluns_number - 1)
            if play[index_fruit_x][index_fruit_y] == ".":
                boolean = False
        play[index_fruit_x][index_fruit_y] = "*"
