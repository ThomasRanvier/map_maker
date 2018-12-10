package Mapping;

import Utils.Position;

import java.util.Arrays;

public class Map {
    public static final double SIZE_OF_CELL_IN_METER = 1;
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
            System.out.println("Robot=" + laserPosition + " - Echo=" + echo + " - Distance=" + distance + " - Angle=" + angle);
            Position echoInMap = toMapPositionNoLimits(echo);
            //Usage of toMapPositionNoLimits car même si la distance de l'echo est en dehors des limites on a
            //quand même besoin de ces coordonnées pour trouver une ligne entre les 2 points.
            updateLine(laserInMap, echoInMap, distance < MAX_VALUE_LASERS);
        }
    }

    private Position getEchoPosition(Position laserPosition, double distance, double angle) {
        return new Position(laserPosition.getX() + (distance * Math.cos(angle)),
                laserPosition.getY() + (distance * Math.sin(angle)));
    }

    public void updateLine(Position pos0, Position pos1, boolean thereIsAnObstacle) {
        //Bresenham's line algorithm
        //
        //if distance >= 40 -> Pas d'obstacle, toute la ligne passe à 0
        //if cell to update is not in boundaries stop the update
        //if cell to update == echoInMap && cell to update ->
        //if distance < 40 -> Il y a un obstacle
        //
        if (Math.abs(pos1.getYInt() - pos0.getYInt()) < Math.abs(pos1.getXInt() - pos0.getXInt())) {
            if (pos0.getXInt() > pos1.getXInt())
                this.updateLineLow(pos1, pos0, thereIsAnObstacle);
            else
                this.updateLineLow(pos0, pos1, thereIsAnObstacle);
        } else {
            if (pos0.getYInt() > pos1.getYInt())
                this.updateLineHigh(pos1, pos0, thereIsAnObstacle);
            else
                this.updateLineHigh(pos0, pos1, thereIsAnObstacle);
        }
        if (thereIsAnObstacle && pos1.getXInt() >= 0 && pos1.getYInt() >= 0 && pos1.getXInt() < this.width && pos1.getYInt() < this.height) {
            this.grid[pos1.getXInt()][pos1.getYInt()] += 0.01;
            if (this.grid[pos1.getXInt()][pos1.getYInt()] > MAX_GRID_VALUE)
                this.grid[pos1.getXInt()][pos1.getYInt()] = MAX_GRID_VALUE;
        }
    }

    private void updateLineLow(Position pos0, Position pos1, boolean thereIsAnObstacle) {
        int dx = pos1.getXInt() - pos0.getXInt();
        int dy = pos1.getYInt() - pos0.getYInt();
        int y_iterator = 1;
        if (dy < 0) {
            y_iterator = -1;
            dy = -dy;
        }
        int D = 2 * dy - dx;
        int y = pos0.getYInt();

        for (int x = pos0.getXInt(); x <= pos1.getXInt(); x++) {
            if (x >= 0 && y >= 0 && x < this.width && y < this.height) {
                this.grid[x][y] = 0.0;
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
        int dx = pos1.getXInt() - pos0.getXInt();
        int dy = pos1.getYInt() - pos0.getYInt();
        int x_iterator = 1;
        if (dx < 0) {
            x_iterator = -1;
            dx = -dx;
        }
        int D = 2 * dx - dy;
        int x = pos0.getXInt();

        for (int y = pos0.getYInt(); y <= pos1.getYInt(); y++) {
            if (x >= 0 && y >= 0 && x < this.width && y < this.height) {
                this.grid[x][y] = 0.0;
            } else {
                return;
            }
            if (D > 0) {
                x+=x_iterator;
                D -= 2 * dy;
            }
            D += 2 * dx;
        }
    }

    @Override
    public String toString() {
        String output = "";
        for (int i = 0; i < this.grid.length; i++) {
            for (int j = 0; j < this.grid[i].length; j++) {
                output += this.grid[i][j] + "\t";
            }
            output += "\n";
        }
        return output;
    }
}
