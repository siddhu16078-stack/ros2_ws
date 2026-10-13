import rclpy
from rclpy.node import Node

class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.get_logger().info('Hello ROS')

def main():
    rclpy.init()
    rclpy.spin(Hello())
    rclpy.shutdown()