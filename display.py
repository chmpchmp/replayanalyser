import turtle

WINDOW_HEIGHT = 540
WINDOW_WIDTH = 960

PLAYFIELD_HEIGHT = 0.8 * WINDOW_HEIGHT
PLAYFIELD_WIDTH = (4 * PLAYFIELD_HEIGHT) / 3

SCALE = PLAYFIELD_HEIGHT / 384

INPUT_CIRCLE_RADIUS = 2

class Display:
    def __init__(self, miss):
        self.miss = miss

        self.draw_canvas()

        turtle.getscreen().getcanvas().postscript(file = 'test.eps')

        turtle.exitonclick()

    def draw_canvas(self):
        self.setup()
        self.draw_playfield()
        self.draw_hit_objects()
        self.draw_cursor_trail()
        self.draw_cursor_inputs()

    def setup(self):
        turtle.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
        turtle.speed('fastest')
        turtle.hideturtle()

    def draw_playfield(self):
        turtle.color('grey')
        turtle.penup()

        turtle.goto((self.canvas_x(512), self.canvas_y(384)))
        turtle.pendown()
        turtle.goto((self.canvas_x(0), self.canvas_y(384)))
        turtle.goto((self.canvas_x(0), self.canvas_y(0)))
        turtle.goto((self.canvas_x(512), self.canvas_y(0)))
        turtle.goto((self.canvas_x(512), self.canvas_y(384)))
        turtle.penup()

    def draw_hit_objects(self):
        for x, y, time, type in self.miss.hit_object_data:
            turtle.goto(self.canvas_x(x), self.canvas_y(y) - (SCALE * self.miss.circle_radius))
            turtle.pendown()

            if time == self.miss.hit_object_timing:
                if type & 1 == 1:
                    turtle.color('chocolate')
                if type & 2 == 2:
                    turtle.color('burlywood') 
            else:
                if type & 1 == 1:
                    turtle.color('cornflower blue')
                if type & 2 == 2:
                    turtle.color('dark turquoise')

            turtle.circle(SCALE * self.miss.circle_radius)   

            turtle.penup()

    def draw_cursor_trail(self):
        turtle.goto(self.canvas_x(self.miss.cursor_data[0][1]), self.canvas_y(self.miss.cursor_data[0][2]))
        turtle.pendown()

        for time, x, y, input in self.miss.cursor_data:
            turtle.color('black')
            turtle.goto(self.canvas_x(x), self.canvas_y(y))

        turtle.penup()

    def draw_cursor_inputs(self):
        for time, x, y, input in self.miss.cursor_input_data:
            turtle.goto(self.canvas_x(x), self.canvas_y(y) - INPUT_CIRCLE_RADIUS)
            turtle.pendown()

            turtle.color('red')

            turtle.begin_fill()
            turtle.circle(INPUT_CIRCLE_RADIUS)   
            turtle.end_fill()

            turtle.penup()

    def canvas_x(self, x: str) -> int:
        return SCALE * (int(x) - 0.5 * 512)

    def canvas_y(self, y: str) -> int:
        return (-SCALE * (int(y) - 0.5 * 384))