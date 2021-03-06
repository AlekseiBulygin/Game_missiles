import turtle
import os
import shutil
from PIL import Image
from random import randint, choice

PATH = os.path.dirname(__file__)
BASE_X, BASE_Y = 0, -220
ENEMY_COUNT = 5
BUILDINGS_TYPE = {'factory': [-350, -220, 4000],
                  'nuclear': [-200, -220, 3000],
                  'skyscraper': [200, -220, 2000],
                  'house': [350, -220, 500]}


class PointsInGame:

    def __init__(self):
        self.start_points = 0
        self.points = 0
        title = turtle.Turtle()
        title.hideturtle()
        title.color("white")
        title.speed(0)
        title.penup()
        title.setpos(x=-400, y=250)
        title.write(f"Points: {self.start_points}", align="center", font=["Arial", 10, "bold"])
        self.title = title

    def check_points(self):
        if self.points != self.start_points:
            self.start_points = self.points
            self.title.clear()
            self.title.write(f"Points: {self.points}", align="center", font=["Arial", 10, "bold"])


class Missile:
    def __init__(self, color, x, y, x1, y1):
        self.x = x
        self.y = y
        self.to_x = x1
        self.to_y = y1
        self.color = color
        self.status = "launched"
        self.target = x1, y1
        self.radius = 1

        pen = turtle.Turtle(visible=False)
        pen.color(color)
        pen.penup()
        pen.setpos(x, y)
        pen.pendown()
        lenght = pen.towards(x1, y1)
        pen.setheading(lenght)
        pen.showturtle()

        picture = "missile_enemy.gif"
        if color == "white":
            picture = "missile_our.gif"
        self.name = f"{color}_turned_{lenght}.gif"
        if os.path.exists(os.path.join(PATH, "launched_missiles", self.name)):
            self.name = f"{color}_turned_{lenght + randint(0, 100)}.gif"
        image_obj = Image.open(os.path.join(PATH, 'images', picture)).convert("RGB")
        bg = Image.new("RGBA", image_obj.size, (255, 0, 0, 0))
        bg.paste(image_obj.rotate(lenght))
        bg.save(os.path.join(PATH, "launched_missiles", self.name), transparency=0)
        window.register_shape(os.path.join(PATH, "launched_missiles", self.name))
        pen.shape(os.path.join(PATH, "launched_missiles", self.name))

        self.missile = pen

    def get_x(self):
        return self.missile.xcor()

    def get_y(self):
        return self.missile.ycor()

    def move(self):
        status = self.status
        if status == "launched":
            self.missile.forward(4)
            if self.missile.distance(x=self.to_x, y=self.to_y) < 10:
                self.status = "explode"
                self.missile.shape('circle')
        elif status == "explode":
            self.radius += 1
            if self.radius > 3:
                self.missile.clear()
                self.missile.hideturtle()
                self.status = "dead"
            else:
                self.missile.shapesize(self.radius)
        elif status == "dead":
            self.missile.clear()
            self.missile.hideturtle()


class Buildings:
    def __init__(self, x, y, health, name):
        self.x = x
        self.y = y
        self.health = health
        self.name = name
        self.full_health = health
        point = turtle.Turtle()
        point.hideturtle()
        point.speed(0)
        point.penup()
        point.setpos(x=self.x, y=self.y)
        window.register_shape(os.path.join(PATH, 'images', self.get_picture()))
        point.shape(os.path.join(PATH, 'images', self.get_picture()))
        point.showturtle()
        self.point = point

        title = turtle.Turtle()
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.setpos(x=self.x, y=self.y - 65)
        title.write(str(self.health), align="center", font=["Arial", 10, "bold"])
        self.title = title
        self.title_health = self.health

    def get_picture(self):
        if self.health < 0:
            return f"{self.name}_3.gif"
        if self.health < self.full_health * 0.5:
            return f"{self.name}_2.gif"
        return f"{self.name}_1.gif"

    def draw(self):
        picture = self.get_picture()
        if self.point.shape() != os.path.join(PATH, 'images', picture):
            window.register_shape(os.path.join(PATH, 'images', picture))
            self.point.shape(os.path.join(PATH, 'images', picture))
        if self.health != self.title_health and self.health >= 0:
            self.title_health = self.health
            self.title.clear()
            self.title.write(self.title_health, align="center", font=["Arial", 10, "bold"])
        elif self.health != self.title_health and self.health < 0:
            self.title_health = self.health
            self.title.clear()
            self.title.write("0", align="center", font=["Arial", 10, "bold"])

    def is_alive(self):
        return self.health >= 0


class MyBase(Buildings):
    def get_picture(self):

        for missile in our_missiles:
            if missile.missile.distance(self.x, self.y) < 50:
                return f"{self.name}_opened.gif"

        return f"{self.name}.gif"


def enemy_missile():
    start_x = randint(-400, 400)
    start_y = 300
    alive_buildings = [b for b in buildings if b.is_alive()]
    if alive_buildings:
        target = choice(alive_buildings)
        info = Missile(color="red", x=start_x, y=start_y, x1=target.x, y1=target.y)
        enemy_missiles.append(info)


def our_missile(x, y):
    info = Missile(color="white", x=BASE_X, y=BASE_Y + 20, x1=x, y1=y)
    our_missiles.append(info)


def launch(missiles):
    for info in missiles:
        info.move()

    dead_missiles = [i for i in missiles if i.status == "dead"]
    for dead in dead_missiles:
        missiles.remove(dead)
        try:
            os.remove(os.path.join(os.path.dirname(__file__), "launched_missiles", dead.name))
        except FileNotFoundError:
            pass


def count_enemy_missiles():
    if len(enemy_missiles) < ENEMY_COUNT:
        enemy_missile()


def intercept_missile():
    for our_info in our_missiles:
        if our_info.status != "explode":   # intercept missile in explode
            continue
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info.missile
            if enemy_missile.distance(our_info.get_x(), our_info.get_y()) < our_info.radius * 10:
                enemy_info.status = "dead"
                global points
                points.points += 10


def create_buildings():
    buildings.append(MyBase(x=BASE_X, y=BASE_Y, health=4000, name='base'))
    for name, info in BUILDINGS_TYPE.items():
        buildings.append(Buildings(x=info[0], y=info[1], health=info[2], name=name))


def draw_buildings():
    for building in buildings:
        building.draw()


def damage_to_buildings():
    for enemy_info in enemy_missiles:
        enemy_missile = enemy_info.missile
        if enemy_info.status != "explode":
            continue
        for building in buildings:
            if enemy_missile.distance(building.x, building.y) < enemy_info.radius * 10 and \
                    enemy_info.radius == 1:
                building.health -= 100


def game_over():
    return buildings[0].health < 0


buildings = []

window = turtle.Screen()
window.setup(900, 600)


def game():

    global our_missiles, enemy_missiles, buildings, points

    window.clear()
    buildings.clear()
    window.tracer(n=2)
    window.bgpic(os.path.join(PATH, 'images', 'background.gif'))
    window.onclick(our_missile)
    points = PointsInGame()

    our_missiles = []
    enemy_missiles = []
    create_buildings()
    if not os.path.exists("launched_missiles"):
        os.makedirs("launched_missiles")
    while True:
        window.update()
        draw_buildings()
        if game_over():
            break
        intercept_missile()
        points.check_points()
        damage_to_buildings()
        count_enemy_missiles()
        launch(enemy_missiles)
        launch(our_missiles)

    pen = turtle.Turtle(visible=False)
    pen.color("red")
    pen.speed(0)
    pen.penup()
    pen.write("game over", align="center", font=["Arial", 30, "bold"])


while True:
    game()
    answer = window.textinput(title="Hello", prompt="Want more? y/n")
    if answer.lower() not in ['y', 'yes', 'да', 'д']:
        shutil.rmtree("launched_missiles")
        break
