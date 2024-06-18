import turtle
import random
from functools import partial

g_screen = None
g_snake = None
g_monster = None
g_snake_sz = 10
g_intro = None
g_keypressed = None
g_status = None

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT = ("Arial",16,"normal")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP:90, KEY_DOWN:270, KEY_LEFT:180, KEY_RIGHT:0}

def configurePlayArea():

    # motion border
    m = createTurtle(0,0,"","black")
    m.shapesize(25,25,5)
    m.goto(0,-40)  # shift down half the status

    # status border 
    s = createTurtle(0,0,"","black")
    s.shapesize(4,25,5)
    s.goto(0,250)  # shift up half the motion

    # introduction
    intro = createTurtle(-200,150)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial",16,"normal"))
    
    # statuses
    status = createTurtle(0,0,"","black")
    status.hideturtle()
    status.goto(-200,s.ycor()) 

    return intro, status

def configScreen():
    s = turtle.Screen()
    s.tracer(0)    # disable auto screen refresh, 0=disable, 1=enable
    s.title("Snake by Kinley Lam")
    s.setup(500+120, 500+120+80)
    s.mode("standard")
    return s

def createTurtle(x, y, color="red", border="black"):
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x,y)
    return t

def updateStatus():
    g_status.clear()
    g_status.write(g_keypressed, font=('arial',15,'bold'))
    g_screen.update()

def setSnakeHeading(key):
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading( HEADING_BY_KEY[key] )

def onArrowKeyPressed(key):
    global g_keypressed
    g_keypressed = key
    setSnakeHeading(key)
    updateStatus()
    
def onTimerSnake():
    print('onTimerSnake')

    if g_keypressed == None:
        g_screen.ontimer(onTimerSnake, 200)
        return

    # Clone the head as body
    g_snake.color(*COLOR_BODY)
    g_snake.stamp()
    g_snake.color(COLOR_HEAD)

    # Advance snake
    g_snake.forward(20)

    # Shifting or extending the tail.
    # Remove the last square on Shifting.
    if len(g_snake.stampItems) > g_snake_sz:
        g_snake.clearstamps(1)
    
    g_screen.update()

    g_screen.ontimer(onTimerSnake, 200)


def onTimerMonster():
    print('onTimerMonster')
    dir = list(range(0,360,90))
    random.shuffle(dir)
    g_monster.setheading(dir[0])
    g_monster.forward(20)
    
    g_screen.update()
    g_screen.ontimer(onTimerMonster, 1000)


def startGame(x,y):
    g_screen.onscreenclick(None)
    g_intro.clear()

    g_screen.onkey(partial(onArrowKeyPressed,KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_RIGHT), KEY_RIGHT)

    g_screen.ontimer(onTimerSnake, 100)
    g_screen.ontimer(onTimerMonster, 1000)

if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status = configurePlayArea()
    
    updateStatus()

    g_monster = createTurtle(-110,-110,"purple", "black")
    g_snake = createTurtle(0,0,"red", "black")

    g_screen.onscreenclick(startGame)

    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()