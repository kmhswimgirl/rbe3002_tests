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

@pytest.mark.parametrize("grid_coord, world_coord", world_grid)
def test_grid_to_world(grid_coord, world_coord):
    '''convert grid coordinates to world coordinates'''
    result = planner.grid_to_world(map_meta, grid_coord)
    assert result == world_coord

@pytest.mark.parametrize("grid_coord, world_coord", world_grid)
def test_world_to_grid(grid_coord, world_coord):
    '''the inverse of the previous function'''
    result = planner.world_to_grid(map_meta, world_coord)
    assert result == grid_coord

@pytest.mark.parametrize("p1, p2, expected_distance", e_dist)
def test_euclidean_distance(p1, p2, expected_distance):
    '''confirming euclidean_distance() works'''
    result = planner.euclidean_distance(p1, p2)
    assert abs(result - expected_distance) < 1e-5 

@pytest.mark.parametrize("test_point, n_4", n_4)
def test_neighbors_of_4(test_point, n_4):
    '''confirm neighbors_of_4 works'''
    result = planner.neighbors_of_4(test_point)
    assert result == n_4

@pytest.mark.parametrize("test_point, n_8", n_8)
def test_neighbors_of_8(test_point, n_8):
    '''confirm neighbors_of_8 works'''
    result = planner.neighbors_of_8(test_point)
    assert result == n_8

@pytest.mark.parametrize("path, expected_poses", path_test_case)
def test_build_path_message(path, expected_poses):
    '''make sure build_path_message works by checking type and poses'''
    result = planner.build_path_message(path)
    assert len(result.poses) == len(expected_poses)
    assert type(result) == Path
    
    # ignore headers b/c of timestamps, 
    # compare with approx b/c floating point errors
    for actual_pose, expected_pose in zip(result.poses, expected_poses):
        assert actual_pose.pose.position.x == pytest.approx(expected_pose.pose.position.x)
        assert actual_pose.pose.position.y == pytest.approx(expected_pose.pose.position.y)
        assert actual_pose.pose.position.z == pytest.approx(expected_pose.pose.position.z)
        assert actual_pose.pose.orientation == expected_pose.pose.orientation

