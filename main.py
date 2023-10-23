from replay import Replay
from beatmap import Beatmap

MILLISECOND_INTERVAL = 200

class ReplayData:
    def __init__(self, replay_path: str):
        replay_data = Replay(replay_path).decode_replay()

        life_bar_data = replay_data['life_bar_graph'].split(',')
        self.life_bar_data = dict()

        for point in life_bar_data:
            point_data = point.split('|')
            if float(point_data[1]) < 1:
                self.life_bar_data[int(point_data[0])] = float(point_data[1])
            
        self.cursor_data = replay_data['byte_array'].split(',')[:-1]

        print(self.life_bar_data)

def run():
    path = r'sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr'
    path = r'sample_replays\chmpchmp - Suzuyu - Euphorium [The Dream Of White Star.] (2022-10-28) Osu.osr'
    path = r'sample_replays\chmpchmp - Dove Cameron - LazyBaby [Hard] (2023-08-06) Osu.osr'
   
    data = ReplayData(path)

    import turtle

    ms_offset = 0
    draw_lines = False

    turtle.setup(960, 600)
    turtle.speed('fastest')
    turtle.hideturtle()
    turtle.penup()

    #turtle.goto((0, 0))
    #turtle.pendown()
    #turtle.goto((512, 0))
    #turtle.goto((512, 384))
    #turtle.goto((0, 384))
    #turtle.goto((0, 0))
    #turtle.penup()

    turtle.goto((256, 192))
    turtle.pendown()
    turtle.goto((-256, 192))
    turtle.goto((-256, -192))
    turtle.goto((256, -192))
    turtle.goto((256, 192))
    turtle.penup()

    turtle.color('blue')

    for point in data.cursor_data[1:]:
        point_data = point.split('|')
        #print(point_data)

        ms_offset += int(point_data[0])

        if point_data[0] == '-12345':
            print('Replay finished!')
        else:
            if ms_offset in data.life_bar_data.keys() :
                print('Combo break detected!')
                offset_limit = ms_offset + MILLISECOND_INTERVAL
                draw_lines = True
                turtle.goto((float(point_data[1])-256, float(point_data[2])-192))
                turtle.pendown()

            if draw_lines:
                turtle.goto((float(point_data[1])-256, float(point_data[2])-192))

                if ms_offset > offset_limit:
                    draw_lines = False
                    turtle.penup()
            
            #print(ms_offset)

    turtle.exitonclick()
    
if __name__ == '__main__':
    run()