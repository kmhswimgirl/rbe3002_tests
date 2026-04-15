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
from geometry_msgs.msg import TwistStamped

from control.tf_controller import Controller

@launch_pytest.fixture(scope="class")
def generate_test_description():

    launch_file_path = PathJoinSubstitution([FindPackageShare('control'), 'launch', 'lab2_sim.launch.py'])

    lab2_sim = IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file_path),
                                        launch_arguments={'use_sim_time': 'true'}.items()
    )

    delay_tests = TimerAction(period=2.0, actions=[launch_pytest.actions.ReadyToTest()])

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

class TestDrive():
    @classmethod
    def setup_class(cls):
        rclpy.init()
        cls.node = Controller(0, 0, 0)
        cls.executor = MultiThreadedExecutor()
        cls.executor.add_node(cls.node)
        cls.exec_thread = threading.Thread(target=cls.executor.spin, daemon=True)
        cls.exec_thread.start()
        time.sleep(1) 

    @classmethod
    def teardown_class(cls):
        cls.node.destroy_node()
        cls.executor.shutdown()
        cls.exec_thread.join(timeout=2)
        # rclpy.shutdown()

    @pytest.mark.launch(fixture=generate_test_description)
    def test_drive(self, rclpy_init):
        '''confirms the robot can move in a straight line'''

        position = {'x': None, 'y': None}
        def odom_callback(msg: Odometry):
            position['x'] = msg.pose.pose.position.x
            position['y'] = msg.pose.pose.position.y

        odom_sub = rclpy_init.create_subscription(Odometry, '/odom', odom_callback, 10)

        timeout = 5
        start_time = time.time()
        while (position['x'] is None or position['y'] is None) and (time.time() - start_time < timeout):
            rclpy.spin_once(rclpy_init, timeout_sec=0.1)
        assert position['x'] is not None and position['y'] is not None, "no odom msg before drive()"

        start_pos = (position['x'], position['y'])

        drive_thread = threading.Thread(target=self.node.drive, args=(2.0, 0.2))
        drive_thread.start()
        drive_thread.join(timeout=10)

        time.sleep(1)
        rclpy.spin_once(rclpy_init, timeout_sec=0.1)
        end_pos = (position['x'], position['y'])

        rclpy_init.destroy_subscription(odom_sub)

        dist = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        print(f"Start: {start_pos}, End: {end_pos}, Distance moved: {dist:.2f}")

        assert 2.03 > dist > 1.95, f"Incorrect drive distance {dist:.2f}m"

