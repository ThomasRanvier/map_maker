import Mapping.Map;
import Mapping.Mapper;
import Utils.Position;
import Utils.ShowMap;

class Main{
    public static final int SLEEP_TIME = 50;
    public static final double LASERS_DISTANCE = 0.15;

    public static void main(String[] args) throws InterruptedException {
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
        Mapper mapper = new Mapper(map, showmap);

        //robot.move(Math.PI * 0.1, 0.3);

        while (true) {
            robot.updateInformations();

            mapper.updateMap(robot.getLaserPosition(), robot.getLasers());

        }
    }
}
