import Mapping.Map;
import Utils.Position;
import Utils.ShowMap;

class Main{
    public static void main(String[] args) {
        String host = args[0];
        int port = Integer.parseInt(args[1]);
        int x_lower_left = -10, y_lower_left = -10, x_upper_right = 10, y_upper_right = 10;
        boolean show_gui = true;
        if (args.length >= 6) {
            x_lower_left = Integer.parseInt(args[2]);
            y_lower_left = Integer.parseInt(args[3]);
            x_upper_right = Integer.parseInt(args[4]);
            y_upper_right = Integer.parseInt(args[5]);
        }
        if (args.length >= 7) {
            show_gui = Boolean.parseBoolean(args[6]);
        }

        Robot robot = new Robot(host, port);
        Map map = new Map(new Position(x_lower_left, y_lower_left), new Position(x_upper_right, y_upper_right));
        ShowMap showmap = new ShowMap(map.getHeight(), map.getWidth(), show_gui);

        //robot.move(Math.PI * 0.1, 0.3);

        while (true) {
            robot.updateLocalization();
            Position robotPosition = robot.getRobotPosition();
            Position robotPositionInMap = map.toMapPosition(robotPosition);
            double robotAngle = robot.getBearingAngle();
            System.out.println("Robot position: x: " + robotPosition.getX() + ", y:" + robotPosition.getY());
            System.out.println("Robot position on map: x: " + robotPositionInMap.getX() + ", y:" + robotPositionInMap.getY());
            System.out.println("Robot angle: " + robotAngle);

            robot.updateLasers();
            Position laserPosition = robot.getLaserPosition();
            System.out.println("Lasers position: x: " + robotPosition.getX() + ", y:" + robotPosition.getY());
            double[] laserEchoes = robot.getLaserEchoes();
            double[] laserAngles = robot.getLaserAngles();
            System.out.println("Object at " + laserEchoes[56] + "m in " + laserAngles[56] * 180.0 / Math.PI + " degrees");
            map.updateMap(laserPosition, laserEchoes, laserAngles);

            showmap.updateMap(map.grid, (int) robotPositionInMap.getY(), (int) robotPositionInMap.getX());
        }
    }
}
