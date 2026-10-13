import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.create_subscription(Pose, '/turtle1/pose',self.on_pose, 10)

    def on_pose(self,pose):
        self.get_logger().info(f'x: {pose.x} y: {pose.y}')


def main():
    rclpy.init()
    rclpy.spin(Listener())
    rclpy.shutdown()