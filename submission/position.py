class Position:
    """
    Class that implements the Position datastructure that can stock 3 dimensional coordinates and an angle.
    """
    
    def __init__(self, x = None, y = None, z = None, angle = None):
        """
        Instantiates a Position.
        :param x: x coordinate.
        :type x: float
        :param y: y coordinate.
        :type y: float
        :param z: z coordinate.
        :type z: float
        :param angle: angle.
        :type angle: float
        """
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def __str__(self):
        """
        Override of the __str__ method to be able to print out the position in a nice format, also to be able to hash the object.
        """
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

    def __eq__(self, other):
        """
        Override of the __eq__ operator to be able to compare Position objects together
        """
        is_equal = False
        if isinstance(other, Position):
            is_equal = (other.x == self.x and other.y == self.y and other.z == self.z and other.angle == self.angle)
        return is_equal

    def __hash__(self):
        """
        Override of the __hash__ method to be able to put Position objects in sets.
        """
        return hash(str(self))
