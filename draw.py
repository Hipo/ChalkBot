import json
import sys
from plotter import Plotter, log
from simulator import Simulator


if __name__ == '__main__':
    filename = sys.argv[1]
    coords = json.load(open(filename))
    plotter = Plotter(width=910, height=800, margin=(50, 100), step_size=10, max_segment=10)
    sim = Simulator(plotter_width=plotter.width, plotter_height=plotter.height, margin=plotter.margin, output_directory='output')
    cx, cy = (plotter.width / 2), (plotter.height / 2)
    plotter.set_initial_position(cx, cy)
    log('set initial lengths: %s, %s' % (plotter.m1.string_length, plotter.m2.string_length))
    raw_input()
    plotter.set_coordinates(coords)
    sim.render_test(plotter.coords)
    plotter.move_to_start()
    plotter.pen_down()
    plotter.draw()
    plotter.pen_up()
    plotter.move_to(cx, cy)
