import Communications.*;
import Mapping.Laser;
import Utils.Position;

public class Robot {
    private RobotCommunication robotcomm; // communication drivers
    private LocalizationResponse lr;
    private LaserEchoesResponse ler;
    private LaserPropertiesResponse lpr;
    private DifferentialDriveRequest dr;

    /**
     * Create a robot connected to host "host" at port "port" and
     * initializes the Responses and Request.
     *
     * @param host normally http://127.0.0.1
     * @param port normally 50000
     */
    public Robot(String host, int port) {
        this.robotcomm = new RobotCommunication(host, port);
        this.lr = new LocalizationResponse();
        this.ler = new LaserEchoesResponse();
        this.lpr = new LaserPropertiesResponse();
        this.dr = new DifferentialDriveRequest();
    }

    public void move(double angularSpeed, double linearSpeed) {
        dr.setAngularSpeed(angularSpeed);
        dr.setLinearSpeed(linearSpeed);
        try {
            int rc = robotcomm.putRequest(dr);
        } catch (Exception e) {
            System.err.println("Can't put move request");
        }
    }

    public void updateInformations() {
        try {
            robotcomm.getResponse(lr);
            robotcomm.getResponse(ler);
            robotcomm.getResponse(lpr);
        } catch (Exception e) {
            System.err.println("Can't update robot informations");
        }
    }

    /**
     * Extract the robot bearing from the response
     *
     * @return angle in degrees
     */
    public double getBearingAngle() {
        double angle = lr.getHeadingAngle();
        return angle;// * 180 / Math.PI;
    }

    /**
     * Extract the robot position
     *
     * @return coordinates
     */
    public Position getRobotPosition() {
        return lr.getPosition();
    }

    public double[] getLaserEchoes() {
        return ler.getEchoes();
    }

    public Position getLaserPosition() {
        return new Position(
                this.getRobotPosition().getX() + Main.LASERS_DISTANCE * Math.cos(this.getBearingAngle()),
                this.getRobotPosition().getY() + Main.LASERS_DISTANCE * Math.sin(this.getBearingAngle())
        );
    }

    public Laser[] getLasers() {
        double[] lasersEchoes = this.getLaserEchoes();
        double[] lasersAngles = this.getLaserAngles();
        Laser[] lasers = new Laser[lasersEchoes.length];

        Position laserPosition = this.getLaserPosition();

        for (int i = 0; i < lasersEchoes.length; i++) {
            lasers[i] = new Laser(laserPosition, lasersEchoes[i], lasersAngles[i]);
        }

        return lasers;
    }

    /**
     * Get corresponding angles to each laser beam relative to the real world
     *
     * @return laser angles in radians
     */
    public double[] getLaserAngles() {
        int beamCount = (int) ((lpr.getEndAngle() - lpr.getStartAngle()) / lpr.getAngleIncrement()) + 1;
        double[] angles = new double[beamCount];
        double a = lr.getHeadingAngle() + lpr.getStartAngle();
        for (int i = 0; i < beamCount; i++) {
            /*
            if (a < -Math.PI)
                a += 2 * Math.PI;
            if (a > Math.PI)
                a -= 2 * Math.PI;
            */
            angles[i] = a;
            a += 1 * Math.PI / 180;
        }
        return angles;
    }
}
