import math

from superwires import games
games.init(screen_width=640, screen_height=480, fps=50)

class Ship(games.Sprite):
    VELOCITY = .03
    ROTATE_SPEED = 3
    def update(self):
        angle = self.angle * math.pi / 180
        if games.keyboard.is_pressed(games.K_w):
            self.dx += Ship.VELOCITY * math.sin(angle)
            self.dy += Ship.VELOCITY * -math.cos(angle)
        if games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.ROTATE_SPEED
        if games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.ROTATE_SPEED
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width


def main():
    nebula_image = games.load_image("nebula.jpg", transparent=False)
    explosion_files = ["explosion"+str(n)+".bmp" for n in range(1, 10)]
    games.screen.background = nebula_image
    ship_image = games.load_image("ship.bmp")
    ship = Ship(image=ship_image, x=games.screen.width/2, y=games.screen.height/2)
    explosion = games.Animation(images=explosion_files, y = games.screen.height/3,
                                x = games.screen.width/3,
                                n_repeats=0, repeat_interval=5)
    games.screen.add(explosion)
    games.screen.add(ship)
    games.screen.mainloop()
main()
