package Mapping;

import Utils.Position;

public class Laser {
    private static final int MAX_DISTANCE_LASER = 40;

    public Position realWorldPosition;

    public double distance;

    public double angle;

    public Laser(Position laserPosition, double distance, double angle) {
        this.distance = distance;
        this.angle = angle;
        this.calculateRealPosition(laserPosition);
    }

    private void calculateRealPosition(Position laserPosition) {
        this.realWorldPosition = new Position(
                laserPosition.getX() + this.distance * Math.cos(this.angle),
                laserPosition.getY() + this.distance * Math.sin(this.angle)
        );
    }

    public Position getGridPosition(Map map) {
        return map.toMapPosition(this.realWorldPosition);
    }
}
