import pytest
import rclpy
from nav_msgs.msg import OccupancyGrid

from occupancy_grids import map1, map2, map3

from pathing.path_planner import PathPlanner

@pytest.fixture(scope="session", autouse=True)
def rclpy_init():
    '''init ROS python client library'''
    rclpy.init()
    map = map2
    yield
    rclpy.shutdown()

def test_euclidean_distance(): 
    '''confirming euclidean_distance() works'''
    pass

def test_grid_to_world():
    '''convert grid coordinates to world coordinates'''
    pass

def test_world_to_grid():
    '''the inverse of the previous function'''
    pass

def test_neighbors_of_4():
    '''confirm neighbors_of_4() works'''
    pass

def test_neighbors_of_8():
    '''confirm neighbors_of_8() works'''
    pass

def path_to_poses():
    '''convert a path message in cell coordinates to a list of PoseStamped in world coordinates'''
    pass
