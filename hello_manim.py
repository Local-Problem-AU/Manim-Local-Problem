# file: hello_manim.py
from manim import *

class HelloManim(Scene):
    def construct(self):
        square = Square().scale(1.2).set_color(BLUE)
        self.add(square)
