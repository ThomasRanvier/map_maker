from math import atan2, pi
from utils.position import Position

"""
https://github.com/encukou/bresenham/blob/master/bresenham.py
"""
def bresenham_line(self, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0
    D = 2*dy - dx
    y = 0
    for x in range(dx + 1):
        yield Position(x0 + x * xx + y * yx, y0 + x * xy + y * yy)
        if D >= 0:
            y += 1
            D -= 2*dx
            D += 2*dy

def orientation_to_angle(orientation):
    head = heading(orientation)
    return atan2(head['Y'], head['X'])

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
