package Mapping;

import Utils.Position;

public class Map {
    public static final double SIZE_OF_CELL_IN_METER = 0.5;
    public static final double DEFAULT_GRID_VALUE = 0.5;
    public static final double MAX_GRID_VALUE = 1;
    public static final double MAX_VALUE_LASERS = 40.0;

    public double[][] grid;

    protected int width;
    protected int height;

    protected Position pos_lower_left;
    protected Position pos_upper_right;

    public Map(Position pos_lower_left, Position pos_upper_right) {
        this.pos_lower_left = pos_lower_left;
        this.pos_upper_right = pos_upper_right;
        this.width = (int)((pos_upper_right.getX() - pos_lower_left.getX()) / SIZE_OF_CELL_IN_METER);
        this.height = (int)((pos_upper_right.getY() - pos_lower_left.getY()) / SIZE_OF_CELL_IN_METER);
        this.grid = new double[width][height];

        for (int x = 0; x < this.width; x++) {
            for (int y = 0; y < this.height; y++) {
                this.grid[x][y] = DEFAULT_GRID_VALUE;
            }
        }
    }

    public Position toMapPosition (Position real_world_pos) {
        Position mapPos = real_world_pos.clone();

        if (real_world_pos.getX() < this.pos_lower_left.getX()
                || real_world_pos.getX() > this.pos_upper_right.getX()
                || real_world_pos.getY() < this.pos_lower_left.getY()
                || real_world_pos.getY() > this.pos_upper_right.getY()) {
            throw new IllegalArgumentException("The coordinate of the input position is not in the limit of the Map");
        }

        double x = (real_world_pos.getX() - this.pos_lower_left.getX()) / SIZE_OF_CELL_IN_METER - 1;
        double y = (this.pos_upper_right.getY() - real_world_pos.getY()) / SIZE_OF_CELL_IN_METER - 1;

        mapPos.setX((x < 0.0)?0.0:Math.floor(x));
        mapPos.setY((y < 0.0)?0.0:Math.floor(y));

        return mapPos;
    }

    public Position toMapPositionNoLimits (Position real_world_pos) {
        Position mapPos = real_world_pos.clone();

        double x = (real_world_pos.getX() - this.pos_lower_left.getX()) / SIZE_OF_CELL_IN_METER - 1;
        double y = (this.pos_upper_right.getY() - real_world_pos.getY()) / SIZE_OF_CELL_IN_METER - 1;

        mapPos.setX((x < 0.0)?0.0:Math.floor(x));
        mapPos.setY((y < 0.0)?0.0:Math.floor(y));

        return mapPos;
    }

    public int getWidth() {
        return this.width;
    }

    public int getHeight() {
        return this.height;
    }

    public void updateMap(Position laserPosition, double[] laserEchoes, double[] laserAngles) {
        Position laserInMap = toMapPosition(laserPosition);
        for (int i = 0; i < laserEchoes.length; i++) {
            double distance = laserEchoes[i];
            double angle = laserAngles[i];
            Position echo = getEchoPosition(laserPosition, distance, angle);
            Position echoInMap = toMapPositionNoLimits(echo);
            //Usage of toMapPositionNoLimits car même si la distance de l'echo est en dehors des limites on a
            //quand même besoin de ces coordonnées pour trouver une ligne entre les 2 points.
            updateLine(laserInMap, echoInMap, distance < MAX_VALUE_LASERS);
        }
    }

    private Position getEchoPosition(Position laserPosition, double distance, double angle) {
        return new Position(laserPosition.getX() + (distance * Math.sin(angle)),
                laserPosition.getY() + (distance * Math.cos(angle)));
    }

    private void updateLine(Position pos0, Position pos1, boolean thereIsAnObstacle) {
        //Bresenham's line algorithm
        //
        //if distance >= 40 -> Pas d'obstacle, toute la ligne passe à 0
        //if cell to update is not in boundaries stop the update
        //if cell to update == echoInMap && cell to update ->
        //if distance < 40 -> Il y a un obstacle
        //
        if (Math.abs(pos1.getYInt() - pos0.getYInt()) < Math.abs(pos1.getXInt() - pos0.getXInt())) {
            this.updateLineLow(pos0, pos1, thereIsAnObstacle);
        } else {
            this.updateLineHigh(pos0, pos1, thereIsAnObstacle);
        }
    }

    private void updateLineLow(Position pos0, Position pos1, boolean thereIsAnObstacle) {
        int dx = pos1.getXInt() - pos0.getXInt();
        int dy = Math.abs(pos1.getYInt() - pos0.getYInt());
        int D = 2 * dy - dx;
        int y = pos0.getYInt();
        int x_iterator = (pos1.getXInt() > pos0.getYInt())?-1:1;
        int y_iterator = (pos0.getYInt() > pos1.getYInt())?-1:1;

        for (int x = pos0.getXInt(); x != pos1.getXInt() + x_iterator; x+=x_iterator) {
            if (x >= 0 && y >= 0 && x < this.width && y < this.height) {
                //if (thereIsAnObstacle && x == pos1.getXInt() && y == pos1.getYInt()) {
                //    this.grid[x][y] = MAX_GRID_VALUE;
                //} else {
                    this.grid[x][y] = 0.0;
                //}
            } else {
                break;
            }
            if (D > 0) {
                y+=y_iterator;
                D -= 2 * dx;
            }
            D += 2 * dy;
        }
    }

    private void updateLineHigh(Position pos0, Position pos1, boolean thereIsAnObstacle) {
        int dx = Math.abs(pos1.getXInt() - pos0.getXInt());
        int dy = pos1.getYInt() - pos0.getYInt();
        int D = 2 * dy - dx;
        int x = pos0.getXInt();
        int x_iterator = (pos1.getXInt() > pos0.getYInt())?-1:1;
        int y_iterator = (pos0.getYInt() > pos1.getYInt())?-1:1;

        for (int y = pos0.getYInt(); x != pos1.getYInt() + y_iterator; y+=y_iterator) {
            if (x >= 0 && y >= 0 && x < this.width && y < this.height) {
                //if (thereIsAnObstacle && x == pos1.getXInt() && y == pos1.getYInt()) {
                //    this.grid[x][y] = MAX_GRID_VALUE;
                //} else {
                    this.grid[x][y] = 0.0;
                //}
            } else {
                break;
            }
            if (D > 0) {
                x+=x_iterator;
                D -= 2 * dy;
            }
            D += 2 * dx;
        }
    }
}
