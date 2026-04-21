import pytest
import rclpy
from map_attributes import map_meta, numpy_map, expansion_1_sq, a_star_tests
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

@pytest.mark.parametrize("start, goal, exp_length, tolerance", a_star_tests)
def test_a_star_path(start, goal, exp_length, tolerance):
    result = planner.a_star()