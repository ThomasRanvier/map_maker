package Communications;

import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class DifferentialDriveRequest implements Request {
    private HashMap<String, Object> data;

    public DifferentialDriveRequest() {
        this(0, 0);
    }

    public DifferentialDriveRequest(double linearSpeed, double angularSpeed) {
        data = new HashMap<String, Object>();

        setLinearSpeed(linearSpeed);
        setAngularSpeed(angularSpeed);
    }

    public void setLinearSpeed(double linearSpeed) {
        data.put("TargetLinearSpeed", linearSpeed);
    }

    public void setAngularSpeed(double angularSpeed) {
        data.put("TargetAngularSpeed", angularSpeed);
    }

    public HashMap<String, Object> getData() {
        return data;
    }

    public String getPath() {
        return "/lokarria/differentialdrive";
    }

}
