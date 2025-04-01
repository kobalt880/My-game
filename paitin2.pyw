from pygame import *
from time import sleep

def rinr(r1, r2, glob=False):
    bools = []
    if not glob:
        for i in range(r1[0], r1[1]):
            for j in range(r2[0], r2[1]):
                bools.append(j == i)
        return any(bools)

    else:
        for i in range(r1[0], r1[1]):
            bools.append(i in range(r2[0], r2[1]))
        return all(bools)

def show_text(text, pos=(5, 5)):
    text = f.render(text, True, (200, 255, 255))
    win.blit(text, pos)

class Player:
    def __init__(self, x, y, size=20, hp=3, color=(200, 50, 50)):
        self.x = x
        self.y = y
        self.size = size
        self.hp = hp
        self.color = color
        self.base_x = x
        self.base_y = y
        self.max_hp = hp

    def get_x_area(self, extend=False):
        if not extend:
            return self.x, self.x + self.size
        else:
            return self.x - 1, self.x + self.size + 1

    def get_y_area(self, extend=False):
        if not extend:
            return self.y, self.y + self.size
        else:
            return self.y - 1, self.y + self.size + 1

    def to_center(self):
        self.x = self.base_x
        self.y = self.base_y

    def update(self, init=False):
        if init:
            self.Pass = (rinr(self.get_x_area(True), (0, 500)) and
            rinr(self.get_y_area(True), (0, 500)))
        else:
            if self.hp <= 0: self.Pass = False
            if not self.Pass: self.to_center()

    def down(self, ws):
        if not any([rinr((self.y + 1, self.y + self.size + 1), wall.get_y_area()) and
        rinr(self.get_x_area(), wall.get_x_area()) for wall in ws.walls]):
            self.y += 1

    def up(self, ws):
        if not any([rinr((self.y - 1, self.y + self.size - 1), wall.get_y_area()) and
        rinr(self.get_x_area(), wall.get_x_area()) for wall in ws.walls]):
            self.y -= 1

    def left(self, ws):
        if not any([rinr(self.get_y_area(), wall.get_y_area()) and
        rinr((self.x - 1, self.x + self.size - 1), wall.get_x_area()) for wall in ws.walls]):
            self.x -= 1

    def right(self, ws):
        if not any([rinr(self.get_y_area(), wall.get_y_area()) and
        rinr((self.x + 1, self.x + self.size + 1), wall.get_x_area()) for wall in ws.walls]):
            self.x += 1

    def show(self):
        draw.rect(win, self.color, Rect(self.x, self.y, self.size, self.size))

class Wall:
    def __init__(self, x, y, width, height, destroyed=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.destroyed = destroyed

    def get_x_area(self):
        return self.x, self.x + self.width

    def get_y_area(self):
        return self.y, self.y + self.height

    def check(self, pl: Player, evil=True, var=None, end=False):
        global over, gw_num

        if not self.destroyed:
            if (inside := rinr(self.get_x_area(), pl.get_x_area()) and rinr(self.get_y_area(), pl.get_y_area())) and evil:
                pl.hp -= 1
                pl.to_center()
            elif inside and not end:
                if var == 1:
                    walls.walls[4].x += 25
                    self.destroyed = True
                elif var == 2:
                    try:
                        walls2.walls[2].x += 12
                        self.destroyed = True
                        good_walls2.walls[gw_num].destroyed = False
                        gw_num += 1
                    except IndexError: pass

                elif var == 3:

                    def verify(num):
                        self.destroyed = True

                        if not good_walls3.walls[num].destroyed:
                            for wall in good_walls3.walls:
                                wall.destroyed = False
                            player3.to_center()

                    if not any((gw3 := [wall.destroyed for wall in good_walls3.walls])):
                        verify(5)
                    elif gw3.count(True) == 1:
                        verify(3)
                    elif gw3.count(True) == 2:
                        verify(2)
                    elif gw3.count(True) == 3:
                        verify(1)
                    elif gw3.count(True) == 4:
                        verify(6)
                    elif gw3.count(True) == 5:
                        verify(0)
                    elif gw3.count(True) == 6:
                        verify(4)
                    elif gw3.count(True) == 7:
                        verify(7)
                        player3.base_y, player3.base_x = 25, 275
                        player3.to_center()
                    elif gw3.count(True) == 8:
                        player3.x, player3.y = 125, 30

            elif inside and end:
                over = True

class Walls:
    def __init__(self, walls: list[Wall], color=(43, 25, 129)):
        self.walls = walls
        self.color = color

    def show(self):
        for wall in self.walls:
            if not wall.destroyed:
                draw.rect(win, self.color, Rect(wall.x, wall.y, wall.width, wall.height))

    def check_bad_walls(self, pl: Player):
        for wall in self.walls:
            wall.check(pl)

    def check_good_walls(self, pl, var):
        for wall in self.walls:
            wall.check(pl, False, var)

    def check_end_wall(self, pl):
        self.walls[0].check(pl, end=True, evil=False)

class Level:
    def __init__(self, player, walls, bad_walls, good_walls, end_wall, var_of_gw, final=False, skip=False):
        self.player = player
        self.walls = walls
        self.bad_walls = bad_walls
        self.good_walls = good_walls
        self.end_wall = end_wall
        self.final = final
        self.skip = skip
        self.var_of_gw = var_of_gw

    def start(self):
        global over
        over = False
        self.player.update(True)

        while self.player.hp > 0 and not over and not self.skip:
            fps.tick(120)

            for e in event.get():
                if e.type == QUIT:
                    raise

            press = key.get_pressed()
            if press[K_w]:
                self.player.up(self.walls)
            if press[K_s]:
                self.player.down(self.walls)
            if press[K_a]:
                self.player.left(self.walls)
            if press[K_d]:
                self.player.right(self.walls)

            self.player.update()
            self.player.update(True)

            win.fill((0, 0, 0))
            self.player.show()
            self.walls.show()
            self.bad_walls.show()
            self.good_walls.show()
            self.end_wall.show()

            self.bad_walls.check_bad_walls(self.player)
            self.good_walls.check_good_walls(self.player, self.var_of_gw)
            self.end_wall.check_end_wall(self.player)

            show_text(f'Level {self.var_of_gw}, Health: {self.player.hp}' if self.player.hp > 0 else 'game over')

            display.flip()
        else:
            if self.player.hp <= 0:
                sleep(1)
                raise
            elif over and self.final:
                win.fill((0, 0, 0))
                show_text('game over!')
                display.flip()
                sleep(1)
#=======================================================
init()

win = display.set_mode((500, 500))
display.set_caption('game')

f = font.Font(None, 30)
fps = time.Clock()

walls = Walls([
    Wall(250, 150, 50, 300),
    Wall(0, 150, 250, 50),
    Wall(-5, 0, 10, 500),
    Wall(0, 230, 200, 23),
    Wall(5, 430, 250, 20),
    Wall(495, 0, 10, 500), # right wall
    Wall(95, 42, 150, 110) # final wall
], (43, 25, 129))
walls2 = Walls([
    Wall(0, 0, 500, 100),
    Wall(100, 0, 20, 470),
    Wall(430, 410, 150, 20), # moving wall
    Wall(410, 410, 20, 150),
    Wall(0, 495, 410, 10), # lower wall
    Wall(0, 130, 5, 500), # left wall
    Wall(495, 0, 10, 410) # right wall
]); gw_num = 1
walls3 = Walls([
    Wall(250, 250, 250, 20),
    Wall(250, 250, 20, 250),
    Wall(250, 480, 250, 20),
    Wall(480, 250, 20, 250),
    Wall(250, 0, 20, 250), # second sector wall
    Wall(480, 0, 20, 250),
    Wall(250, 0, 250, 20),
    Wall(250, 50, 200, 5), # tall wall
    Wall(0, 0, 5, 500) # left wall
])

bad_walls = Walls([
    Wall(300, 427, 100, 23),
    Wall(430, 427, 100, 23),
    Wall(230, 200, 20, 230),
    Wall(25, 280, 210, 20),
    Wall(5, 330, 100, 20), # double
    Wall(135, 330, 100, 20), # second
    Wall(95, 0, 400, 20), # final wall
    Wall(300, 150, 60, 23), # second double
    Wall(390, 150, 150, 23) # second
], (255, 0, 0))
bad_walls2 = Walls([
    Wall(25, 450, 75, 20),
    Wall(5, 390, 75, 20),
    Wall(25, 330, 75, 20),
    Wall(5, 270, 75, 20),
    Wall(5, 130, 35, 100), # first double
    Wall(65, 130, 35, 100), # second
    Wall(120, 100, 375, 20), # second double
    Wall(140, 142, 335, 20)
], (255, 0, 0))
bad_walls3 = Walls([
    Wall(270, 80, 50, 90), #labyrint
    Wall(350, 80, 130, 40),
    Wall(320, 150, 120, 20),
    Wall(470, 80, 10, 140),
    Wall(270, 170, 90, 50),
    Wall(390, 200, 90,20),
    Wall(5, 100, 60, 140), # first double
    Wall(87, 100, 250-87, 140),
    Wall(5, 280, 150, 140), # second double
    Wall(155+22, 280, 250-(155+22), 140)
], color=(255, 0, 0))

good_walls = Walls([
    Wall(205, 305, 20, 20)
], (0, 255, 0))
good_walls2 = Walls([
    Wall(75, 105, 20, 20),
    Wall(287, 121, 20, 20, destroyed=True),
], (0, 255, 0))
good_walls3 = Walls([
    Wall(290, 290, 20, 20),
    Wall(340, 290, 20, 20),
    Wall(390, 290, 20, 20),
    Wall(440, 290, 20, 20), # upper
    Wall(290, 440, 20, 20),
    Wall(340, 440, 20, 20),
    Wall(390, 440, 20, 20),
    Wall(440, 440, 20, 20), # lower
    Wall(275, 225, 20, 20), # portal wall

], color=(0, 255, 0))

end_wall = Walls([Wall(10, 5, 80, 140)], (255, 0, 255))
end_wall2 = Walls([Wall(450, 450, 50, 50)], (255, 0, 255))
end_wall3 = Walls([Wall(5, 480, 245, 50)], color=(255, 0, 255))

player = Player(10, 205)
player2 = Player(130, 400)
player3 = Player(365, 365)

try:
    level1 = Level(
        player,
        walls,
        bad_walls,
        good_walls,
        end_wall,
        1
    )
    level1.start()

    level2 = Level(
        player2,
        walls2,
        bad_walls2,
        good_walls2,
        end_wall2,
        2
    )
    level2.start()

    level3 = Level(
        player3,
        walls3,
        bad_walls3,
        good_walls3,
        end_wall3,
        3,
        final=True
    )
    level3.start()

except RuntimeError:
    pass
