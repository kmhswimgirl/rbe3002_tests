import pytest
import rclpy
import numpy as np
from nav_msgs.msg import MapMetaData
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
from map_attributes import map_meta, numpy_map, expansion_1_sq, expansion_2_sq
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

@pytest.mark.parametrize("og_map, exp_map", expansion_1_sq)
def test_obstacle_expansion_1(og_map, exp_map):
    result = planner.obstacle_expansion(og_map, 1)
    assert np.array_equal(result, exp_map)
    
@pytest.mark.parametrize("og_map, exp_map", expansion_2_sq)
def test_obstacle_expansion_2(og_map, exp_map):
    result = planner.obstacle_expansion(og_map, 2)
    assert np.array_equal(result, exp_map)



