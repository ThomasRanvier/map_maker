from PIL import Image
import threading
import matplotlib
import time
import numpy as np
from logging import getLogger

logger = getLogger('show_map')

class ShowMap:
    """
    Class that implements the ShowMap object.
    """

    def __init__(self, grid, show_gui = True, save_map_time = 5, name = 'map.png'):
        """
        Instantiates a ShowMap.
        :param grid: The grid of the environment with certainty values.
        :type grid: 2D Numpy array
        :param show_gui: True if we want to show the gui, False otherwise.
        :type show_gui: boolean
        :param save_map_time: Delay between each save of the map.
        :type save_map_time: float
        :param name: Name of the map file.
        :type name: string
        """
        if not show_gui:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        self.__save_map_time = save_map_time
        self.__name = name
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

    def update(self, map_to_display, robot_cell, goal_point = None, frontiers = None, forces = None):
        """
        Function that updates the gui.
        :param map_to_display: The map of the environment to display.
        :type map_to_display: Map
        :param robot_cell: The cell of the robot in the grid.
        :type robot_cell: Position
        :param goal_point: The goal point.
        :type goal_point: Position
        :param frontiers: The frontiers.
        :type frontiers: A list of Position objects.
        :param forces: The forces.
        :type forces: A dictionary of dictionaries representing vectors.
        """
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
        self.__ax.plot(robot_cell.x, map_to_display.grid_height - 1 - robot_cell.y, 'rs', markersize=3)
        if forces != None:
            y = map_to_display.grid_height - 1 - robot_cell.y
            if forces['rep_force'] != None:
                self.__ax.arrow(robot_cell.x, y, forces['rep_force']['x'], -forces['rep_force']['y'], head_width=1, head_length=2, fc='r', ec='r')
            if forces['attr_force'] != None:
                self.__ax.arrow(robot_cell.x, y, forces['attr_force']['x'], -forces['attr_force']['y'], head_width=1, head_length=2, fc='g', ec='g')
            if forces['gen_force'] != None:
                self.__ax.arrow(robot_cell.x, y, forces['gen_force']['x'], -forces['gen_force']['y'], head_width=1, head_length=2, fc='m', ec='m')
        if goal_point != None:
            self.__ax.plot(goal_point.x, map_to_display.grid_height - 1 - goal_point.y, 'bh', markersize=8)
        if frontiers != None:
            index = 0
            for frontier in frontiers:
                count = 0
                for point in frontier:
                    count += 1
                    if count % 3 == 0:
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
        """
        Function that saves the map to a file.
        """
        pass
        """
        data = np.fromstring(self.__fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(self.__fig.canvas.get_width_height()[::-1] + (3,))
        img = Image.fromarray(data)
        img.convert('RGB').save(self.__name, "PNG")
        """
