# puzzlebot_navigation2

SLAM and Navigation2 package for Puzzlebot.

## Purpose

This package provides launch files, parameters, maps, and RViz profiles for:

- SLAM mapping mode.
- Localization and autonomous navigation mode.

## Contents

- `config/slam_toolbox.yaml`: SLAM Toolbox parameters.
- `config/nav2_params.yaml`: Nav2 stack parameters.
- `launch/slam.launch.xml`, `launch/slam_core.launch.xml`: SLAM bringup.
- `launch/nav2.launch.xml`, `launch/nav2_core.launch.xml`: Nav2 bringup.
- `maps/map_maze.yaml`, `maps/map_maze.pgm`: Project map assets.
- `rviz/slam.rviz`, `rviz/nav2.rviz`: RViz profiles for mapping and navigation.

## SLAM Mode

```bash
ros2 launch puzzlebot_navigation2 slam.launch.xml
```

Useful args:

- `headless:=true`
- `launch_rviz:=false`
- `launch_teleop:=true`
- `normalized_scan_restamp:=true` (only for clock-jump/bag-replay issues; keep `false` for normal SLAM to avoid timestamp skew)
- Use only one odom TF source at a time: either `bridge_diffdrive_tf:=true` or `publish_odom_tf_from_odom:=true` (not both).

Save map from SLAM:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/puzzlebot_ros2/puzzlebot_navigation2/maps/map_maze
```

## Nav2 Mode

```bash
ros2 launch puzzlebot_navigation2 nav2.launch.xml
```

Useful args:

- `headless:=true`
- `launch_rviz:=false`
- `map_path:=<absolute-or-package-map-yaml>`
