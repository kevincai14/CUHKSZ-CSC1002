import turtle


def creat_game():
    global column, game_base
    column = []  # a list that include all the Token Placeholder
    n = 0   # counter for confirm the Token Placeholder's position

    for i in range(8):
        i = turtle.Turtle('square')  # create the Token Placeholder
        column.append(i)
        i.up()
        i.shapesize(0.75, 2.5, 4)   # confirm the size
        i.goto(35 + 60 * n, 27.5)   # move the Token Placeholder to the right place
        n += 1

    game_base = []  # create a chessboard in list form
    for i in range(8):
        game_base.append([0, 0, 0, 0, 0, 0, 0, 0])


def add_token(player, column, game):    # add token to the chessboard in list form
    row = 1
    for i in game:  # travel the chessboard
        if i[column - 1] != 0:  # check whether the place is blank
            row += 1
            continue
        else:
            i[column - 1] = player  # add token
            break

    if row == 9:    # check whether the column is full to add token
        return False
    else:
        return [game, [column, row]]


def check_game(game, last_put_position):
    x = last_put_position[0]    # the position that last token wad dropped
    y = last_put_position[1]
    player = game[y - 1][x - 1]  # confirm which player is now playing

    # to check whether the same row has connect-4
    counter = 0
    active_position = []    # the list that include connect-4 position
    active_x = 1
    for i in game[y - 1]:
        if counter != 4:
            if i == player:
                counter += 1
                active_position.append([active_x, y])
            else:   # once there is different value, the counter become 0
                counter = 0
                active_position = []
        active_x += 1
    if counter == 4:    # the counter = 4 means that there are connect-4
        return active_position

    # to check whether the same column has connect-4, similar as above
    counter = 0
    active_position = []
    active_y = 1
    for i in game:
        if counter != 4:
            if i[x - 1] == player:
                counter += 1
                active_position.append([x, active_y])
            else:
                counter = 0
                active_position = []
        active_y += 1
    if counter == 4:
        return active_position

    # to check whether the diagonal has connect-4, both left and right
    diagonal_1 = []  # left-bottom to right-top
    diagonal_2 = []  # left-top to right-bottom
    all_position_1 = []  # a list that include all the position in that diagonal
    all_position_2 = []
    n = -8  # counter for travel

    while True:  # add position in that diagonal to the list
        if x + n in range(0, 8) and y + n in range(0, 8):
            diagonal_1.append(game[y + n][x + n])
            all_position_1.append([x + n + 1, y + n + 1])
        if x + n in range(0, 9) and y - n in range(0, 9):
            diagonal_2.append(game[y - n - 1][x + n - 1])
            all_position_2.append([x + n, y - n])
        if n == 8:
            break
        n += 1

    check_list = [diagonal_1, diagonal_2]
    all_position = [all_position_1, all_position_2]
    active_position = []
    turn = 0    # counter for travel
    for diagonal in check_list:  # to check whether the diagonal has connect-4, both left and right
        counter = 0
        n = 0
        for i in diagonal:
            if counter != 4:
                if i == player:
                    counter += 1
                    active_position.append(all_position[turn][n])   # add position to active position
                else:
                    counter = 0
                    active_position = []
            n += 1
            if counter == 4:
                return active_position
        turn += 1

    # to check whether the game is tied
    counter = 0
    for i in game:
        for k in i:
            if k == 0:
                counter += 1
    if counter == 0:
        return False


def onMouseMotion(event):  # to trace the Mouse Motion
    global g_x
    x, y = event.x, event.y
    g_x = x


def checkcolumn():  # to check if the mouse is on the Token Placeholder and change its color
    for i in column:
        x = i.xcor()
        if abs(g_x - x) <= 25:  # check if it is on the Token Placeholder
            i.color(color_now, i.color()[1])
        else:
            i.color(i.color()[1])

    game.ontimer(checkcolumn, 10)   # timer for check
    return


def check_player():  # to check who is playing the game now
    global player
    if color_now == 'purple':
        player = 1
    else:
        player = 2


def add_token_turtle(position, color_now):  # add the token in turtle form
    global used_position
    x = 35 + (position[0] - 1) * 60  # to ensure where the token is dropped
    y = 75 + (position[1] - 1) * 50

    s = turtle.Screen()
    s.tracer(0)  # turn off the refresh

    t = turtle.Turtle('circle')  # create the token
    t.color(color_now)  # set the color
    t.shapesize(2, 2, 3)    # set token size
    t.up()
    t.goto(x, y)    # drop to the position
    s.update()
    s.tracer(1)  # refresh the screen

    used_position[str(position)] = t    # add the turtle of token into a dictionary for finding later

    s.onclick(onMouseClick)  # recall the click function


def onMouseClick(x, y):
    global color_now
    n = 1
    for i in column:    # to check which column is clicked
        c_x = i.xcor()
        if abs(c_x - x) <= 30:
            add_column = n
        n += 1

    check_player()  # check who is playing now
    state = add_token(player, add_column, game_base)    # add the token in list form
    position = state[1]  # confirm where to drop the token

    if state != False:  # print the chessboard in console
        for i in range(8):
            print(game_base[-1 - i])
        print('')

        add_token_turtle(position, color_now)

    check_data = check_game(game_base, position)    # check the game which player has won the game or not and game tied
    if check_data != None:  # the game finish, someone win or the game tied
        if check_data == False:
            game.title('Game tied!')
            game.onscreenclick(None)  # ban the mouse click
        else:
            for i in check_data:
                used_position.get(str(i)).color('red', color_now)   # mark out the token that has connect-4
                game.title('The ' + color_now + ' player win!')  # change the title
                game.onscreenclick(None)  # ban the mouse click
    else:   # the game go on, change the player
        if color_now == 'blue':
            color_now = 'purple'
        else:
            color_now = 'blue'

        game.title('Now is ' + color_now + ' playper turn!')  # change the title


if __name__ == '__main__':  # main part of the game
    game_state = 0
    game = turtle.Screen()  # create the turtle
    game.setup(500, 450)
    game.setworldcoordinates(0, 0, 500, 450)
    game.title('The purple turn first!')
    color_now = 'purple'
    used_position = {}  # create dictionary for find token

    creat_game()    # create the game
    c = game.getcanvas()
    game.ontimer(checkcolumn, 500)  # timer for check the column

    game.onclick(onMouseClick)   # check the mouse click
    c.bind('<Motion>', onMouseMotion)

    game.mainloop()
