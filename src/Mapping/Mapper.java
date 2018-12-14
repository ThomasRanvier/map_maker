package Mapping;

import Utils.Position;
import Utils.ShowMap;

public class Mapper {
    private Map map;
    private ShowMap showmap;

    public Mapper(Map map, ShowMap showmap) {
        this.map = map;
        this.showmap = showmap;
    }

    public void updateMap(Position laserPosition, double[] laserEchoes, double[] laserAngles) {
        Position laserInMap = this.map.toMapPosition(laserPosition);
        for (int i = 0; i < laserEchoes.length; i++) {
            double distance = laserEchoes[i];
            double angle = laserAngles[i];
            Position echoPosition = getEchoPosition(laserPosition, distance, angle);
            Position echoInMap = this.map.toMapPositionNoLimits(echoPosition);
            updateLine(laserInMap, echoInMap, distance);
        }
        this.showmap.updateMap(this.map.grid, laserInMap.getYInt(), laserInMap.getXInt());
    }

    private Position getEchoPosition(Position laserPosition, double distance, double angle) {
        return new Position(laserPosition.getX() + (distance * Math.cos(angle)),
                laserPosition.getY() + (distance * Math.sin(angle)));
    }

    private double bayesianProbability(double occupiedProbablity, double previousProbability) {
        double emptyProbability = 1 - occupiedProbablity;
        double emptyPreviousProbability = 1 - previousProbability;
        return (occupiedProbablity * previousProbability) / (occupiedProbablity * previousProbability + emptyProbability * emptyPreviousProbability);
    }

    /*
     * Updates the values of the grid in a line between the two points, uses Bresenham's line algorithm.
     *
     * @param pos0 First point
     * @param pos1 Second point
     * @param thereIsAnObstacle True if the laser detected an obstacle, false otherwise
     */
    public void updateLine(Position pos0, Position pos1, double distance) {
        boolean thereIsAnObstacle = (distance < Map.MAX_VALUE_LASERS);
        if (Math.abs(pos1.getYInt() - pos0.getYInt()) < Math.abs(pos1.getXInt() - pos0.getXInt())) {
            if (pos0.getXInt() > pos1.getXInt())
                this.updateLineLow(pos1, pos0);
            else
                this.updateLineLow(pos0, pos1);
        } else {
            if (pos0.getYInt() > pos1.getYInt())
                this.updateLineHigh(pos1, pos0);
            else
                this.updateLineHigh(pos0, pos1);
        }
        if (thereIsAnObstacle && pos1.getXInt() >= 0 && pos1.getYInt() >= 0 && pos1.getXInt() < this.map.width && pos1.getYInt() < this.map.height) {
            double occupiedProbability = getOccupiedProbability(distance);
            if (this.map.grid[pos1.getXInt()][pos1.getYInt()] <= 0.7)
                this.map.grid[pos1.getXInt()][pos1.getYInt()] += 0.01;
            this.map.grid[pos1.getXInt()][pos1.getYInt()] = bayesianProbability(occupiedProbability, this.map.grid[pos1.getXInt()][pos1.getYInt()]);
        }
    }

    private void updateLineLow(Position pos0, Position pos1) {
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
            if (x >= 0 && y >= 0 && x < this.map.width && y < this.map.height) {
                Position pos0InRealWorld = this.map.toRealWorldPosition(pos0);
                Position pos1InRealWorld = this.map.toRealWorldPosition(pos1);
                double distance = Math.sqrt(Math.pow(pos0InRealWorld.getX() - pos1InRealWorld.getX(), 2) + Math.pow(pos0InRealWorld.getY() - pos1InRealWorld.getY(), 2));
                if (distance < MAX_VALUE_LASERS - 10) {
                    double occupiedProbability = getOccupiedProbability(distance);
                    this.map.grid[x][y] = bayesianProbability(1 - occupiedProbability, this.map.grid[x][y]);
                }
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

    private void updateLineHigh(Position pos0, Position pos1) {
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
            if (x >= 0 && y >= 0 && x < this.map.width && y < this.map.height) {
                Position pos0InRealWorld = this.map.toRealWorldPosition(pos0);
                Position pos1InRealWorld = this.map.toRealWorldPosition(pos1);
                double distance = Math.sqrt(Math.pow(pos0InRealWorld.getX() - pos1InRealWorld.getX(), 2) + Math.pow(pos0InRealWorld.getY() - pos1InRealWorld.getY(), 2));
                if (distance < MAX_VALUE_LASERS - 10) {
                    double occupiedProbability = getOccupiedProbability(distance);
                    this.map.grid[x][y] = bayesianProbability(1 - occupiedProbability, this.map.grid[x][y]);
                }
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

    private double getOccupiedProbability(double distance) {
        return (((Map.MAX_VALUE_LASERS - distance) / Map.MAX_VALUE_LASERS) + 1) / 2 * 0.98;
    }
}
