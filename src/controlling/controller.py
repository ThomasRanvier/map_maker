class Controller:
    def __init__(self, robot, robot_map):
        self.__map = robot_map
        self.__robot = robot
    
    def go_to_goal_point(self, robot_cell, goal_point):
        pass

    def turn_around(self):
        self.__robot.post_speed(2, 2)

    def stop(self):
        self.__robot.post_speed(0, 0)
