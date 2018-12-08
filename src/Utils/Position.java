package Utils;

public class Position {
    public double x;
    public double y;
    public double z;

    public Position() {
        this(0.0, 0.0);
    }

    public Position(double x, double y) {
        this(x, y, 0.0);
    }

    public Position(double x, double y, double z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }

    public double getZ() {
        return z;
    }

    public void setZ(double z) {
        this.z = z;
    }

    public int getXInt() {
        return Double.valueOf(this.x).intValue();
    }

    public int getYInt() {
        return Double.valueOf(this.y).intValue();
    }

    public int getZInt() {
        return Double.valueOf(this.z).intValue();
    }

    public double getDistanceTo(Position p) {
        return Math.sqrt((x - p.x) * (x - p.x) + (y - p.y) * (y - p.y));
    }

    // bearing relative 'north'
    public double getBearingTo(Position p) {
        return Math.atan2(p.y - y, p.x - x);
    }

    public Position clone() {
        return new Position(this.getX(), this.getY(), this.getZ());
    }
}
