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

class TestRotate: # tests for drive and rotate functions
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
    def test_rotate_case_1(self, rclpy_init):
        '''testing normalizing the turn angle (part 1)'''

        angle = {'yaw': None} # not sure why tf using a dictionary works for this 

        def odom_callback(msg:Odometry):
            quat = msg.pose.pose.orientation
            rotation = R.from_quat([quat.x, quat.y, quat.z, quat.w])
            euler = rotation.as_euler('xyz')
            angle['yaw'] = euler[2] 
        
        odom_sub = rclpy_init.create_subscription(Odometry, '/odom', odom_callback, 10)

        timeout = 5
        start_time = time.time()
        while angle['yaw'] is None and (time.time() - start_time < timeout):
            rclpy.spin_once(rclpy_init, timeout_sec=0.1)
        assert angle['yaw'] is not None, "no odom msg before rotate()"

        start_angle = angle['yaw']

        turn_thread = threading.Thread(target=self.node.rotate, args=(math.pi + 0.1, 0.3))
        turn_thread.start()
        turn_thread.join(timeout=20)

        time.sleep(1)
        rclpy.spin_once(rclpy_init, timeout_sec=0.1)
        end_angle = angle['yaw']

        rclpy_init.destroy_subscription(odom_sub)
        dist = abs(start_angle - end_angle)
        print(f"rotated {dist:.2f} radians")

        assert math.isclose(dist, 3.03, abs_tol=0.1), f"did not rotate within tolerance, rotated {dist:.2f} radians"

    @pytest.mark.launch(fixture=generate_test_description)
    def test_rotate_case_2(self, rclpy_init):
        '''testing normalizing the turn angle (part 2)'''

        angle = {'yaw': None} # not sure why tf using a dictionary works for this 

        def odom_callback(msg:Odometry):
            quat = msg.pose.pose.orientation
            rotation = R.from_quat([quat.x, quat.y, quat.z, quat.w])
            euler = rotation.as_euler('xyz')
            angle['yaw'] = euler[2] 
        
        odom_sub = rclpy_init.create_subscription(Odometry, '/odom', odom_callback, 10)

        timeout = 5
        start_time = time.time()
        while angle['yaw'] is None and (time.time() - start_time < timeout):
            rclpy.spin_once(rclpy_init, timeout_sec=0.1)
        assert angle['yaw'] is not None, "no odom msg before rotate()"

        start_angle = angle['yaw']

        turn_thread = threading.Thread(target=self.node.rotate, args=(-math.pi - 0.1, 0.3))
        turn_thread.start()
        turn_thread.join(timeout=20)

        time.sleep(1)
        rclpy.spin_once(rclpy_init, timeout_sec=0.1)
        end_angle = angle['yaw']

        rclpy_init.destroy_subscription(odom_sub)
        dist = abs(start_angle) + abs(end_angle)
        print(f"rotated {dist:.2f} radians")

        assert math.isclose(dist, 6.05, abs_tol=0.1), f"did not rotate within tolerance, rotated {dist:.2f} radians"
