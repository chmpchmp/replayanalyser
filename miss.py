from dataclasses import dataclass

@dataclass
class Miss:
    hit_object_data: list(list())
    hit_object_timing: int
    cursor_data: list(list())
    cursor_input_data: list(list())
    circle_radius: float