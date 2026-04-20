# puzzlebot_gazebo

Simulation package for Puzzlebot in Gazebo Sim.

## Purpose

This package launches Gazebo, spawns the maze and robot, and bridges required topics between Gazebo and ROS 2.

## Contents

- `launch/puzzlebot_gazebo.launch.xml`: Main simulation bringup.
- `config/gazebo_bridge.yaml`: Topic bridge configuration.
- `worlds/empty_with_sensors.sdf`: Base world.
- `worlds/maze_world.world/model.sdf`: Maze model used in the project.

## Run

```bash
ros2 launch puzzlebot_gazebo puzzlebot_gazebo.launch.xml
```

Optional launch arguments:

- `headless:=true` to run without GUI.
- `use_sim_time:=true` to use simulation time.
