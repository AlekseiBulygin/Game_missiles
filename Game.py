import turtle
import os
from random import randint

window = turtle.Screen()
window.setup(900, 600)
window.bgpic(os.path.join(os.path.dirname(__file__), 'images', 'background.png'))
window.tracer(n=2)

BASE_X, BASE_Y = 0, -230


class Buildings:
    def __init__(self, x, y, health, pic):
        self.x = x
        self.y = y
        self.health = health
        self.pic = pic
        self.full_health = health
        point = turtle.Turtle()
        point.hideturtle()
        point.penup()
        point.setpos(x, y)
        window.register_shape(os.path.join(os.path.dirname(__file__), 'images', self.pic_object(pic, 0)))
        point.shape(os.path.join(os.path.dirname(__file__), 'images', self.pic_object(pic, 0)))
        point.showturtle()
        self.point = point

    def pic_object(self, name, number):
        our_objects = {"base": ["base.gif", "base.gif", "base.gif"],
                       "kremlin": ["kremlin_1.gif", "kremlin_2.gif", "kremlin_3.gif"],
                       "house": ["house_1.gif", "house_2.gif", "house_3.gif"],
                       "nuclear": ["nuclear_1.gif", "nuclear_2.gif", "nuclear_3.gif"],
                       "skyscraper": ["skyscraper_1.gif", "skyscraper_2.gif", "skyscraper_3.gif"]}
        pic = our_objects[name][number]
        return pic

    def damage_to_buildings(self):
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info["missile"]
            if enemy_info["status"] != "explode":
                continue
            if enemy_missile.distance(self.x, self.y) < enemy_info["radius"] * 10 and \
                    enemy_info["radius"] == 1:
                self.health -= 100
            if self.health < self.full_health / 2:
                window.register_shape(os.path.join(os.path.dirname(__file__), 'images', self.pic_object(self.pic, 1)))
                self.point.shape(os.path.join(os.path.dirname(__file__), 'images', self.pic_object(self.pic, 1)))
            elif self.health < 0:
                window.register_shape(os.path.join(os.path.dirname(__file__), 'images', self.pic_object(self.pic, 2)))
                self.point.shape(os.path.join(os.path.dirname(__file__), 'images', self.pic_object(self.pic, 2)))


buildings = []


def create_buildings():
    buildings_type = ['kremlin', 'nuclear', 'skyscraper', 'house']
    coordinates = [[-350, -230], [-200, -230], [200, -230], [350, -230]]
    health = [4000, 3000, 2000, 1000, 500]
    base = buildings.append(Buildings(x=BASE_X, y=BASE_Y, health=4000, pic='base'))
    for i in range(len(buildings_type)):
        buildings.append(Buildings(x=coordinates[i][0], y=coordinates[i][1], health=health[i], pic=buildings_type[i]))


create_buildings()

class Missile:
    def __init(self, color, x, y, x1, y1):
        self.x = x
        self.y = y
        self.to_x = x1
        self.to_y = y1
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.color(color)
        pen.penup()
        pen.setpos(x, y)
        pen.pendown()
        lenght = pen.towards(x1, y1)
        pen.setheading(lenght)
        pen.showturtle()



def create_missile(color, x, y, x1, y1):
    missile = turtle.Turtle(visible=False)
    missile.color(color)
    # window.register_shape(os.path.join(os.path.dirname(__file__), 'images', 'missile_our.gif'))
    # missile.shape(os.path.join(os.path.dirname(__file__), 'images', 'missile_our.gif'))
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


def game_over():
    return buildings[0].health < 0


window.onclick(our_missile)

our_missiles = []
enemy_missiles = []


while True:
    window.update()
    if game_over():
        continue
    intercept_missile()
    for self in buildings:
        self.damage_to_buildings()
    count_enemy_missiles()
    launch(enemy_missiles)
    launch(our_missiles)
