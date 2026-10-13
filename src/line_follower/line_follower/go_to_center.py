import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class GoToCenter(Node):
    def __init__(self):
        super().__init__('go_to_center')
        self.pub = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.create_subscription(Pose,'/turtle1/pose', self.on_pose, 10)

        self.target_x = 5.5
        self.target_y = 5.5
    def on_pose(self,pose):
        dx = self.target_x - pose.x
        dy = self.target_y - pose.y
        dist = math.hypot(dx,dy)
        angle_to_target = math.atan2(dy,dx)
        angle_error = angle_to_target - pose.theta
        angle_error = math.atan2(math.sin(angle_error),math.cos(angle_error)) #so that shortest path is taken

        cmd = Twist()
        if dist>0.1:
            cmd.linear.x = 1.0
            cmd.angular.z = 10*angle_error
        self.pub.publish(cmd)
          

def main():
    rclpy.init()
    rclpy.spin(GoToCenter())
    rclpy.shutdown()
        
