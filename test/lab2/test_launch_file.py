import rclpy
import pytest
import launch_pytest.actions
import launch_pytest
import subprocess
import time
import threading
import asyncio
import math

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from rclpy.executors import MultiThreadedExecutor

from scipy.spatial.transform import Rotation as R

from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, TwistStamped

from control.tf_controller import Controller
from control.path_generator import PathGenerator

@launch_pytest.fixture(scope="class")
def generate_test_description():

    launch_file_path = PathJoinSubstitution([FindPackageShare('control'), 'launch', 'lab2_sim.launch.py'])

    lab2_sim = IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file_path),
                                        launch_arguments={'use_sim_time': 'true'}.items()
    )

    delay_tests = TimerAction(period=3.0, actions=[launch_pytest.actions.ReadyToTest()])

    return LaunchDescription([
        lab2_sim,
        delay_tests
    ])

@pytest.fixture(scope="session", autouse=True) # ngl I have no idea what this does.
def event_loop():
    '''make event loop to stop warnings from appearing?'''
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="class")
def rclpy_init():
    '''init python client library'''
    if not rclpy.ok():
        rclpy.init()
    test_node = rclpy.create_node('test_node')
    yield test_node
    test_node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()
    subprocess.run(["killall", "ruby"]) # kill gz sim GUI + background lurking processes?

class TestNodeBringup: # check that basic things work such as correct nodes being launched
    @pytest.mark.launch(fixture=generate_test_description)
    def test_correct_nodes_active(self, rclpy_init):
        '''verify the correct nodes launched and are active'''

        expected_nodes = ['controller', 'robot_state_publisher', 'ros_gz_bridge', 'test_node']

        for _ in range(10):
            node_list = rclpy_init.get_node_names()
            print(node_list)
            if all(node in node_list for node in expected_nodes):
                break
            time.sleep(0.5)

        for node in expected_nodes:
            assert node in node_list, f"Node {node} not found"

    @pytest.mark.launch(fixture=generate_test_description)
    def test_turtlebot_topics(self, rclpy_init):
        '''verify types for turtlebot messages'''

        topics = rclpy_init.get_topic_names_and_types()
        topic_dict = dict(topics)

        assert 'geometry_msgs/msg/TwistStamped' in topic_dict.get('/cmd_vel', [])
        assert 'nav_msgs/msg/Odometry' in topic_dict.get('/odom', [])
        assert 'sensor_msgs/msg/LaserScan' in topic_dict.get('/scan',[])
        assert 'sensor_msgs/msg/Imu' in topic_dict.get('/imu',[])