from PIL import Image
import threading
import matplotlib
import time
import numpy as np
from logging import getLogger

logger = getLogger('show_map')

class ShowMap:
    def __init__(self, grid, show_gui = True, save_map_time = 5, name = 'map.png', robot_size = 3):
        if not show_gui:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        self.__save_map_time = save_map_time
        self.__name = name
        self.__robot_size = robot_size
        self.__image = Image.fromarray(grid * 255)
        plt.rcParams['toolbar'] = 'None'
        self.__fig, self.__ax = plt.subplots(1, 1)
        self.__fig.suptitle(self.__name)
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])
        self.__implot = self.__ax.imshow(self.__image)
        plt.show(block=False)
        self.__fig.canvas.draw()
        self.__save()
        self.__start_time = time.time()

    def update(self, map_to_display, robot_cell, goal_point = None, path = None, frontiers = None, attr_force = None, rep_force = None):
        import matplotlib.pyplot as plt
        plt.pause(0.02)
        grid = np.matrix(map_to_display.grid)
        for x in range(map_to_display.grid_width):
            for y in range(map_to_display.grid_height):
                value = grid[x, y]
                self.__image.putpixel((x, map_to_display.grid_height - 1 - y), abs(255 - (value * 255)))
        self.__ax.clear()
        self.__implot = self.__ax.imshow(self.__image)
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])
        self.__ax.plot(robot_cell.x, map_to_display.grid_height - 1 - robot_cell.y, 'rs', markersize=self.__robot_size)
        if rep_force != None:
            y = map_to_display.grid_height - 1 - robot_cell.y
            self.__ax.arrow(robot_cell.x, y, rep_force['dx'], -rep_force['dy'], head_width=1, head_length=2, fc='g', ec='g')
        if attr_force != None:
            y = map_to_display.grid_height - 1 - robot_cell.y
            self.__ax.arrow(robot_cell.x, y, attr_force['dx'], -attr_force['dy'], head_width=1, head_length=2, fc='g', ec='g')
        if goal_point != None:
            self.__ax.plot(goal_point.x, map_to_display.grid_height - 1 - goal_point.y, 'bh', markersize=8)
        if path != None:
            for point in path:
                self.__ax.plot(point.x, map_to_display.grid_height - 1 - point.y, 'g+', markersize=2)
        if frontiers != None:
            index = 0
            for frontier in frontiers:
                for point in frontier:
                    color = ['gh', 'ch', 'mh', 'yh', 'kh']
                    self.__ax.plot(point.x, map_to_display.grid_height - 1 - point.y, color[index % 5], markersize=1)
                index += 1
        self.__fig.canvas.draw()
        elapsed_time = time.time() - self.__start_time
        if elapsed_time >= self.__save_map_time:
            self.__save()
            self.t = threading.Thread(target=self.__save, args=())
            self.t.start()
            self.__start_time = time.time()

    def __save(self):
        pass
        """
        data = np.fromstring(self.__fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(self.__fig.canvas.get_width_height()[::-1] + (3,))
        img = Image.fromarray(data)
        img.convert('RGB').save(self.__name, "PNG")
        """
