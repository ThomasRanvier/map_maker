from math import atan2, pi
from utils.position import Position

"""
http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
"""
def bresenham_line(x1, y1, x2, y2):
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
    return (pos_2.x - pos_1.x)**2 + (pos_2.y - pos_1.y)**2

def centroid(points):
    count = 0.0
    x_sum = 0.0
    y_sum = 0.0
    for point in points:
        x_sum += point.x
        y_sum += point.y
        count += 1.0
    return Position(x_sum / count, y_sum / count)

def von_neumann_neighbourhood(cell, grid_width, grid_height):
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
    neighbours = []
    if cell.x > 0:
        neighbours.append(Position(cell.x - 1, cell.y))
    if cell.y > 0:
        neighbours.append(Position(cell.x, cell.y - 1))
    if cell.x < grid_width - 1:
        neighbours.append(Position(cell.x + 1, cell.y))
    if cell.y < grid_height - 1:
        neighbours.append(Position(cell.x, cell.y + 1))
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
