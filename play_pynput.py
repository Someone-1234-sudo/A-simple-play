# In this play with the libraries colorama (to color the terminal)
# and pynput (to move the letter with up, down, left and right keys)


from pynput import keyboard
import os
import time
import random
from colorama import init, Fore, Back, Style, Cursor

init()

score = 0
aux_point = 0
game_over = False

# Movement control variables
moves = {"up": False, "down": False, "left": False, "right": False, "shift": False}


def clear_screen():
    os.system('cls')


def print_game():
    clear_screen()
    for rows in board:
        for cols in rows:
            if cols == "P":
                print(Fore.GREEN + cols + Style.RESET_ALL, end=" ")
            elif cols == "!":
                print(Fore.RED + cols + Style.RESET_ALL, end=" ")
            elif cols == "*":
                print(Fore.YELLOW + cols + Style.RESET_ALL, end=" ")
            else:
                print(cols, end=" ")
        print()
    print(f"Score: {score}")
    print("Instructions: you are player P, collect * and avoid !. Press shift to quit.")


def end_play(tab: list[list]):
    for k in tab:
        for p in k:
            if p == "P":
                return False
    return True


def add_point():
    for i in board:
        for o in i:
            if o == "*":
                return False
    return True

# Keyboard functions


def on_press(key):
    try:
        if key == keyboard.Key.up:
            moves["up"] = True
        elif key == keyboard.Key.down:
            moves["down"] = True
        elif key == keyboard.Key.left:
            moves["left"] = True
        elif key == keyboard.Key.right:
            moves["right"] = True
        elif key == keyboard.Key.shift:
            moves["shift"] = True
    except:
        pass


def on_release(key):
    try:
        if key == keyboard.Key.up:
            moves["up"] = False
        elif key == keyboard.Key.down:
            moves["down"] = False
        elif key == keyboard.Key.left:
            moves["left"] = False
        elif key == keyboard.Key.right:
            moves["right"] = False
        elif key == keyboard.Key.shift:
            moves["shift"] = False
    except:
        pass


# Keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Initial board
num_cols = 10
num_rows = 7
board = [["." for _ in range(num_cols)] for _ in range(num_rows)]
level_up = 4

player_x = 0
player_y = 0
board[player_x][player_y] = "P"

enemies = [{"x": num_rows-1, "y": num_cols-1}]
board[num_rows-1][num_cols-1] = "!"

fruit_x = random.choice([i for i in range(0, num_rows) if i != player_x and i != num_rows-1])
fruit_y = random.choice([i for i in range(0, num_cols) if i != player_y and i != num_cols-1])
board[fruit_x][fruit_y] = "*"

print_game()

while not game_over:
    up, down, right, left, shift = moves["up"], moves["down"], moves["right"], moves["left"], moves["shift"]

    if right:
        board[player_x][player_y] = "."
        player_y += 1
        if player_y == num_cols:
            player_y -= 1

    if left:
        board[player_x][player_y] = "."
        player_y -= 1
        if player_y == -1:
            player_y += 1

    if up:
        board[player_x][player_y] = "."
        player_x -= 1
        if player_x == -1:
            player_x += 1

    if down:
        board[player_x][player_y] = "."
        player_x += 1
        if player_x == num_rows:
            player_x -= 1

    board[player_x][player_y] = "P"

    if up or down or right or left:
        for enemy in enemies:
            board[enemy["x"]][enemy["y"]] = "."
            direction = random.randint(1, 4)
            if direction == 1:
                enemy["y"] += 1
                if enemy["y"] >= num_cols:
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
                if enemy["x"] >= num_rows:
                    enemy["x"] -= 2
            if board[enemy["x"]][enemy["y"]] == "*":
                if fruit_x == 0:
                    fruit_x += 1
                else:
                    fruit_x -= 1
                board[fruit_x][fruit_y] = "*"
            board[enemy["x"]][enemy["y"]] = "!"

        print_game()
        time.sleep(0.1)

    if shift or end_play(board):
        clear_screen()
        print(f"Game over: you scored {score} points.")
        game_over = True
    if score % level_up == 0 and score != 0 and score != aux_point:
        aux_point = score
        enemies.append({"x": num_rows - 1, "y": num_cols - 1})
        board[enemies[-1]["x"]][enemies[-1]["y"]] = "!"
    if add_point():
        score += 1
        boolean = True
        while boolean:
            fruit_x = random.randint(0, num_rows - 1)
            fruit_y = random.randint(0, num_cols - 1)
            if board[fruit_x][fruit_y] == ".":
                boolean = False
        board[fruit_x][fruit_y] = "*"
