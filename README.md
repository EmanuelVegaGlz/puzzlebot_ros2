# Puzzlebot ROS 2 Workspace

This repository contains a ROS 2 Humble simulation and navigation stack for a differential-drive Puzzlebot running in Gazebo Sim.

The workspace is organized as a multi-package ROS 2 project and supports two operational modes (phases):

1. **Phase 1: SLAM / Mapping** using `slam_toolbox`.
2. **Phase 2: Localization + Navigation** using Navigation2 (Nav2) with a prebuilt map.

---

## 1) System Description

The system simulates a Puzzlebot with:

- Differential drive kinematics (`/cmd_vel` -> wheel motion).
- 2D LiDAR (`/scan`) for mapping and localization.
- Odometry (`/odom`) and TF tree (`map`, `odom`, `base_footprint`, `base_link`, laser frame).
- Maze environment spawned in Gazebo Sim.

The repository is **configuration-driven**:

- Launch orchestration is done with ROS 2 XML launch files.
- Robot/world definitions are in URDF/SDF.
- Runtime behavior is configured in YAML (bridge, SLAM, Nav2, maps).

There are no custom C++/Python nodes in this workspace; behavior is built by composing standard ROS 2 packages.

---

## 2) Repository and Workspace Structure

### Top-level workspace

- `puzzlebot_description/`: Robot model, meshes, RViz view, and robot-state launch.
- `puzzlebot_gazebo/`: Gazebo world launch, simulator bridge config, and world assets.
- `puzzlebot_navigation2/`: SLAM and Nav2 launch/config/maps for both phases.
- `build/`, `install/`, `log/`: Colcon-generated build artifacts.

### Package breakdown

#### `puzzlebot_description`

Purpose:

- Defines the Puzzlebot physical model and publishes robot description/TF.

Key contents:

- `urdf/puzzlebot.urdf`: Robot links, joints, lidar sensor, diff-drive Gazebo systems.
- `meshes/`: Visual mesh assets.
- `rviz/`: RViz config for model visualization.
- `launch/puzzlebot_description.launch.xml`: Publishes `robot_description` and optional RViz/Gazebo helpers.

#### `puzzlebot_gazebo`

Purpose:

- Starts Gazebo Sim world, spawns maze and robot, and bridges Gazebo <-> ROS 2 topics.

Key contents:

- `launch/puzzlebot_gazebo.launch.xml`: Main simulator launch.
- `config/gazebo_bridge.yaml`: Bridge rules for `/clock`, `/cmd_vel`, `/odom`, `/tf`, `/joint_states`, `/scan`.
- `worlds/empty_with_sensors.sdf`: Base world.
- `worlds/maze_world.world/model.sdf`: Maze model spawned at runtime.

#### `puzzlebot_navigation2`

Purpose:

- Implements both phase entry points:
  - SLAM mapping workflow.
  - Nav2 localization/planning/control workflow.

Key contents:

- Launch:
  - `launch/slam.launch.xml`, `launch/slam_core.launch.xml`
  - `launch/nav2.launch.xml`, `launch/nav2_core.launch.xml`
- Config:
  - `config/slam_toolbox.yaml`
  - `config/nav2_params.yaml`
- Maps:
  - `maps/map_maze.yaml` + `maps/map_maze.pgm`
  - `maps/my_maze.yaml` + `maps/my_maze.pgm`
- RViz:
  - `rviz/slam.rviz`
  - `rviz/nav2.rviz`

---

## 3) Prerequisites

### Platform

- Ubuntu 22.04.5 LTS
- ROS 2 Humble (`ROS_DISTRO=humble`)

### Tooling

- Python: 3.10.12
- CMake: 3.22.1
- colcon-core: 0.20.1
- ros2cli: 0.18.18
- Gazebo Sim (`gz sim`): 7.0.0
- Ignition Gazebo shim (`ign gazebo`): 6.17.0

### ROS packages (tested versions)

- `ros-humble-navigation2`: 1.1.20-1jammy.20260326.171707
- `ros-humble-nav2-bringup`: 1.1.20-1jammy.20260326.184223
- `ros-humble-slam-toolbox`: 2.6.10-1jammy.20260326.170116
- `ros-humble-ros-gz-sim`: 0.244.23-1jammy.20260325.234248
- `ros-humble-ros-gz-bridge`: 0.244.23-1jammy.20260326.131207
- `ros-humble-rviz2`: 11.2.26-1jammy.20260326.171215
- `ros-humble-teleop-twist-keyboard`: 2.4.1-1jammy.20260310.172413
- `ros-humble-xacro`: 2.1.1-1jammy.20260307.132851

### Typical installation

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-ros-gz-sim \
  ros-humble-ros-gz-bridge \
  ros-humble-teleop-twist-keyboard \
  ros-humble-xacro \
  python3-colcon-common-extensions
```

> Note: If your distro package versions differ, launches should still work as long as APIs are compatible with ROS 2 Humble.

---

## 4) Build and Setup

From workspace root:

```bash
cd ~/puzzlebot_ros2
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Optional check:

```bash
ros2 pkg list | grep -E "puzzlebot_description|puzzlebot_gazebo|puzzlebot_navigation2"
```

---

## 5) Usage Modes (Phases)

### Phase 1: SLAM / Mapping

Goal:

- Drive the robot in the maze and generate a 2D occupancy map.

Launch:

```bash
source /opt/ros/humble/setup.bash
source ~/puzzlebot_ros2/install/setup.bash
ros2 launch puzzlebot_navigation2 slam.launch.xml launch_teleop:=true
```

What this phase launches:

- Gazebo world + maze + robot (`puzzlebot_gazebo`).
- `slam_toolbox` in mapping mode.
- RViz with SLAM visualization.
- Optional keyboard teleop (enabled above).

How to operate:

1. Use teleop terminal instructions to move through all maze corridors.
2. In RViz, verify map is being built from `/scan` and TF is stable.
3. Save map when finished.

Save a map:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/puzzlebot_ros2/puzzlebot_navigation2/maps/my_maze
```

This generates:

- `my_maze.pgm`
- `my_maze.yaml`

You can then use this map in Phase 2 with `map_path:=.../my_maze.yaml`.

### Phase 2: Localization + Navigation (Nav2)

Goal:

- Localize in a known map and navigate to goal poses.

Launch:

```bash
source /opt/ros/humble/setup.bash
source ~/puzzlebot_ros2/install/setup.bash
ros2 launch puzzlebot_navigation2 nav2.launch.xml
```

Optional map override:

```bash
ros2 launch puzzlebot_navigation2 nav2.launch.xml \
  map_path:=~/puzzlebot_ros2/puzzlebot_navigation2/maps/my_maze.yaml
```

What this phase launches:

- Gazebo world + maze + robot.
- Nav2 bringup (AMCL, planner, controller, behavior tree navigator, costmaps).
- RViz for localization and goal-based navigation.

How to operate:

1. In RViz, set an initial pose (`2D Pose Estimate`).
2. Wait until AMCL converges.
3. Send a navigation goal (`Nav2 Goal` / `2D Goal Pose`).
4. Monitor path and local planner behavior.

---

## 6) Key Runtime Interfaces

Important bridged topics:

- `/cmd_vel` (ROS -> Gazebo)
- `/odom` (Gazebo -> ROS)
- `/scan` (Gazebo -> ROS)
- `/tf` via Gazebo diff-drive TF
- `/clock` (simulation time)
- `/joint_states` (Gazebo model joint state -> ROS)

Important launch arguments:

- `headless:=true|false` (Gazebo GUI off/on)
- `use_sim_time:=true|false`
- `launch_teleop:=true|false` (SLAM phase)
- `teleop_use_xterm:=true|false` (SLAM phase)
- `map_path:=...` (Nav2 phase)
- `nav2_params_file:=...`
- `slam_params_file:=...`

---

## 7) Troubleshooting Notes

- **Gazebo world loading error**: Ensure Gazebo is launched with a world SDF and maze is spawned as a model; passing a model SDF as a world can fail.
- **No AMCL particles/pose**: In Nav2 phase, set initial pose in RViz and verify map server + AMCL are active.
- **Map server image errors**: Confirm `.pgm` files are valid binary Netpbm images (not comma-separated text bytes).
- **TF old data / unstable transforms**: Kill stale Gazebo processes and relaunch with isolated partition variables if needed.

Helpful cleanup command:

```bash
pkill -f "gz sim|ign gazebo"
```

---

## 8) Suggested Development Workflow

1. Build and source workspace.
2. Run Phase 1 to create/update map.
3. Validate map files in `puzzlebot_navigation2/maps/`.
4. Run Phase 2 with the selected map.
5. Tune `config/nav2_params.yaml` and `config/slam_toolbox.yaml` as needed.

---

## 9) Current Repository State Summary

- Branch: `main`
- Workspace type: ROS 2 colcon workspace with three packages.
- Primary entry points:
  - `ros2 launch puzzlebot_navigation2 slam.launch.xml`
  - `ros2 launch puzzlebot_navigation2 nav2.launch.xml`
