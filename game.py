import math
import random

from superwires import games, color
games.init(screen_width=640, screen_height=480, fps=50)

class Game(object):
    def __init__(self):
        self.level = 0
        self.sound = games.load_sound("level.wav")
        self.score = games.Text(value=0, size=30, color=color.white, top=5, right=games.screen.width - 10,
                                is_collideable=False)
        games.screen.add(self.score)
        self.ship = Ship(game = self,
                         x= games.screen.width/2,
                         y= games.screen.height/2)
        games.screen.add(self.ship)

    def play(self):
        games.music.load("theme.mid")
        games.music.play(-1)
        nebula_img = games.load_image("nebula.jpg")
        games.screen.background = nebula_img
        self.advance()
        games.screen.mainloop()

    def advance(self):
        self.level += 1
        BUFFER = 30
        for i in range(self.level):
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)
            x = self.ship.x + x_distance 
            y = self.ship.y + y_distance
            x = x % games.screen.width
            y = y % games.screen.height
            new_asteroid = Asteroid(game = self, x=x, y=y, size=Asteroid.LARGE)
            games.screen.add(new_asteroid)
            level_message = games.Message(value= f"Level {self.level}", size=40,
                                          color=color.purple, 
                                          x = games.screen.width/2,
                                          y = games.screen.height/2,
                                          is_collideable=False, 
                                          lifetime=3*games.screen.fps)
            games.screen.add(level_message)
            if self.level > 1:
                self.sound.play()
    
    def end(self):
        end_message = games.Message(value="Game Over",
                                    size = 90,
                                    color=color.red,
                                    x= games.screen.width/2,
                                    y=games.screen.height/2, 
                                    lifetime=5*games.screen.fps,
                                    is_collideable=False,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)                
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

class Collider(Wrapper):
    def update(self):
        super(Collider, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()

class Explosion(games.Animation):
    sound = games.load_sound("explosion.wav")
    images = [f"explosion{i}.bmp" for i in range(1, 10)]

    def __init__(self, x, y):
        super(Explosion, self).__init__(
            images=Explosion.images, x=x, y=y,
            repeat_interval=4, n_repeats=1,
            is_collideable=False
        )
        Explosion.sound.play()

class Asteroid(Wrapper):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    POINTS = 30
    total = 0
    images = {SMALL: games.load_image("asteroid_small.bmp"),
              MEDIUM: games.load_image("asteroid_med.bmp"),
              LARGE: games.load_image("asteroid_big.bmp")}
    SPEED = 2
    SPAWN = 2
    def __init__(self, game, x, y, size):
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],
            x = x,y = y,
            dx= random.choice([-1, 1]) * Asteroid.SPEED*random.random()/size,
            dy= random.choice([-1, 1]) * Asteroid.SPEED*random.random()/size
        )
        self.size = size
        self.game = game
        Asteroid.total += 1

    def die(self):
        Asteroid.total -= 1
        self.game.score.value += int(Asteroid.POINTS/ self.size)
        self.game.score.right = games.screen.width - 10
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game = self.game, x=self.x, y=self.y,
                                        size = self.size-1)
                games.screen.add(new_asteroid)
        super(Asteroid, self).die()
        if Asteroid.total == 0:
            self.game.advance()

class Missile(Collider):
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

class Ship(Collider):
    VELOCITY = .03
    ROTATE_SPEED = 3
    MISSILE_DELAY = 25
    sound = games.load_sound("thrust.wav")
    image = games.load_image("ship.bmp")

    def __init__(self, game, x, y):
        super(Ship, self).__init__(
            image=Ship.image, x=x, y=y
        )
        self.missile_delay = 0
        self.game = game
    
    def die(self):
        self.game.end()
        super(Ship, self).die()
    
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
    my_game = Game()
    my_game.play()
main()