# map maker

This is an AI project, the point is to implement an algorithm that will make a virtual robot (using MRDS) discover its environment while creating an internal map of it.

Our implementation uses a Wavefront Frontiers Detector algorithm and the Bresenham's line algorithm to build the map around the robot by reading the laser echoes.
It then selects the closest frontier and compute its centroid to define the goal, a path is built between the robot and the goal using the A\* algorithm.
To follow the path it uses a potential field, in that way it follows the path while avoiding the obstacles around.

For references and more details see our report under the report directory.
