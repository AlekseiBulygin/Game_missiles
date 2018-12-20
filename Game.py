import math
import turtle
from random import randint

window = turtle.Screen()
window.setup(900, 600)
window.bgpic('images/background.png')
#window.tracer(n=2)

BASE_X, BASE_Y = 0, -230
base = turtle.Turtle(visible=False)

def create_missile(color, x, y, x1, y1):
    missile = turtle.Turtle(visible=False)
    missile.color(color)
    missile.penup()
    missile.setpos(x, y)
    missile.pendown()
    lenght = missile.towards(x1, y1)
    missile.setheading(lenght)
    missile.showturtle()
    info = {"missile": missile,
            "target": [x1, y1],
            "status": "launched",
            "radius": 0}
    return info


def enemy_missile():
    start_x = randint(-400, 400)
    start_y = 300
    info = create_missile("red", start_x, start_y, BASE_X, BASE_Y)
    enemy_missiles.append(info)


def our_missile(x, y):
    info = create_missile("white", BASE_X, BASE_Y, x, y)
    our_missiles.append(info)


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
            info["radius"] += 1
            if info["radius"] > 3:
                missile.clear()
                missile.hideturtle()
                info["status"] = "dead"
            else:
                missile.shapesize(info["radius"])
        elif status == "dead":
            missile.clear()
            missile.hideturtle()

    dead_missiles = [i for i in missiles if i["status"] == "dead"]
    for dead in dead_missiles:
        missiles.remove(dead)


def count_enemy_missiles():
    if len(enemy_missiles) < 5:
        enemy_missile()


def intercept_missile():
    for our_info in our_missiles:
        if our_info["status"] != "explode":   # intercept missile in explode
            continue
        our_missile = our_info["missile"]
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info["missile"]
            if enemy_missile.distance(our_missile.xcor(), our_missile.ycor()) < our_info["radius"] * 10:
                enemy_info["status"] = "dead"


window.onclick(our_missile)

our_missiles = []
enemy_missiles = []

while True:
    window.update()
    intercept_missile()
    count_enemy_missiles()
    launch(enemy_missiles)
    launch(our_missiles)
