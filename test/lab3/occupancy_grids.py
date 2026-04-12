from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Header
from geometry_msgs.msg import Pose, Point, Quaternion

map1 = OccupancyGrid()
map1.header.stamp.sec = 0
map1.header.stamp.nanosec = 0
map1.header.frame_id = "map"
map1.info.map_load_time.sec = 0
map1.info.map_load_time.nanosec = 0
map1.info.resolution = 0.1
map1.info.width = 10
map1.info.height = 10
map1.info.origin.position.x = 0.0
map1.info.origin.position.y = 0.0
map1.info.origin.position.z = 0.0
map1.info.origin.orientation.x = 0.0
map1.info.origin.orientation.y = 0.0
map1.info.origin.orientation.z = 0.0
map1.info.origin.orientation.w = 1.0
map1.data = [
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0,
    0, 0, 0, -1, 100, 100, -1, 0, 0, 0
]

map2 = OccupancyGrid()
map2.header.stamp.sec = 0
map2.header.stamp.nanosec = 0
map2.header.frame_id = "map"
map2.info.map_load_time.sec = 0
map2.info.map_load_time.nanosec = 0
map2.info.resolution = 0.1
map2.info.width = 30
map2.info.height = 20
map2.info.origin.position.x = 0.0
map2.info.origin.position.y = 0.0
map2.info.origin.position.z = 0.0
map2.info.origin.orientation.x = 0.0
map2.info.origin.orientation.y = 0.0
map2.info.origin.orientation.z = 0.0
map2.info.origin.orientation.w = 1.0
map2.data = [
    *([100]*30),
    *([100] + [0]*28 + [100]) * 9,
    *([100]*14 + [0] + [100]*15),
    *([100] + [0]*28 + [100]) * 9,
    *([100]*30)
]

map3 = OccupancyGrid()
map3.header.stamp.sec = 0
map3.header.stamp.nanosec = 0
map3.header.frame_id = "map"
map3.info.map_load_time.sec = 0
map3.info.map_load_time.nanosec = 0
map3.info.resolution = 0.1
map3.info.width = 30
map3.info.height = 20
map3.info.origin.position.x = 0.0
map3.info.origin.position.y = 0.0
map3.info.origin.position.z = 0.0
map3.info.origin.orientation.x = 0.0
map3.info.origin.orientation.y = 0.0
map3.info.origin.orientation.z = 0.0
map3.info.origin.orientation.w = 1.0

maze_rows = []
maze_rows.append([100]*30)
for _ in range(4):
    maze_rows.append([100] + [0]*28 + [100])
maze_rows.append([100,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,100])
for _ in range(3):
    maze_rows.append([100] + [0]*28 + [100])
maze_rows.append([100]*5 + [0]*20 + [100]*5)
for _ in range(3):
    maze_rows.append([100] + [0]*28 + [100])
maze_rows.append([100,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,100])
for _ in range(5):
    maze_rows.append([100] + [0]*28 + [100])
maze_rows.append([100]*30)
map3.data = [cell for row in maze_rows for cell in row]

map4 = OccupancyGrid()
map4.header.stamp.sec = 0
map4.header.stamp.nanosec = 0
map4.header.frame_id = "map"
map4.info.map_load_time.sec = 0
map4.info.map_load_time.nanosec = 0
map4.info.resolution = 0.1
map4.info.width = 40
map4.info.height = 40
map4.info.origin.position.x = 0.0
map4.info.origin.position.y = 0.0
map4.info.origin.position.z = 0.0
map4.info.origin.orientation.x = 0.0
map4.info.origin.orientation.y = 0.0
map4.info.origin.orientation.z = 0.0
map4.info.origin.orientation.w = 1.0

large_maze_rows = []
large_maze_rows.append([100]*40)

large_maze_rows.append([100] + [0]*38 + [100])
for _ in range(3):
    large_maze_rows.append([100] + [0]*10 + [100]*4 + [0]*22 + [100])
large_maze_rows.append([100,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,100])
for _ in range(4):
    large_maze_rows.append([100] + [0]*38 + [100])
large_maze_rows.append([100]*10 + [0]*20 + [100]*10)
for _ in range(3):
    large_maze_rows.append([100] + [0]*38 + [100])
large_maze_rows.append([100,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,100])
for _ in range(4):
    large_maze_rows.append([100] + [0]*38 + [100])
large_maze_rows.append([100]*8 + [0]*24 + [100]*8)
for _ in range(3):
    large_maze_rows.append([100] + [0]*38 + [100])
large_maze_rows.append([100,0,0,0,0,100,100,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,100,100,0,0,0,0,100])
for _ in range(5):
    large_maze_rows.append([100] + [0]*38 + [100])
# Bottom wall
large_maze_rows.append([100]*40)
map4.data = [cell for row in large_maze_rows for cell in row]

print(map4.data)