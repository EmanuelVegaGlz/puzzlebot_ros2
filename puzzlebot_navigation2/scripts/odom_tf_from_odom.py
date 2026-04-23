#!/usr/bin/env python3

import math

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from tf2_ros import TransformBroadcaster


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def yaw_from_quaternion(x: float, y: float, z: float, w: float) -> float:
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


def quaternion_from_yaw(yaw: float) -> tuple[float, float, float, float]:
    half_yaw = 0.5 * yaw
    return (0.0, 0.0, math.sin(half_yaw), math.cos(half_yaw))


class OdomTfFromOdomNode(Node):
    def __init__(self) -> None:
        super().__init__("odom_tf_from_odom")

        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("parent_frame", "odom")
        self.declare_parameter("child_frame", "base_footprint")
        self.declare_parameter("use_odom_header_frames", True)
        self.declare_parameter("smoothing_alpha", 1.0)

        self.odom_topic = str(self.get_parameter("odom_topic").value)
        self.parent_frame = str(self.get_parameter("parent_frame").value)
        self.child_frame = str(self.get_parameter("child_frame").value)
        self.use_odom_header_frames = bool(self.get_parameter("use_odom_header_frames").value)
        self.smoothing_alpha = clamp(float(self.get_parameter("smoothing_alpha").value), 0.0, 1.0)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=50,
            durability=DurabilityPolicy.VOLATILE,
        )

        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(Odometry, self.odom_topic, self.odom_callback, qos)

        self.initialized = False
        self.last_x = 0.0
        self.last_y = 0.0
        self.last_z = 0.0
        self.last_yaw = 0.0

        self.get_logger().info(
            f"Publishing odom TF from {self.odom_topic} with alpha={self.smoothing_alpha:.3f}"
        )

    def odom_callback(self, msg: Odometry) -> None:
        parent_frame = self.parent_frame
        child_frame = self.child_frame

        if self.use_odom_header_frames:
            if msg.header.frame_id:
                parent_frame = msg.header.frame_id
            if msg.child_frame_id:
                child_frame = msg.child_frame_id

        if not parent_frame or not child_frame:
            return

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z

        q = msg.pose.pose.orientation
        yaw = yaw_from_quaternion(q.x, q.y, q.z, q.w)

        if not self.initialized:
            smoothed_x = x
            smoothed_y = y
            smoothed_z = z
            smoothed_yaw = yaw
            self.initialized = True
        else:
            alpha = self.smoothing_alpha
            smoothed_x = self.last_x + alpha * (x - self.last_x)
            smoothed_y = self.last_y + alpha * (y - self.last_y)
            smoothed_z = self.last_z + alpha * (z - self.last_z)

            yaw_delta = math.atan2(math.sin(yaw - self.last_yaw), math.cos(yaw - self.last_yaw))
            smoothed_yaw = self.last_yaw + alpha * yaw_delta

        self.last_x = smoothed_x
        self.last_y = smoothed_y
        self.last_z = smoothed_z
        self.last_yaw = smoothed_yaw

        tx = TransformStamped()
        tx.header.stamp = msg.header.stamp
        tx.header.frame_id = parent_frame
        tx.child_frame_id = child_frame
        tx.transform.translation.x = smoothed_x
        tx.transform.translation.y = smoothed_y
        tx.transform.translation.z = smoothed_z

        qx, qy, qz, qw = quaternion_from_yaw(smoothed_yaw)
        tx.transform.rotation.x = qx
        tx.transform.rotation.y = qy
        tx.transform.rotation.z = qz
        tx.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(tx)


def main() -> None:
    rclpy.init()
    node = OdomTfFromOdomNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
