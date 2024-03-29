from miss import Miss

from PIL import Image, ImageDraw

PLAYFIELD_HEIGHT = 384
PLAYFIELD_WIDTH = 512

INPUT_CIRCLE_RADIUS = 2

class Canvas:
    def __init__(self, miss: Miss, width: int, height: int):
        self.miss = miss

        self.width = width
        self.height = height

        self.scale = (0.8 * self.height) / PLAYFIELD_HEIGHT

        self.image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image) 

    def export(self, directory: str, output_file: int) -> None:
        self.draw_canvas()
        self.export_canvas(directory, output_file)

    def draw_canvas(self) -> None:
        self.draw_playfield()
        self.draw_hit_objects()
        self.draw_cursor_trail()
        self.draw_cursor_inputs()

    def draw_playfield(self) -> None:
        playfield_coordinates = [(0, 0), (0, 384), (512, 384), (512, 0), (0, 0)]
        self.draw_lines(playfield_coordinates, "grey")

    def draw_hit_objects(self) -> None:
        for x, y, time, type in self.miss.hit_object_data:
            if time == self.miss.hit_object_timing:
                self.draw_ellipse((x, y), self.scale * self.miss.circle_radius, 'red')
            else:
                self.draw_ellipse((x, y), self.scale * self.miss.circle_radius, 'black')
            
    def draw_cursor_trail(self) -> None:
        cursor_data = [(x, y) for time, x, y, input in self.miss.cursor_data]
        self.draw_lines(cursor_data, "black")

        self.draw_ellipse((self.miss.cursor_data[-1][1], self.miss.cursor_data[-1][2]), self.scale * INPUT_CIRCLE_RADIUS, 'black', 'yellow')

    def draw_cursor_inputs(self) -> None:
        for time, x, y, input in self.miss.cursor_input_data:
            self.draw_ellipse((x, y), self.scale * INPUT_CIRCLE_RADIUS, 'blue',)

    def draw_lines(self, points: list, color: str, line_width = 0) -> None:
        transformed_points = [(self.canvas_x(x), self.canvas_y(y)) for x, y in points]
        self.draw.line(transformed_points, fill = color, width = line_width)

    def draw_ellipse(self, point: tuple, circle_radius: float, border_color: str, fill_color = None) -> None:
        transformed_point = (self.canvas_x(point[0]), self.canvas_y(point[1]))
        point_coordinates = [(transformed_point[0] - circle_radius, transformed_point[1] - circle_radius), (transformed_point[0] + circle_radius, transformed_point[1] + circle_radius)]
        self.draw.ellipse(point_coordinates, outline = border_color, fill = fill_color) 

    def canvas_x(self, x: str) -> int:
        return self.scale * (int(x) - 0.5 * PLAYFIELD_WIDTH) + 0.5 * self.width

    def canvas_y(self, y: str) -> int:
        return self.scale * (int(y) - 0.5 * PLAYFIELD_HEIGHT) + 0.5 * self.height
    
    def export_canvas(self, directory: str, output_file: int) -> None:
        self.image.save(f'{directory}\\{output_file:06}.png')