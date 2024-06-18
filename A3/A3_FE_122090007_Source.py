import turtle
import random
import time
from functools import partial

g_screen = None  # the screen for game
g_snake = None  # the turtle object of the snake
g_monster = None  # the turtle object of the monster
g_snake_sz = 5  # the initial size of the snake
g_intro = None  # the turtle object of the instruction
g_keypressed = None  # the key that was pressed
g_keypressed_previous = None  # the last key that was pressed
g_status = None  # the turtle object of the motion
g_timer = None  # the turtle object of the timer
g_game_over = False  # the satus whether the snake was caught
g_game_win = False  # the satus whether the game win
start_time = None  # timer for starting the game
pause_state = False  # the satus whether the game paused
snake_body_pos = []  # list for storing the snake body position
food_items = []  # the list store food items
food_items_hide = []  # the list store hidden food items
contact_n = 0  # the counter for counting the contact

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT = ("Arial", 16, "normal")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
    "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


def configurePlayArea():
    # motion border
    m = createTurtle(0, 0, "", "black")
    m.shapesize(25, 25, 5)
    m.goto(0, -40)  # shift down half the status

    # status border
    s = createTurtle(0, 0, "", "black")
    s.shapesize(4, 25, 5)
    s.goto(0, 250)  # shift up half the motion

    # introduction
    intro = createTurtle(-200, 150)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial", 16, "normal"))

    # statuses
    status = createTurtle(0, 0, "", "black")
    status.hideturtle()
    status.goto(100, s.ycor() - 15)

    # timer
    timer = createTurtle(0, 0, "", "black")
    timer.hideturtle()
    timer.goto(-30, s.ycor() - 15)
    timer.write('Time: 0', font=('arial', 15, 'bold'))

    # contact
    contact = createTurtle(0, 0, "", "black")
    contact.hideturtle()
    contact.goto(-200, s.ycor() - 15)
    contact.write('Contact: 0', font=('arial', 15, 'bold'))

    return intro, status, timer, contact


def configScreen():  # set up the game area
    s = turtle.Screen()
    s.tracer(0)  # disable auto screen refresh, 0=disable, 1=enable
    s.title("Snake by Kevin Cai")
    s.setup(500 + 120, 500 + 120 + 80)
    s.mode("standard")
    return s


def createTurtle(x, y, color="red", border="black"):  # create a turtle object
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t


def updateStatus():  # update the motion
    g_status.clear()  # clear the screen
    if g_keypressed != 'space':
        g_status.write('Motion: ' + str(g_keypressed), font=('arial', 15, 'bold'))
        g_screen.update()
    else:
        g_status.write('Motion: Paused', font=('arial', 15, 'bold'))
        g_screen.update()


def setSnakeHeading(key):  # set the heading of the snake by the key pressed
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading(HEADING_BY_KEY[key])


def onArrowKeyPressed(key):  # set up the thing to do after press the key
    global g_keypressed, g_keypressed_previous
    if g_keypressed != 'space':
        g_keypressed_previous = g_keypressed

    if pause_state != True:  # prevent the opposite moving
        if g_keypressed_previous == 'Right' and key == 'Left':
            g_keypressed = 'Right'
        elif g_keypressed_previous == 'Left' and key == 'Right':
            g_keypressed = 'Left'
        elif g_keypressed_previous == 'Up' and key == 'Down':
            g_keypressed = 'Up'
        elif g_keypressed_previous == 'Down' and key == 'Up':
            g_keypressed = 'Down'
        else:
            g_keypressed = key
    else:
        if key == 'space':  # set the head after repressed the space when paused
            g_keypressed = g_keypressed_previous
        else:
            g_keypressed = key

    if g_keypressed == 'space':  # update the motion bar
        updateStatus()
    else:  # update the motion bar
        setSnakeHeading(g_keypressed)
        updateStatus()


def onTimerSnake():
    global pause_state, food_items, g_snake_sz, food_items_hide, g_game_win
    snake_x, snake_y = g_snake.position()
    for i in food_items:  # check whether the snake eat the food
        if round(g_snake.distance(i[0].position())) == 15:
            i[0].clear()
            food_items.remove(i)
            g_snake_sz += i[1]

    if len(food_items) == 0 and len(food_items_hide) == 0:  # check whether all the food are eaten
        g_game_win = True
        turtle.color('red')
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(snake_x - 40, snake_y - 40)
        turtle.write('Winner!!!', font=('arial', 15, 'bold'))
        return

    if g_game_over:  # stop moving after being caught
        return

    if g_keypressed == None:  # keep the direction to move
        g_screen.ontimer(onTimerSnake, 200)
        return

    hit_state = False
    for i in snake_body_pos:  # check whether the snake hit the body
        g_snake.forward(20)
        if round(g_snake.distance(i[0], i[1])) == 0:
            hit_state = True
            g_snake.back(20)
            break
        else:
            g_snake.back(20)
    # check whether the snake is in the game area or not
    if g_keypressed == 'Right' and snake_x + 20 > 241:
        pause_state = True
    elif g_keypressed == 'Left' and snake_x - 20 < -241:
        pause_state = True
    elif g_keypressed == "Up" and snake_y + 20 > 201:
        pause_state = True
    elif g_keypressed == 'Down' and snake_y - 20 < -281:
        pause_state = True
    elif g_keypressed == 'space':
        pause_state = True
    elif hit_state == 1:
        pause_state = True
    else:
        # Clone the head as body
        g_snake.color(*COLOR_BODY)
        g_snake.stamp()
        body_pos = [round(snake_x), round(snake_y)]
        snake_body_pos.append(body_pos)
        g_snake.color(COLOR_HEAD)
        # Advance snake
        pause_state = False
        g_snake.forward(20)

        # Shifting or extending the tail.
        if len(g_snake.stampItems) > g_snake_sz:
            g_snake.clearstamps(1)
            del snake_body_pos[0]  # Remove the last square on Shifting.
        elif len(g_snake.stampItems) <= g_snake_sz and g_snake_sz != 5:  # when start the snake didn't slow down
            g_screen.ontimer(onTimerSnake, 400)  # slow down the snake when growing body
            g_screen.update()
            return
        g_screen.update()
    g_screen.ontimer(onTimerSnake, 200)


def onTimerMonster():
    snake_x, snake_y = g_snake.position()
    if g_game_over:  # show the text when catch the snake
        turtle.color('purple')
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(snake_x - 40, snake_y - 40)
        turtle.write('Game Over!!!', font=('arial', 15, 'bold'))
        return
    if g_game_win:  # stop when the snake eat all food
        return

    monster_heading = g_monster.towards(snake_x, snake_y)  # trace the head of the snake
    for i in [0, 90, 180, 270, 360]:
        if monster_heading - i < 45:  # find which direction should the snake move to
            monster_heading = i
            break

    g_monster.setheading(monster_heading)  # set the snake head
    g_monster.forward(20)  # forward the monster
    g_screen.update()
    g_screen.ontimer(onTimerMonster, random.randint(180, 600))  # move at a random speed


def onTimerCheckGame():
    global g_game_over
    snake_x, snake_y = g_snake.position()
    if g_monster.distance(snake_x, snake_y) < 15:  # check whether the snake has caught the snake
        g_game_over = True
    g_screen.ontimer(onTimerCheckGame, 200)


def timer():  # timer for count the game time
    global start_time
    if g_game_over or g_game_win:
        return
    time_now = int(round(time.time() - start_time, 0))
    g_timer.clear()
    g_timer.write('Time: ' + str(time_now), font=('arial', 15, 'bold'))
    g_screen.update()
    g_screen.ontimer(timer, 1000)


def contact():  # count the times that the monster contact the body
    global contact_n
    if g_game_over:
        return
    for i in snake_body_pos:  # check whether the monster contact the body
        if round(g_monster.distance(i[0], i[1])) == 14:
            contact_n += 1
            break

    g_contact.clear()
    g_contact.write('Contact: ' + str(contact_n), font=('arial', 15, 'bold'))
    g_screen.update()
    g_screen.ontimer(contact, 500)


def food_create():  # create the food
    global food_items
    for i in range(1, 6):  # distribute the food to random position
        x = random.randint(-12, 12) * 20 - 4
        y = random.randint(-15, 9) * 20 + 6

        food = createTurtle(0, 0, "", "black")
        food.hideturtle()
        food.goto(x, y)
        food.write(i, font=('arial', 15, 'bold'))

        food_items.append([food, i])  # add food to the list


def food_hide_and_unhide():  # function for hiding or unhide the food
    global food_items, food_items_hide
    if g_game_win:  # stop when the gamer win
        return

    def hide_food():  # hide the food randomly
        hide_item_index = random.randint(0, len(food_items) - 1)
        food_items[hide_item_index][0].clear()
        food_items_hide.append(food_items.pop(hide_item_index))

    def unhide_food():  # unhide the food randomly
        unhide_item_index = random.randint(0, len(food_items_hide) - 1)
        food_items_hide[unhide_item_index][0].write(food_items_hide[unhide_item_index][1], font=('arial', 15, 'bold'))
        food_items.append(food_items_hide.pop(unhide_item_index))

    mode = random.randint(0, 1)  # choose whether to hide or unhide
    if mode == 0:
        if len(food_items) != 0:
            hide_food()
        else:
            unhide_food()
    elif mode == 1:
        if len(food_items_hide) != 0:
            unhide_food()
        else:
            hide_food()

    g_screen.ontimer(food_hide_and_unhide, random.randint(5000, 10000))


def startGame(x, y):
    global start_time
    g_screen.onscreenclick(None)  # ban the click after game start
    g_intro.clear()  # clear the intro
    start_time = time.time()  # record the start time
    food_create()  # create the food

    g_screen.onkey(partial(onArrowKeyPressed, KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_RIGHT), KEY_RIGHT)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_SPACE), KEY_SPACE)

    g_screen.ontimer(timer, 1000)
    g_screen.ontimer(onTimerSnake, 100)
    g_screen.ontimer(onTimerMonster, 1000)
    g_screen.ontimer(contact, 1000)
    g_screen.ontimer(onTimerCheckGame, 100)
    g_screen.ontimer(food_hide_and_unhide, random.randint(5000, 10000))


if __name__ == "__main__":
    g_screen = configScreen()  # create the game area
    g_intro, g_status, g_timer, g_contact = configurePlayArea()  # create the game area
    updateStatus()

    g_snake = createTurtle(0, 0, "red", "black")  # create the snake

    monster_x = random.randint(-11, 12) * 20 - 10  # randomly pick a position for the monster
    monster_y = random.randint(-13, 10) * 20 - 10
    while g_snake.distance(monster_x, monster_y) < 155:  # keep the monster away from the snake
        monster_x = random.randint(-11, 12) * 20 - 10
        monster_y = random.randint(-13, 10) * 20 - 10
    g_monster = createTurtle(monster_x, monster_y, "purple", "black")  # create the monster

    g_screen.onscreenclick(startGame)  # click to start the game
    g_screen.update()
    g_screen.listen()

    g_screen.mainloop()
