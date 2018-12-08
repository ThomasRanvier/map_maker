package Communications;

import Utils.Position;
import Utils.Quaternion;

import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

/**
 * Returns a orientation and position
 *
 * @author Thomas Johansson
 * <p>
 * Updated by Ola Ringdahl 2015-12-16 (added convert2double)
 */

public class LocalizationResponse implements Response {
    private Map<String, Object> data;

    public void setData(Map<String, Object> data) {
        this.data = data;
    }

    public Quaternion getOrientation() {
        Map<String, Object> pose = (Map<String, Object>) data.get("Pose");
        Map<String, Object> orientation = (Map<String, Object>) pose.get("Orientation");

        double w = RobotCommunication.convert2Double(orientation.get("W"));
        double x = RobotCommunication.convert2Double(orientation.get("X"));
        double y = RobotCommunication.convert2Double(orientation.get("Y"));
        double z = RobotCommunication.convert2Double(orientation.get("Z"));

        return new Quaternion(w, x, y, z);
    }

    public Position getPosition() {
        Map<String, Object> pose = (Map<String, Object>) data.get("Pose");
        Map<String, Object> position = (Map<String, Object>) pose.get("Position");

        double x = RobotCommunication.convert2Double(position.get("X"));
        double y = RobotCommunication.convert2Double(position.get("Y"));
        double z = RobotCommunication.convert2Double(position.get("Z"));

        return new Position(x, y, z);
    }

    public double getHeadingAngle() {
        Quaternion q = this.getOrientation();
        Position v = q.bearing();

        return Math.atan2(v.getY(), v.getX());
    }

    public int getStatus() {
        return (Integer) data.get("Status");
    }

    public String getPath() {
        return "/lokarria/localization";
    }

    public long getTimestamp() {
        return (Long) data.get("TimeStamp");
    }

}
