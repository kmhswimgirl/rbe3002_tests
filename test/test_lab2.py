import pytest
import rclpy
from control.tf_controller import Controller #type:ignore
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Point, Quaternion
from scipy.spatial.transform import Rotation as R

@pytest.fixture(scope="session", autouse=True)
def rclpy_init():
    '''init python client library'''
    rclpy.init()
    yield
    rclpy.shutdown()

def test_controller_init():
    ctrl = Controller(0,0,0)
    assert ctrl is not None

def test_update_odometry():
    '''test updating odometry method'''
    ctrl = Controller(0, 0, 0)
    
    odom_msg = Odometry()
    odom_msg.pose.pose.position.x = 1.5
    odom_msg.pose.pose.position.y = 2.5
    
    rotation = R.from_euler('xyz', [0, 0, 0.785])  # 45 deg in radians
    quat = rotation.as_quat()
    odom_msg.pose.pose.orientation.x = quat[0]
    odom_msg.pose.pose.orientation.y = quat[1]
    odom_msg.pose.pose.orientation.z = quat[2]
    odom_msg.pose.pose.orientation.w = quat[3]
    
    ctrl.update_odometry(odom_msg)
    
    # asserts for x and y coordinates as well as yaw 
    assert ctrl.px == 1.5
    assert ctrl.py == 2.5
    assert abs(ctrl.pth - 0.785) < 0.01  # floating pt error allowance
