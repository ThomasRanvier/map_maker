
class Main{
    public static void main(String[] args) {
        Robot robot = new Robot("http://itchy.cs.umu.se", 50000);
        Map map = new Map(new Position(-5, -5), new Position(5, 5));
        ShowMap showmap = new ShowMap(map.getHeight, map.getWidth, true);

        robot.move(Math.PI * 0.2, 0.3);

        while (true) {
            robot.updateLocalization();
            Position robotPosition = robot.getRobotPosition();
            Position robotPositionInMap = map.toMapPosition(robotPosition);
            double robotAngle = robot.getBearingAngle();
            System.out.println("Robot position: x: " + robotPosition.getX() + ", y:" + robotPosition.getY());
            System.out.println("Robot position on map: x: " + robotPositionInMap.getX() + ", y:" + robotPositionInMap.getY());
            System.out.println("Robot angle: " + robotAngle);

            robot.updateLasers();
            Position laserPosition robot.getLaserPosition();
            System.out.println("Lasers position: x: " + robotPosition.getX() + ", y:" + robotPosition.getY());
            double[] laserEchoes = robot.getLaserEchoes();
            double[] laserAngles = robot.getLaserAngles();
            System.out.println("Object at " + laserEchoes[56] + "m in " + laserAngles[56] * 180.0 / Math.PI + " degrees");
            map.updateMap(laserPosition, laserEchoes, laserAngles)

            showmap.updateMap(map.getGrid(), (int)robotPositionInMap.getY(), (int)robotPositionInMap.getX());
        }
    }
}
