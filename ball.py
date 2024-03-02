from tkinter import *
import random
import time
tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

class Ball:
    def __init__(self, size, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(size, size, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.speeds = [1, 2, 3]
        self.x = random.choice([1, -1]) * random.choice(self.speeds)
        self.y = random.choice([1, -1]) * random.choice(self.speeds)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[3] >= self.canvas_height or pos[1] <= 0:
            self.y = -self.y
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x = -self.x

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left())
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right())

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0]<=0 or pos[2]>=self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

paddle = Paddle(canvas, 'blue')
ball = Ball(10, canvas, 'red')

while True:
    ball.draw()
    paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)