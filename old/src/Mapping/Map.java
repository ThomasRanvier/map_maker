package Mapping;

import Utils.Position;

public class Map {
    public static final double SIZE_OF_CELL_IN_METER = 1;
    public static final double DEFAULT_GRID_VALUE = 0.5;
    public static final int MAX_GRID_VALUE = 1;
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

    public Position toMapPosition(Position real_world_pos) {
        Position mapPos = this.toMapPositionNoLimits(real_world_pos);

        if (real_world_pos.getX() < this.pos_lower_left.getX()
                || real_world_pos.getX() > this.pos_upper_right.getX()
                || real_world_pos.getY() < this.pos_lower_left.getY()
                || real_world_pos.getY() > this.pos_upper_right.getY()) {
            throw new IllegalArgumentException("The coordinate of the input position is not in the limit of the Map");
        }

        return mapPos;
    }

    public Position toMapPositionNoLimits(Position real_world_pos) {
        Position mapPos = real_world_pos.clone();

        double x = (real_world_pos.getX() - this.pos_lower_left.getX()) / SIZE_OF_CELL_IN_METER - 1;
        double y = (real_world_pos.getY() - this.pos_lower_left.getY()) / SIZE_OF_CELL_IN_METER - 1;

        mapPos.setX((x < 0.0)?0.0:Math.floor(x));
        mapPos.setY((y < 0.0)?0.0:Math.floor(y));

        return mapPos;
    }

    public Position toRealWorldPosition(Position cell) {
        if (cell.getX() < 0 || cell.getX() >= this.width || cell.getY() < 0 || cell.getY() >= this.height)
            throw new IllegalArgumentException("The coordinate of the input position is not in the limit of the Map");
        return new Position(this.pos_lower_left.getX() + (cell.getX() * SIZE_OF_CELL_IN_METER), this.pos_lower_left.getY() + (cell.getY() * SIZE_OF_CELL_IN_METER));
    }

    public int getWidth() {
        return this.width;
    }

    public int getHeight() {
        return this.height;
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
