import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class LineSteering(Node):
    def __init__(self):
        super().__init__('line_steering')

        # Tunable settings (can be changed from the terminal without editing code)
        self.declare_parameter('kp', 1.5)
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 0.2)
        self.declare_parameter('linear_speed', 0.15)
        self.declare_parameter('max_angular', 1.5)

        self.create_subscription(Float32, '/line/error', self.on_error, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_timer(0.1, self.watchdog)

        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = None
        self.last_msg_time = self.get_clock().now()
        self.last_sign = 1.0

    def on_error(self, msg):
        now = self.get_clock().now()
        error = msg.data

        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value
        speed = self.get_parameter('linear_speed').value
        max_ang = self.get_parameter('max_angular').value

        if self.prev_time is None:
            dt = 0.033
            derivative = 0.0
        else:
            dt = max((now - self.prev_time).nanoseconds * 1e-9, 1e-3)
            derivative = (error - self.prev_error) / dt

        self.integral += error * dt
        self.integral = max(-1.0, min(1.0, self.integral))   # stop it growing forever

        output = kp * error + ki * self.integral + kd * derivative

        cmd = Twist()
        # Line on the right (error > 0) means turn right, which is negative angular.z in ROS
        cmd.angular.z = max(-max_ang, min(max_ang, -output))
        # Slow down when the error is large so the robot can correct before it leaves the line
        cmd.linear.x = speed * (1.0 - 0.6 * min(abs(error), 1.0))
        self.cmd_pub.publish(cmd)

        self.prev_error = error
        self.prev_time = now
        self.last_msg_time = now
        if error != 0.0:
            self.last_sign = 1.0 if error > 0 else -1.0

    def watchdog(self):
        # If no line has been seen for 0.5 s, stop moving forward and turn toward
        # the side where the line was last seen
        age = (self.get_clock().now() - self.last_msg_time).nanoseconds * 1e-9
        if age > 0.5:
            cmd = Twist()
            cmd.angular.z = -0.5 * self.last_sign
            self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = LineSteering()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()