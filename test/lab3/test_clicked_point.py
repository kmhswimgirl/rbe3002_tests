import pytest
import rclpy
from nav_msgs.msg import MapMetaData
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
from map_attributes import map_meta, numpy_map
from pathing.numpy_lab3 import PathPlanner

@pytest.fixture(scope="session", autouse=True)
def rclpy_init():
    '''init ROS python client library'''
    if not rclpy.ok():
        rclpy.init()
    global planner
    planner = PathPlanner()
    planner.map = numpy_map
    planner.mapinfo = map_meta
    yield
    if rclpy.ok():
        rclpy.shutdown()


def test_clicked_point_callback():
    
    pass