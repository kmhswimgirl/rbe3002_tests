import pytest
import rclpy
from map_attributes import map_meta, numpy_map, opti_path
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

@pytest.mark.parametrize("path, reduced_path", opti_path)
def test_optimize_path(path, reduced_path):
    result = planner.optimize_path(path)
    
    print(result)
    print(reduced_path)
    assert result == reduced_path