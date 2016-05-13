import sys
import os

from PIL import Image
from PIL import ImageDraw, ImageFont

from plotter import Pen, find_pen_position


class Simulator(object):
    def __init__(self, plotter_width, plotter_height, margin, skip_frames=100, output_directory='./'):
        self.font = ImageFont.truetype("arial.ttf", 20)
        self.line = []
        self.i = 0
        self.skip_frames = skip_frames
        self.output_directory = output_directory
        try:
            os.makedirs(output_directory)
        except os.error:
            pass
        self.height = 400
        self.scale_factor = self.height / float(plotter_height)
        self.width = int(plotter_width * self.scale_factor)
        self.plotter_width = plotter_width
        self.plotter_height = plotter_height
        self.margin = margin
        self.left_string_length = 0
        self.right_string_length = 0
        self.pen = Pen()

    def update(self):
        if self.pen.down:
            self.line.append(self.scale(self.pen.x, self.pen.y))
        if self.i % self.skip_frames == 0:
            self.render_frame()
        self.i += 1

    def process_command(self, s):
        command = s[0]
        if command == 'M':
            motor = s[1]
            direction = s[2]
            steps = int(s[3])
            if direction == '-':
                steps *= -1
            if motor == 'L':
                self.left_string_length += (steps * self.step_size)
            else:
                self.right_string_length += (steps * self.step_size)
            self.pen.x, self.pen.y = find_pen_position(self.left_string_length, self.right_string_length, self.plotter_width)
        if command == 'P':
            if s[1] == 'D':
                self.pen.down = True
            elif s[1] == 'U':
                self.pen.down = False
        self.update()

    def run(self, commands):
        for s in commands:
            if s[-1] == '\n':
                s = s[:-1]
            print(s)
            self.process_command(s)
        sim.finish()

    def finish(self):
        self.render_frame()

    def scale(self, x, y):
        return (x * self.scale_factor, y * self.scale_factor)

    def render_frame(self):
        image = Image.new("RGB", (self.width, self.height), "#111")
        draw = ImageDraw.Draw(image)
        draw.line(self.line, fill=(255, 0, 0, 255), width=2)
        draw.text((50, 10), "%0.0f" % self.left_string_length, font=self.font, fill=(255, 255, 255, 255))
        draw.text((self.width - 100, 10), "%0.0f" % self.right_string_length, font=self.font, fill=(255, 255, 255, 255))
        draw.line([(0, 0), self.scale(self.pen.x, self.pen.y)], fill=(255, 255, 255, 255), width=2)
        draw.line([(self.width, 0), self.scale(self.pen.x, self.pen.y)], fill=(255, 255, 255, 255), width=2)
        image.save("%s/frame%04.0f.png" % (self.output_directory, self.i), "PNG")

    def render_test(self, coords):
        image = Image.new("RGB", (self.width, self.height), "#D0D0D0")
        draw = ImageDraw.Draw(image)
        draw.line([self.scale(x, y) for x, y in coords], fill=(255, 0, 0, 255), width=2)
        draw.rectangle([self.scale(self.margin[0], self.margin[1]), self.scale(self.plotter_width - self.margin[0], self.plotter_height - self.margin[1])], outline=(0, 0, 255, 255))
        image.save("%s/test.png" % self.output_directory, "PNG")


if __name__ == '__main__':
    sim = Simulator(plotter_width=910, plotter_height=800, margin=(50, 100), skip_frames=10, output_directory='output')
    sim.left_string_length, sim.right_string_length = 605, 605
    sim.step_size = 5
    sim.run(sys.stdin.readlines())
