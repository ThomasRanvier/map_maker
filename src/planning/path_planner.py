from utils.position import Position

class PathPlanner:
    def __init__(self, robot_map):
        self.__map = robot_map

    def get_path(self, robot_pos, goal_point):
        robot_cell = self.__map.to_grid_pos(Position(robot_pos.x, robot_pos.y))
        path = [robot_cell]
        
        return None
