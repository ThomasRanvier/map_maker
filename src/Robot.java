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
        System.out.println("Start to move robot");
        int rc = robotcomm.putRequest(dr);
        System.out.println("Response code " + rc);
    }

    public void udpateLocalization() {
        robotcomm.getResponse(lr);
    }

    /**
     * Extract the robot bearing from the response
     *
     * @return angle in degrees
     */
    public double getBearingAngle() {
        double angle = lr.getHeadingAngle();
        return angle * 180 / Math.PI;
    }

    /**
     * Extract the robot position
     *
     * @return coordinates
     */
    public Position getRobotPosition() {
        return lr.getPosition();
    }

    public void udpateLasers() {
        robotcomm.getResponse(ler);
        robotcomm.getResponse(lpr);
    }

    public double[] getLaserEchoes() {
        return ler.getEchoes();
    }

    public Position getLaserPosition() {
        return lpr.getPosition();
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
            if (a < -Math.PI)
                a += 2 * Math.PI
            if (a > Math.PI)
                a -= 2 * Math.PI
            angles[i] = a;
            a += 1 * Math.PI / 180;
        }
        return angles;
    }
}
