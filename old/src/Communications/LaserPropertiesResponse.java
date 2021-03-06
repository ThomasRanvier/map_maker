package Communications;

import Utils.Position;
import Utils.Quaternion;

import java.util.Map;

public class LaserPropertiesResponse implements Response {
    private Map<String, Object> data;

    public void setData(Map<String, Object> data) {
        this.data = data;
    }

    public Quaternion getOrientation() {
        Map<String, Object> pose = (Map<String, Object>) data.get("Pose");
        Map<String, Object> orientation = (Map<String, Object>) pose
                .get("Orientation");

        double w = (Double) orientation.get("W");
        double x = (Double) orientation.get("X");
        double y = (Double) orientation.get("Y");
        double z = (Double) orientation.get("Z");

        return new Quaternion(w, x, y, z);
    }

    public Position getPosition() {
        Map<String, Object> pose = (Map<String, Object>) data.get("Pose");
        Map<String, Object> position = (Map<String, Object>) pose
                .get("Position");
        double x, y, z = 0;
        if (position.get("X") instanceof Integer) {
            // System.out.println("Integer.....");
            x = ((Integer) position.get("X")).doubleValue();
        } else {
            x = (Double) position.get("X");
        }
        if (position.get("Y") instanceof Integer) {
            // System.out.println("Integer.....");
            y = ((Integer) position.get("Y")).doubleValue();
        } else {
            y = (Double) position.get("Y");
        }
        if (position.get("Z") instanceof Integer) {
            // System.out.println("Integer.....");
            z = ((Integer) position.get("Z")).doubleValue();
        } else {
            z = (Double) position.get("Z");
        }
        // double y = (Double) position.get("Y");
        // double z = (Double) position.get("Z");

        return new Position(x, y, z);
    }

    /**
     * @return Angle of the first beam in radians
     */
    public double getStartAngle() {
        return (Double) data.get("StartAngle");
    }

    /**
     * @return Angle of the last beam in radians
     */
    public double getEndAngle() {
        return (Double) data.get("EndAngle");
    }

    /**
     * @return Angle increment in radians
     */
    public double getAngleIncrement() {
        return (Double) data.get("AngleIncrement");
    }

    public String getPath() {
        return "/lokarria/laser/properties";
    }

    public long getTimestamp() {
        return 0;
    }

}
