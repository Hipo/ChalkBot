from PIL import Image
from PIL import ImageDraw, ImageFont


class Simulator(object):
    def __init__(self, plotter, skip_frames=100, output_directory='./'):
        self.plotter = plotter
        plotter.add_change_handler(self.update)
        self.font = ImageFont.truetype("arial.ttf", 20)
        self.line = []
        self.i = 0
        self.skip_frames = skip_frames
        self.output_directory = output_directory

    def update(self):
        if self.plotter.pen.down:
            self.line.append((self.plotter.pen.x, self.plotter.pen.y))
        if self.i % self.skip_frames == 0:
            self.render_frame()
        self.i += 1

    def finish(self):
        self.render_frame()

    def render_frame(self):
        plotter = self.plotter
        image = Image.new("RGB", (plotter.width, plotter.height), "#D0D0D0")
        draw = ImageDraw.Draw(image)
        draw.line(self.line, fill=(255, 0, 0, 255), width=2)
        draw.text((50, 10), "%0.0f" % plotter.m1.string_length, font=self.font, fill=(0, 0, 0, 255))
        draw.text((plotter.width - 100, 10), "%0.0f" % plotter.m2.string_length, font=self.font, fill=(0, 0, 0, 255))
        draw.line([(0, 0), (plotter.pen.x, plotter.pen.y)], fill=(0, 0, 0, 255), width=2)
        draw.line([(plotter.width, 0), (plotter.pen.x, plotter.pen.y)], fill=(0, 0, 0, 255), width=2)
        image.save("%s/frame%04.0f.png" % (self.output_directory, self.i), "PNG")

    def render_test(self, coords):
        plotter = self.plotter
        image = Image.new("RGB", (plotter.width, plotter.height), "#D0D0D0")
        draw = ImageDraw.Draw(image)
        draw.line(coords, fill=(255, 0, 0, 255), width=2)
        draw.rectangle([(plotter.margin[0], plotter.margin[1]), (plotter.width - plotter.margin[0], plotter.height - plotter.margin[1])], outline=(0, 0, 255, 255))
        image.save("%s/test.png" % self.output_directory, "PNG")
