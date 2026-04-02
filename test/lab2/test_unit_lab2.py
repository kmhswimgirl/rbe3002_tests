import pytest
import rclpy

from control.tf_controller import Controller
from nav_msgs.msg import Odometry
from scipy.spatial.transform import Rotation as R

@pytest.fixture(scope="module")
def rclpy_init():
    rclpy.init()
    yield
    if rclpy.ok():
        rclpy.shutdown()

def test_controller_init(rclpy_init):
    node = Controller(0,0,0)
    assert node.px == 0
    assert node.py == 0
    assert node.pth == 0
    node.destroy_node()

def test_update_odometry(rclpy_init):
    node = Controller(0, 0, 0)
    odom_msg = Odometry()
    odom_msg.pose.pose.position.x = 1.5
    odom_msg.pose.pose.position.y = 2.5
    rotation = R.from_euler('xyz', [0, 0, 0.785])
    quat = rotation.as_quat()
    odom_msg.pose.pose.orientation.x = quat[0]
    odom_msg.pose.pose.orientation.y = quat[1]
    odom_msg.pose.pose.orientation.z = quat[2]
    odom_msg.pose.pose.orientation.w = quat[3]

    node.update_odometry(odom_msg)
    print(odom_msg)

    assert node.px == 1.5
    assert node.py == 2.5
    assert abs(node.pth - 0.785) < 0.01

    node.destroy_node()
