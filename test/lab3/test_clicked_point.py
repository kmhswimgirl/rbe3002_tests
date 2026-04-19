import pytest
import rclpy
from nav_msgs.msg import MapMetaData
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
from map_attributes import map_meta, numpy_map, path_test_case, world_grid, n_4, n_8, e_dist
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


