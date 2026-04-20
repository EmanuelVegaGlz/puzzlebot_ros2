# puzzlebot_description

Robot description package for Puzzlebot.

## Purpose

This package contains the robot model and visualization assets used by simulation and navigation.

## Contents

- `urdf/puzzlebot.urdf`: Main robot model.
- `meshes/`: Visual mesh files.
- `rviz/puzzlebot_rviz.rviz`: Robot inspection RViz profile.
- `launch/puzzlebot_description.launch.xml`: Publishes `robot_description` and TF.

## Run

```bash
ros2 launch puzzlebot_description puzzlebot_description.launch.xml
```

Optional launch arguments:

- `rviz:=true` to open RViz.
- `gazebo:=true` to open Gazebo with an empty world and spawn the robot.
- `joint_gui:=true` to use `joint_state_publisher_gui`.
- `use_sim_time:=true` to use simulation time.
