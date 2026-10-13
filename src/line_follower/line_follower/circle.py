import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Circle(Node):
    def __init__(self):
        super().__init__('circle')
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel',10)
        self.create_timer(0.1,self.tick)

    def tick(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.pub.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(Circle())
    rclpy.shutdown()