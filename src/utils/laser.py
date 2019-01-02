class Laser:
    """
    Class that implement the Laser datastructure, can stock the echoe distance and the angle of the laser.
    """

    def __init__(self, echoe, angle):
        """
        Instantiates a laser.
        :param echoe: Distance of the echoe.
        :type echoe: float
        :param angle: Angle of the laser.
        :type angle: float
        """
        self.echoe = echoe
        self.angle = angle

    def __str__(self):
        """
        Override of the __str__ method to be able to print out the Laser object in a nice format.
        """
        return 'echoe: ' + str(self.echoe) + 'angle: ' + str(self.angle)
