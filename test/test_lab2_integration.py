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

class TestSpeedControl: # try basic commands such as publishing to /cmd_vel
    @pytest.mark.launch(fixture=generate_test_description)
    def test_send_speed(self, rclpy_init):
        received = threading.Event()
        node = Controller(0,0,0)

        def callback(msg: TwistStamped):
            print(f"linear speed: {msg.twist.linear}")
            print(f"angular speed: {msg.twist.angular}")
            assert msg.twist.linear.x is not None or 0, "nothing published to topic"      
            assert isinstance(msg, TwistStamped), "message type is incorrect"
            received.set()

        sub = rclpy_init.create_subscription(TwistStamped, '/cmd_vel', callback, 10)
        node.send_speed(0.1, 0.4)

        for _ in range(10):
            rclpy.spin_once(rclpy_init, timeout_sec=0.1)
            if received.is_set():
                break

        assert received.is_set(), "No message received on /cmd_vel"
        rclpy_init.destroy_subscription(sub)

class TestBasicMovement: # try driving to a pose
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

        assert dist > 1.9, f"Incorrect drive distance {dist:.2f}m"
    
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

        assert 3.10 > dist > 3.01, f"did not rotate within tolerance, rotated {dist:.2f} radians"

    
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

        assert 6.10 > dist > 6.0, f"did not rotate within tolerance, rotated {dist:.2f} radians"




