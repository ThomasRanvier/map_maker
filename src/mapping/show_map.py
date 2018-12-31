from PIL import Image
import threading
import matplotlib
import time
import numpy as np

class ShowMap:
    def __init__(self, map_to_display, show_gui = True, save_map_time = 5, name = 'map.png', robot_size = 3):
        if not show_gui:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        self.__map = map_to_display
        self.__save_map_time = save_map_time
        self.__name = name
        self.__robot_size = robot_size
        self.__image = Image.fromarray(self.__map.grid * 255)
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

    def update(self, robot_pos, goal_point = None, path = None, frontiers = None):
        import matplotlib.pyplot as plt
        plt.pause(0.02)
        grid = np.matrix(self.__map.grid)
        for x in range(self.__map.grid_width):
            for y in range(self.__map.grid_height):
                value = grid[x, y]
                self.__image.putpixel((x, self.__map.grid_height - 1 - y), abs(255 - (value * 255)))
        self.__ax.clear()
        self.__implot = self.__ax.imshow(self.__image)
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])
        self.__ax.plot(robot_pos.x, self.__map.grid_height - 1 - robot_pos.y, 'rs', markersize=self.__robot_size)
        if goal_point != None:
            self.__ax.plot(goal_point.x, self.__map.grid_height - 1 - goal_point.y, 'bh', markersize=4)
        if path != None:
            for point in path:
                self.__ax.plot(point.x, self.__map.grid_height - 1 - point.y, 'g+', markersize=2)
        if frontiers != None:
            index = 0
            for frontier in frontiers:
                for point in frontier:
                    color = ['gh', 'ch', 'mh', 'yh', 'kh']
                    self.__ax.plot(point.x, self.__map.grid_height - 1 - point.y, color[index % 5], markersize=2)
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
