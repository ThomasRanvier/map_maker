class Position:
    def __init__(self, x = None, y = None, z = None, angle = None):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def __str__(self):
        string = 'Empty position'
        if self.x != None:
            string = ' x: ' + str(self.x)
        if self.y != None:
            string += ' y: ' + str(self.y)
        if self.z != None:
            string += ' z: ' + str(self.z)
        if self.angle != None:
            string += ' angle: ' + str(self.angle)
        return string
