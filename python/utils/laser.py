class Laser:
    def __init__(self, echoe, angle):
        self.echoe = echoe
        self.angle = angle

    def __str__(self):
        return 'echoe: ' + str(self.echoe) + 'angle: ' + str(self.angle)
