from miss import Miss

import turtle

class Display:
    def __init__(self, miss: Miss):
        self.miss = miss
        self.draw_playfield()

        for x, y, time, type in self.miss.hit_object_data:
            turtle.goto(self.canvas_x(x), self.canvas_y(y) - self.miss.circle_radius)
            turtle.pendown()
            turtle.begin_fill()
            turtle.circle(self.miss.circle_radius)
            
            if time == self.miss.hit_object_timing:
                turtle.color('red')
            else:
                turtle.color('yellow')
                
            turtle.end_fill()
            turtle.penup()
            turtle.color('black')

        turtle.goto(self.canvas_x(self.miss.cursor_data[0][1]), self.canvas_y(self.miss.cursor_data[0][2]))

        for time, x, y, input in self.miss.cursor_data:
            turtle.pendown()
            turtle.goto(self.canvas_x(x), self.canvas_y(y))

        turtle.exitonclick()

    def draw_playfield(self):
        turtle.setup(960, 600)
        turtle.speed('fastest')
        turtle.hideturtle()
        turtle.color('black')
        turtle.penup()

        turtle.goto((self.canvas_x(512), self.canvas_y(384)))
        turtle.pendown()
        turtle.goto((self.canvas_x(0), self.canvas_y(384)))
        turtle.goto((self.canvas_x(0), self.canvas_y(0)))
        turtle.goto((self.canvas_x(512), self.canvas_y(0)))
        turtle.goto((self.canvas_x(512), self.canvas_y(384)))
        turtle.penup()

    def canvas_x(self, x: str) -> int:
        return int(x) - 256

    def canvas_y(self, y: str) -> int:
        return -1 * (int(y) - 192)