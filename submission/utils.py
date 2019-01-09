from math import atan2, pi
from position import Position

def get_deltas(points, max_pos):
    """
    The function used to compute the deltas in x and y axis.
    :param points: The list of the points.
    :type points: A list of Position objects.
    :param max_pos: The number of positions to compare.
    :type max_pos: float
    """
    min_x = points[len(points) - 1].x
    max_x = min_x
    min_y = points[len(points) - 1].y
    max_y = min_y
    for i in range(len(points) - 1 - max_pos, len(points) - 1):
        if min_x > points[i].x:
            min_x = points[i].x
        if min_y > points[i].y:
            min_y = points[i].y
        if max_x < points[i].x:
            max_x = points[i].x
        if max_y < points[i].y:
            max_y = points[i].y
    return (abs(max_x - min_x), abs(max_y - min_y))

def filled_midpoint_circle(x_center, y_center, radius):
    """
    https://stackoverflow.com/questions/10878209/midpoint-circle-algorithm-for-filled-circles
    This function is an implementation of the algorithm that can be found above.
    It gives the user a list of all the points in a circle of a defined radius and a defined center.
    :param x_center: X coordinate of the center of the circle.
    :type x_center: integer
    :param y_center: Y coordinate of the center of the circle.
    :type y_center: integer
    :param radius: Radius of the circle.
    :type radius: integer
    :return: A list of all the points that compose the circle.
    :rtype: A list of Position objects.
    """
    x = radius
    y = 0
    radius_err = 1 - x
    circle = []
    while x >= y:
        start_x = -x + x_center
        end_x = x + x_center
        for ix in range(start_x, end_x + 1):
            circle.append(Position(ix, y + y_center))
        if y != 0:
            for ix in range(start_x, end_x + 1):
                circle.append(Position(ix, -y + y_center))
        y += 1
        if radius_err < 0:
            radius_err += 2 * y + 1
        else:
            if x >= y:
                start_x = -y + 1 + x_center
                end_x = y - 1 + x_center
                for ix in range(start_x, end_x + 1):
                    circle.append(Position(ix, x + y_center))
                    circle.append(Position(ix, -x + y_center))
            x -= 1
            radius_err += 2 * (y - x + 1)
    return circle

def bresenham_line(x1, y1, x2, y2):
    """
    http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    This function is a slightly modified version of the algorithm that can be found above.
    It gives the user a list of all the points that are in a line between the 2 given points.
    :param x1: X coordinate of the first point.
    :type x1: integer
    :param y1: Y coordinate of the first point.
    :type y1: integer
    :param x2: X coordinate of the second point.
    :type x2: integer
    :param y2: Y coordinate of the second point.
    :type y2: integer
    :return: A list of the points that compose the line.
    :rtype: A list of Position objects.
    """
    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = Position(y, x) if is_steep else Position(x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if swapped:
        points.reverse()
    return points

def distance_2(pos_1, pos_2):
    """
    This functions gives the square distance between two positions.
    :param pos_1: First position.
    :type pos_1: Position
    :param pos_2: Second position.
    :type pos_2: Position
    :return: Square distance
    :rtype: float
    """
    return (pos_2.x - pos_1.x)**2 + (pos_2.y - pos_1.y)**2

def centroid(points):
    """
    Computes the centroid of the list of points.
    :param points: A list of points.
    :type points: A list of Position objects.
    :return: The position of the centroid.
    :rtype: Position
    """
    count = 0.0
    x_sum = 0.0
    y_sum = 0.0
    for point in points:
        x_sum += point.x
        y_sum += point.y
        count += 1.0
    return Position(x_sum / count, y_sum / count)

def von_neumann_neighbourhood(cell, grid_width, grid_height):
    """
    Gives the cells of the Von Neumann neighbourhood of the cell.
    :param cell: The cell that we want the neighbourhood of.
    :type cell: Position
    :param grid_width: The width of the grid.
    :type grid_width: integer
    :param grid_height: The height of the grid.
    :type grid_height: integer
    :return: A list of the neighbours.
    :rtype: A list of Position objects.
    """
    neighbours = []
    if cell.x > 0:
        neighbours.append(Position(cell.x - 1, cell.y))
    if cell.y > 0:
        neighbours.append(Position(cell.x, cell.y - 1))
    if cell.x < grid_width - 1:
        neighbours.append(Position(cell.x + 1, cell.y))
    if cell.y < grid_height - 1:
        neighbours.append(Position(cell.x, cell.y + 1))
    return neighbours

def moore_neighbourhood(cell, grid_width, grid_height):
    """
    Gives the cells of the Moore neighbourhood of the cell.
    :param cell: The cell that we want the neighbourhood of.
    :type cell: Position
    :param grid_width: The width of the grid.
    :type grid_width: integer
    :param grid_height: The height of the grid.
    :type grid_height: integer
    :return: A list of the neighbours.
    :rtype: A list of Position objects.
    """
    neighbours = von_neumann_neighbourhood(cell, grid_width, grid_height)
    if cell.x > 0 and cell.y > 0:
        neighbours.append(Position(cell.x - 1, cell.y - 1))
    if cell.x > 0 and cell.y < grid_height - 1:
        neighbours.append(Position(cell.x - 1, cell.y + 1))
    if cell.x < grid_width - 1 and cell.y > 0:
        neighbours.append(Position(cell.x + 1, cell.y - 1))
    if cell.x < grid_width - 1 and cell.y < grid_height - 1:
        neighbours.append(Position(cell.x + 1, cell.y + 1))
    return neighbours

def orientation_to_angle(orientation):
    """
    Converts the orientation of the robot into an angle in radians.
    :param orientation: Orientation of the robot.
    :type orientation: Orientation of the robot.
    :return: The angle in radians.
    :rtype: float
    """
    head = heading(orientation)
    angle = atan2(head['Y'], head['X'])
    while angle > pi:
        angle -= 2.0 * pi
    while angle < -pi:
        angle += 2.0 * pi
    return angle

def heading(q):
    return rotate(q, {'X': 1.0, 'Y': 0.0, "Z": 0.0})

def rotate(q, v):
    return vector(qmult(qmult(q, quaternion(v)), conjugate(q)))

def quaternion(v):
    q = v.copy()
    q['W'] = 0.0
    return q

def vector(q):
    v = {}
    v["X"] = q["X"]
    v["Y"] = q["Y"]
    v["Z"] = q["Z"]
    return v

def conjugate(q):
    qc = q.copy()
    qc["X"] = -q["X"]
    qc["Y"] = -q["Y"]
    qc["Z"] = -q["Z"]
    return qc

def qmult(q1, q2):
    q = {}
    q["W"] = q1["W"] * q2["W"] - q1["X"] * q2["X"] - q1["Y"] * q2["Y"] - q1["Z"] * q2["Z"]
    q["X"] = q1["W"] * q2["X"] + q1["X"] * q2["W"] + q1["Y"] * q2["Z"] - q1["Z"] * q2["Y"]
    q["Y"] = q1["W"] * q2["Y"] - q1["X"] * q2["Z"] + q1["Y"] * q2["W"] + q1["Z"] * q2["X"]
    q["Z"] = q1["W"] * q2["Z"] + q1["X"] * q2["Y"] - q1["Y"] * q2["X"] + q1["Z"] * q2["W"]
    return q
