import math
import turtle
from random import randint

window = turtle.Screen()
window.setup(900, 600)
window.bgpic('images/background.png')

BASE_X, BASE_Y = 0, -230


def calc_lenght(x, y, x1, y1):
    dx = x1 - x
    dy = y1 - y
    lenght = (dx ** 2 + dy ** 2) ** 0.5
    cos_alpha = dx / lenght
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy < 0:
        alpha = -alpha
    return alpha


def create_missile(side, x, y, x1, y1):
    missile = turtle.Turtle(visible=False)
    if side == "our":
        missile.color('white')
    elif side == "enemy":
        missile.color('red')
    missile.penup()
    missile.setpos(x, y)
    missile.pendown()
    lenght = missile.towards(x1, y1)
    missile.setheading(lenght)
    missile.showturtle()
    info = {"missile": missile,
            "target": [x1, y1],
            "status": "launched"}
    missiles.append(info)


def enemy_missile():
    start_x = randint(-400, 400)
    start_y = 300
    # missile = turtle.Turtle(visible=False)
    # missile.color('red')
    # missile.penup()
    # missile.setpos(start_x, start_y)
    # missile.pendown()
    # lenght = missile.towards(x=BASE_X, y=BASE_Y)
    # missile.setheading(lenght)
    # missile.showturtle()
    # info = {"missile": missile,
    #         "target": [BASE_X, BASE_Y],
    #         "status": "launched"}
    # missiles.append(info)
    create_missile("enemy", start_x, start_y, BASE_X, BASE_Y)


def our_missile(x, y):
    # missile = turtle.Turtle(visible=False)
    # missile.color('white')
    # missile.penup()
    # missile.setpos(BASE_X, BASE_Y)
    # missile.pendown()
    # lenght = calc_lenght(BASE_X, BASE_Y, x, y)
    # missile.setheading(lenght)
    # missile.showturtle()
    # info = {"missile": missile,
    #         "target": [x, y],
    #         "status": "launched"}
    # missiles.append(info)
    create_missile("our", BASE_X, BASE_Y, x, y)


def launch(missiles):
    for info in missiles:
        missile = info["missile"]
        status = info["status"]
        if status == "launched":
            missile.forward(4)
            target = info["target"]
            if missile.distance(x=target[0], y=target[1]) < 10:
                info["status"] = "explode"
                missile.shape('circle')
        elif status == "explode":
            missile.clear()
            missile.hideturtle()
            info["status"] = "dead"

    dead_missiles = [i for i in missiles if i["status"] == "dead"]
    for dead in dead_missiles:
        missiles.remove(dead)


window.onclick(our_missile)

missiles = []

while True:
    window.update()
    # for info in our_missiles:
    #     missile = info["missile"]
    #     status = info["status"]
    #     if status == "launched":
    #         missile.forward(10)
    #         target = info["target"]
    #         if missile.distance(x=target[0], y=target[1]) < 20:
    #             info["status"] = "explode"
    #             missile.shape('circle')
    #     elif status == "explode":
    #         missile.clear()
    #         missile.hideturtle()
    #         info["status"] = "dead"
    #
    # dead_missiles = [i for i in our_missiles if i["status"] == "dead"]
    # for dead in dead_missiles:
    #     our_missiles.remove(dead)
    on_fire = randint(1, 100)
    if on_fire == 5:
        enemy_missile()
    launch(missiles)
