import random


# set the keys to control the game
def key_set():
    # check the input
    while True:
        key_set = input(
            'Enter the four letters used for left, right, up and down move, enter each letter with a space:')
        print('')
        correct_counter = 0
        space_counter = 0
        used_key = []

        for i in range(0, len(key_set), 2):
            # check whether there is repeated letter or not
            if key_set[i] in used_key:
                break
            used_key.append(key_set[i])

            # check whether the input is letter or not by ASCII code
            if ord(key_set[i]) >= 65 and ord(key_set[i]) <= 90:  # check upper letter
                correct_counter += 1
            if ord(key_set[i]) >= 97 and ord(key_set[i]) <= 122:  # check lower letter
                correct_counter += 1

        # check the format of space
        for i in range(1, len(key_set), 2):
            if ord(key_set[i]) == 32:
                space_counter += 1
            else:
                space_counter -= 1

        # check the whole input
        if correct_counter == 4 and space_counter == 3:
            break
        else:  # output message about the false
            print('You input the wrong keys!')
            print('The right format: e.g: left-a, right-d, up-w, down-s --> a d w s')
            print('')

    # add the set key to the key dictionary, both upper and lower letter
    key = {}
    key[key_set[0].lower()] = 'left'
    key[key_set[0].upper()] = 'left'
    key[key_set[2].lower()] = 'right'
    key[key_set[2].upper()] = 'right'
    key[key_set[4].lower()] = 'up'
    key[key_set[4].upper()] = 'up'
    key[key_set[6].lower()] = 'down'
    key[key_set[6].upper()] = 'down'
    key['left'] = key_set[0]
    key['right'] = key_set[2]
    key['up'] = key_set[4]
    key['down'] = key_set[6]
    # return the dictionary
    return key


# create a puzzle game
def create_game(type):
    if type == '1':
        game = [[1, 2, 3], [4, 5, 6], [7, 8, ' ']]
    if type == '2':
        game = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, ' ']]
    for i in range(100):  # disorder the game for 100 times in random
        valid_move = find_valid_move(game)
        game = move(valid_move[random.randint(0, len(valid_move) - 1)], game)
    return game  # return the game


# to print the game
def display_game(game):
    for i in game:
        print(end='\n')
        for k in i:
            print(str(k).ljust(4), end='')
    print(end='\n')


# to find the blank space's position
def find_blank(game):
    y_position = 0
    for i in game:
        try:
            x_position = i.index(' ')
            break
        except:
            y_position += 1
            continue
    return [x_position, y_position]


# check where can move to the blank space
def find_valid_move(game):
    xy_position = find_blank(game)
    x_position = xy_position[0]
    y_position = xy_position[1]
    valid_move = []
    if x_position + 1 < len(game[0]):
        valid_move.append('left')
    if x_position - 1 >= 0:
        valid_move.append('right')
    if y_position + 1 < len(game):
        valid_move.append('up')
    if y_position - 1 >= 0:
        valid_move.append('down')
    return valid_move  # return the list of where can move


# check whether the puzzle is solved
def check_game(game):
    if game == [[1, 2, 3], [4, 5, 6], [7, 8, ' ']]:
        return True
    if game == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, ' ']]:
        return True
    else:
        return False


# a function used to move the numbers to the blank space
def move(direction, game):
    bank_position = find_blank(game)
    x = bank_position[0]
    y = bank_position[1]
    if direction == 'right':
        game[y][x] = game[y][x - 1]
        game[y][x - 1] = ' '
    if direction == 'left':
        game[y][x] = game[y][x + 1]
        game[y][x + 1] = ' '
    if direction == 'up':
        game[y][x] = game[y + 1][x]
        game[y + 1][x] = ' '
    if direction == 'down':
        game[y][x] = game[y - 1][x]
        game[y - 1][x] = ' '
    return game


# the main part of the puzzle game
def game_main():
    while True:  # determine the 8 or 15 puzzle or quit the game
        state = input('Enter “1” for 8-puzzle, “2” for 15-puzzle or “q” to end the game:')
        if state == 'q':
            print('The game is over! Good bye and have a nice day!')
            quit(0)
        elif state == '1' or state == '2':
            break
        else:
            print('Please enter "1", "2" or "q"!')

    game = create_game(state)
    counter = 0
    game_state = check_game(game)

    # start the game
    while game_state == False:
        display_game(game)  # display the game
        valid_move = find_valid_move(game)  # find valid move

        # generate prompt text
        text = 'Enter your move ('
        valid_key = []
        for i in valid_move:
            valid_key.append(key[i].lower())
            valid_key.append(key[i].upper())
            i += '-' + key[i]
            text += i + ', '
        text = text[0:-2]
        text += '):'

        # check user's input
        while True:
            user_input = input(text)
            if user_input not in valid_key:
                print('Please input the valid move!')
            else:
                break

        # move the numbers to the blank space
        next_move = key[user_input]
        game = move(next_move, game)

        # count the steps
        counter += 1

        # check whether the game is solved or not
        game_state = check_game(game)
    display_game(game)
    print('Congratulations! You solved the puzzle in ' + str(counter) + ' moves!')
    print('')


# the main part
if __name__ == '__main__':
    print('Welcome to Kinley’s puzzle game! You will be prompted to solve the Sliding Puzzle!')
    key = key_set()
    while True:
        game_main()