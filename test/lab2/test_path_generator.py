import pytest
import rclpy

from control.path_generator import PathGenerator
from nav_msgs.msg import Path
from unittest.mock import MagicMock

@pytest.fixture(scope="module")
def rclpy_init():
    rclpy.init()
    yield
    if rclpy.ok():
        rclpy.shutdown()

def test_path_generator_init(rclpy_init):
    node = PathGenerator(1.0, 2.0, 0.5, 'map')
    assert node.px == 1.0
    assert node.py == 2.0
    assert node.pth == 0.5
    assert node.frame == 'map'
    node.destroy_node()

def test_convert_to_nav_msg(rclpy_init):
    node = PathGenerator(0, 0, 0, 'odom')
    path = [(1, 2), (3, 4)]
    nav_msg = node.convert_to_nav_msg(path)
    assert isinstance(nav_msg, Path)
    assert nav_msg.header.frame_id == 'odom'
    assert len(nav_msg.poses) == 2
    node.destroy_node()

def test_generate_path_publishes(rclpy_init):
    node = PathGenerator(0, 0, 0, 'odom')
    node.send_path.publish = MagicMock()
    node.generate_path()
    assert node.send_path.publish.called
    node.destroy_node()

