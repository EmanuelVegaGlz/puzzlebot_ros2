#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan


class ScanFrameNormalizerNode(Node):
    def __init__(self) -> None:
        super().__init__("scan_frame_normalizer")

        self.declare_parameter("input_topic", "/scan")
        self.declare_parameter("output_topic", "/scan_aligned")
        self.declare_parameter("output_frame_id", "laser_link")
        self.declare_parameter("restamp_with_now", False)

        self.input_topic = str(self.get_parameter("input_topic").value)
        self.output_topic = str(self.get_parameter("output_topic").value)
        self.output_frame_id = str(self.get_parameter("output_frame_id").value)
        self.restamp_with_now = bool(self.get_parameter("restamp_with_now").value)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=50,
            durability=DurabilityPolicy.VOLATILE,
        )

        self.publisher = self.create_publisher(LaserScan, self.output_topic, qos)
        self.subscription = self.create_subscription(LaserScan, self.input_topic, self.scan_callback, qos)

        self.get_logger().info(
            "Normalizing scan frame from "
            f"{self.input_topic} to {self.output_topic} with frame_id={self.output_frame_id} "
            f"restamp_with_now={self.restamp_with_now}"
        )

    def scan_callback(self, msg: LaserScan) -> None:
        # Optionally restamp to current sim time to avoid stale scan timestamps
        # being rejected by slam_toolbox message filters after time discontinuities.
        needs_copy = self.restamp_with_now or msg.header.frame_id != self.output_frame_id

        if not needs_copy:
            self.publisher.publish(msg)
            return

        out = LaserScan()
        out.header = msg.header
        if self.restamp_with_now:
            out.header.stamp = self.get_clock().now().to_msg()
        out.header.frame_id = self.output_frame_id
        out.angle_min = msg.angle_min
        out.angle_max = msg.angle_max
        out.angle_increment = msg.angle_increment
        out.time_increment = msg.time_increment
        out.scan_time = msg.scan_time
        out.range_min = msg.range_min
        out.range_max = msg.range_max
        out.ranges = msg.ranges
        out.intensities = msg.intensities

        self.publisher.publish(out)


def main() -> None:
    rclpy.init()
    node = ScanFrameNormalizerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
