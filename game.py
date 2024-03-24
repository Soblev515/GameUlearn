import math
import random

from superwires import games
games.init(screen_width=640, screen_height=480, fps=50)

class Wrapper(games.Sprite):
    def update(self):
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width
    
    def die(self):
        self.destroy()

class Asteroid(Wrapper):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL: games.load_image("asteroid_small.bmp"),
              MEDIUM: games.load_image("asteroid_med.bmp"),
              LARGE: games.load_image("asteroid_big.bmp")}
    SPEED = 2

    def __init__(self, x, y, size):
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],
            x = x,y = y,
            dx= random.choice([-1, 1]) * Asteroid.SPEED*random.random()/size,
            dy= random.choice([-1, 1]) * Asteroid.SPEED*random.random()/size
        )
        self.size = size
        

class Missile(Wrapper):
    image = games.load_image("missile.bmp")
    sound = games.load_sound("missile.wav")
    BUFFER = 40
    VELOCITY = 7
    LIFETIME = 40

    def __init__(self, ship_x, ship_y, ship_angle):
        angle = ship_angle * math.pi / 180
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y
        dx = Missile.VELOCITY * math.sin(angle)
        dy = Missile.VELOCITY * -math.cos(angle)
        super(Missile, self).__init__(
            x=x,y=y,dx=dx,dy=dy, image=Missile.image
        )
        self.lifetime = Missile.LIFETIME

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.destroy()
        super(Missile, self).update()

class Ship(Wrapper):
    VELOCITY = .03
    ROTATE_SPEED = 3
    MISSILE_DELAY = 25
    sound = games.load_sound("thrust.wav")
    image = games.load_image("ship.bmp")

    def __init__(self, x, y):
        super(Ship, self).__init__(
            image=Ship.image, x=x, y=y
        )
        self.missile_delay = 0

    def update(self):
        angle = self.angle * math.pi / 180
        if self.missile_delay > 0:
            self.missile_delay -= 1
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_delay <= 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_delay = Ship.MISSILE_DELAY
        if games.keyboard.is_pressed(games.K_w):
            Ship.sound.play()
            self.dx += Ship.VELOCITY * math.sin(angle)
            self.dy += Ship.VELOCITY * -math.cos(angle)
        if games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.ROTATE_SPEED
        if games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.ROTATE_SPEED
        super(Ship, self).update()


def main():
    games.music.load("theme.mid")
    games.music.play()
    nebula_image = games.load_image("nebula.jpg", transparent=False)
    explosion_files = ["explosion"+str(n)+".bmp" for n in range(1, 10)]
    games.screen.background = nebula_image
    ship = Ship(x=games.screen.width/2, y=games.screen.height/2)
    explosion = games.Animation(images=explosion_files, y = games.screen.height/3,
                                x = games.screen.width/3,
                                n_repeats=0, repeat_interval=5)
    games.screen.add(explosion)
    games.screen.add(ship)
    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x=x, y=y, size = size)
        games.screen.add(new_asteroid)
    games.screen.mainloop()
main()