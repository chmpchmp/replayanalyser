from dataclasses import dataclass

@dataclass
class Miss:
    hit_object_data: list
    hit_object_timing: int
    cursor_data: list
    cursor_input_data: list
    circle_radius: float