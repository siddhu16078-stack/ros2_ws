import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
import numpy as np
import cv2


class LineDetector(Node):
    def __init__(self):
        super().__init__('line_detector')
        self.create_subscription(Image, '/camera/image_raw', self.on_image, 10)
        self.error_pub = self.create_publisher(Float32, '/line/error', 10)
        self.debug_pub = self.create_publisher(Image, '/line/debug', 10)

    def on_image(self, msg):
        # 1. Turn the ROS image message into a numpy array (height x width x 3)
        frame = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        h, w, _ = frame.shape

        # 2. Grayscale, then threshold: dark pixels (the line) become white (255)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        # 3. Only look at the lower half of the image (the part closest to the robot)
        top = h // 2
        roi = mask[top:, :]

        # 4. Find the centre of the white blob using image moments
        m = cv2.moments(roi)
        debug = frame.copy()
        cv2.rectangle(debug, (0, top), (w - 1, h - 1), (0, 255, 0), 1)

        if m['m00'] > 0:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00']) + top
            # 5. Error: -1 (line at far left) ... 0 (centred) ... +1 (far right)
            error = (cx - w / 2) / (w / 2)
            self.error_pub.publish(Float32(data=float(error)))
            cv2.circle(debug, (cx, cy), 6, (255, 0, 0), -1)
        else:
            self.get_logger().warn('Line not visible', throttle_duration_sec=1.0)

        # Publish the annotated image so we can view it in rqt_image_view
        out = Image()
        out.header = msg.header
        out.height, out.width = h, w
        out.encoding = 'rgb8'
        out.step = w * 3
        out.data = debug.tobytes()
        self.debug_pub.publish(out)


def main():
    rclpy.init()
    node = LineDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()