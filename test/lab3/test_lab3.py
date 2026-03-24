import pytest
import rclpy
from nav_msgs.msg import OccupancyGrid

from pathing.path_planner import PathPlanner #type:ignore

@pytest.fixture(scope="session", autouse=True)
def rclpy_init():
    '''init ROS python client library'''
    rclpy.init()
    # map = OccupancyGrid()
    yield
    rclpy.shutdown()

def test_grid_to_index(): 
    '''multiple tests for converting grid coordinates to array index'''
    
    pass

def test_euclidean_distance(): 
    '''confirming euclidean_distance() works'''
    pass

def test_grid_to_world():
    '''convert grid coordinates to world coordinates'''
    pass

def test_world_to_grid():
    '''the inverse of the previous function'''
    pass

def test_is_cell_walkable():
    '''is the gridcell in the map walkable?'''
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
