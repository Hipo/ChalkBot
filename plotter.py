import sys
import threading
from math import sqrt, ceil


def log(s):
    sys.stderr.write(s + '\n')
    sys.stderr.flush()


def write(s):
    sys.stdout.write(s + '\n')
    sys.stdout.flush()


class XY(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "%s, %s" % (self.x, self.y)


class Motor(XY):
    string_length = 0
    step_size = 5
    on_change = lambda self: None

    def __init__(self, name, x=0, y=0, s=0):
        super(Motor, self).__init__(x, y)
        self.name = name
        self.string_length = s

    def step_forward(self):
        self.string_length += self.step_size
        write('M{name}{direction}{steps}'.format(name=self.name, direction='+', steps=2))
        self.on_change()

    def step_backward(self):
        self.string_length -= self.step_size
        write('M{name}{direction}{steps}'.format(name=self.name, direction='-', steps=2))
        self.on_change()

    def change_length(self, l):
        while abs(self.string_length - l) > self.step_size:
            if self.string_length < l:
                self.step_forward()
            elif self.string_length > l:
                self.step_backward()


class Pen(XY):
    down = False


class Plotter(object):
    def __init__(self, width, height, margin=(20, 20), step_size=1, max_segment=5):
        self.width = width
        self.height = height
        self.margin = margin
        self.m1 = Motor('L', 0, 0)
        self.m2 = Motor('R', width, 0)
        self.m1.on_change = self.m2.on_change = self.on_change
        self.m1.step_size = self.m2.step_size = step_size
        self.pen = Pen()
        self.handlers = []
        self.add_change_handler(self.update_pen)
        self.max_segment = max_segment
        self.coords = []

    def move_to(self, x, y):
        target_strings = self.find_string_lengths(x, y)
        log('From %s to target length %s' % ((self.m1.string_length, self.m2.string_length), target_strings))
        # threads are used here because each motor must be controlled simultaneously
        t1 = threading.Thread(target=self.m1.change_length, args=(target_strings[0],))
        t2 = threading.Thread(target=self.m2.change_length, args=(target_strings[1],))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def set_coordinates(self, coords):
        self.coords = self.scale_image(coords)

    def set_initial_position(self, x, y):
        self.m1.string_length, self.m2.string_length = self.find_string_lengths(x, y)
        self.update_pen()

    def move_to_start(self):
        self.move_to(self.coords[0][0], self.coords[0][1])

    def find_string_lengths(self, x, y):
        a = float(x) - self.m1.x
        b = float(x) - self.m2.x
        c = float(y) - self.m1.y
        m1_p = sqrt((a * a) + (c * c))
        m2_p = sqrt((b * b) + (c * c))
        return int(m1_p), int(m2_p)

    def update_pen(self):
        width = self.m2.x - self.m1.x
        x, y = find_pen_position(self.m1.string_length, self.m2.string_length, width)
        self.pen.x = x
        self.pen.y = y

    def pen_down(self):
        log('Set pen down and press enter')
        raw_input()
        self.pen.down = True
        write('PD')

    def pen_up(self):
        log('Lift pen and press enter')
        raw_input()
        self.pen.down = False
        write('PU')

    def on_change(self):
        for f in self.handlers:
            f()

    def add_change_handler(self, f):
        self.handlers.append(f)

    def draw(self):
        self.pen.down = True
        for x, y in self.coords:
            b = XY(x, y)
            previous = XY(self.pen.x, self.pen.y)
            while int(distance(self.pen, b)) > self.max_segment:
                p = point_on_line(self.pen, b, self.max_segment)
                self.move_to(p.x, p.y)
                if self.pen.x == previous.x and self.pen.y == previous.y:
                    log('Breaking out of loop')
                    break
                previous = XY(self.pen.x, self.pen.y)
            self.move_to(x, y)
        self.pen.down = False

    def scale_image(self, coords):
        minx = min([p[0] for p in coords])
        maxx = max([p[0] for p in coords])
        miny = min([p[1] for p in coords])
        maxy = max([p[1] for p in coords])
        dx = float(abs(maxx - minx))
        dy = float(abs(maxy - miny))
        cx = (minx + maxx) / 2.0
        cy = (miny + maxy) / 2.0
        sx = (self.width - (self.margin[0] * 2.0)) / dx
        sy = (self.height - (self.margin[1] * 2.0)) / dy
        s = min(sx, sy)
        tx = ((self.width / 2.0) - (cx * s))
        ty = ((self.height / 2.0) - (cy * s))
        return [((x * s) + tx, (y * s) + ty) for x, y in coords]


def ease(a, b, t):
    m = XY()
    m.x = a.x + ((b.x - a.x) * t)
    m.y = a.y + ((b.y - a.y) * t)
    return m


def point_on_line(a, b, d):
    vx = float(b.x - a.x)
    vy = float(b.y - a.y)
    mag = sqrt(vx ** 2 + vy ** 2)
    vx /= mag
    vy /= mag
    p = XY()
    p.x = ceil(a.x + vx * d)
    p.y = ceil(a.y + vy * d)
    return p


def distance(a, b):
    vx = float(b.x - a.x)
    vy = float(b.y - a.y)
    return sqrt(vx ** 2 + vy ** 2)


def height_of_triangle(a, b, c):
    s = (a + b + c) / 2.0
    area = sqrt(s * (s - a) * (s - b) * (s - c))  # Heron's Formula
    h = area / (0.5 * c)  # height of triangle with base c
    return h


def find_pen_position(s1, s2, width):
    y = height_of_triangle(s1, s2, width)
    # s1^2 = y^2 + x^2
    x = sqrt(abs((s1 ** 2) - (y ** 2)))
    return round(x), round(y)
