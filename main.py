from beatmap import Beatmap

from dotenv import load_dotenv
import os
import turtle

def run():
    replay_path = r'sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr'
    
    load_dotenv()
    songs_directory = os.getenv('osu_songs_directory')

    beatmap = Beatmap(replay_path, songs_directory)

    draw_playfield()

    for x, y, time, type in beatmap.hit_object_data:
        turtle.goto(canvas_x(x), canvas_y(y) - beatmap.circle_radius)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(beatmap.circle_radius)
        turtle.color('yellow')
        turtle.end_fill()
        turtle.penup()
        turtle.color('black')

    turtle.exitonclick()

def draw_playfield():
    turtle.setup(960, 600)
    turtle.speed('fastest')
    turtle.hideturtle()
    turtle.color('black')
    turtle.penup()

    turtle.goto((canvas_x(512), canvas_y(384)))
    turtle.pendown()
    turtle.goto((canvas_x(0), canvas_y(384)))
    turtle.goto((canvas_x(0), canvas_y(0)))
    turtle.goto((canvas_x(512), canvas_y(0)))
    turtle.goto((canvas_x(512), canvas_y(384)))
    turtle.penup()

def canvas_x(x: str) -> int:
    return int(x) - 256

def canvas_y(y: str) -> int:
    return -1 * (int(y) - 192)
 
if __name__ == '__main__':
    run()