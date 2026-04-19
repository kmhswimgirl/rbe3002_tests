from nav_msgs.msg import OccupancyGrid, MapMetaData
from geometry_msgs.msg import Pose, Point, Quaternion, PoseStamped
from nav_msgs.msg import Path
import numpy as np
from numpy import typing as npt
from typing import Tuple, List
from pathing.numpy_lab3 import PathPlanner as planner

# general map for testing on without using the map server
map = OccupancyGrid()
map.header.stamp.sec = 0
map.header.stamp.nanosec = 0
map.header.frame_id = "map"
map.info.map_load_time.sec = 0
map.info.map_load_time.nanosec = 0
map.info.resolution = 0.1
map.info.width = 40
map.info.height = 30
map.info.origin.position.x = 0.0
map.info.origin.position.y = 0.0
map.info.origin.position.z = 0.0
map.info.origin.orientation.x = 0.0
map.info.origin.orientation.y = 0.0
map.info.origin.orientation.z = 0.0
map.info.origin.orientation.w = 1.0

map_rows = []
map_rows.append([100]*40)

map_rows.append([100] + [0]*38 + [100])
for _ in range(3):
    map_rows.append([100] + [0]*10 + [100]*4 + [0]*24 + [100])  
map_rows.append([100,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,100])
for _ in range(4):
    map_rows.append([100] + [0]*38 + [100])
map_rows.append([100]*10 + [0]*20 + [100]*10)
for _ in range(3):
    map_rows.append([100] + [0]*38 + [100])
map_rows.append([100,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,100])
for _ in range(4):
    map_rows.append([100] + [0]*38 + [100])
map_rows.append([100]*8 + [0]*24 + [100]*8)
for _ in range(3):
    map_rows.append([100] + [0]*38 + [100])
map_rows.append([100,0,0,0,0,100,100,0,0,0,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,0,0,100,100,0,0,0,0,100])
for _ in range(5):
    map_rows.append([100] + [0]*38 + [100])
map_rows.append([100]*40)
map.data = [cell for row in map_rows for cell in row]

# replacement for self.mapinfo
map_meta = MapMetaData()
map_meta = map.info

# numpy map for those functions that need it 
def occupancy_grid_to_numpy(occupancy_grid: OccupancyGrid) -> npt.NDArray:
    width = occupancy_grid.info.width
    height = occupancy_grid.info.height
    data = np.array(occupancy_grid.data, dtype=np.int8)
    grid_2d = data.reshape((height, width))
    return grid_2d

numpy_map = occupancy_grid_to_numpy(map)

# world to grid and grid to world:
world_grid = [
    ((5, 0), Point(x=0.55, y=0.05, z=0.0)),
    ((0, 0), Point(x=0.05, y=0.05, z=0.0)),
    ((10, 10), Point(x=1.05, y=1.05, z=0.0)),
    ((100, -9), Point(x=10.05, y=-0.85, z=0.0))
]

# euclidean distance test points
e_dist = [
    ((0, 0), (0, 0), 0.0),                   
    ((0, 0), (3, 4), 5.0),                    
    ((0, 0), (1, 0), 1.0),                   
    ((0, 0), (0, 1), 1.0),                   
    ((1, 1), (4, 5), 5.0),             
    ((-1, -1), (1, 1), 2.828427),
    ((0, 0), (5, 12), 13.0),                  
    ((2, 3), (2, 8), 5.0),                    
    ((-3, -4), (0, 0), 5.0)              
]

# neighbors of four test points
n_4 = [
    ((1, 1), [(1, 2), (2, 1)]), 
    ((5, 5), [(5, 6), (5, 4), (6, 5), (4, 5)]), 
    ((20, 15), [(20, 16), (20, 14), (21, 15), (19, 15)]), 
    ((10, 10), [(10, 11), (10, 9), (11, 10)]), 
    ((38, 28), [(38, 27), (37, 28)]), 
    ((19, 14), [(19, 15), (19, 13), (20, 14), (18, 14)]), 
    ((2, 2), [(2, 3), (2, 1), (3, 2), (1, 2)])
]

# neighbors of eight test points
n_8 = [ 
    ((1, 1), [(2, 2), (1, 2), (2, 1)]), 
    ((5, 5), [(6, 6), (4, 4), (6, 4), (4, 6), (5, 6), (5, 4), (6, 5), (4, 5)]), 
    ((20, 15), [(21, 16), (19, 14), (21, 14), (19, 16), (20, 16), (20, 14), (21, 15), (19, 15)]), 
    ((10, 10), [(11, 11), (9, 9), (11, 9), (9, 11), (10, 11), (10, 9), (11, 10)]), 
    ((38, 28), [(37, 27), (38, 27), (37, 28)]), 
    ((19, 14), [(20, 15), (18, 13), (20, 13), (18, 15), (19, 15), (19, 13), (20, 14), (18, 14)]), 
    ((2, 2), [(3, 3), (1, 1), (3, 1), (1, 3), (2, 3), (2, 1), (3, 2), (1, 2)])
]

# build path message test paths
init_path = [
    (2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (6, 3), (7, 3), (8, 4), (8, 5), (8, 6), (9, 6), (10, 6), 
    (11, 6), (12, 7), (12, 8), (12, 9), (13, 10), (14, 10), (15, 11), (15, 12), (16, 13), (17, 14), 
    (18, 15), (19, 16), (20, 16), (21, 16),(22, 16), (23, 16), (24, 17), (25, 18), (26, 18), (27, 19)
]

test_expected_poses = [
    PoseStamped(
        header={'stamp': {'sec': 0, 'nanosec': 0}, 'frame_id': 'map'},
        pose=Pose(position=Point(x=x, y=y, z=0.0), orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0))
    )
    for (x, y) in [
        (0.25, 0.25), (0.35, 0.25), (0.45, 0.25), (0.55, 0.25),
        (0.55, 0.35), (0.65, 0.35), (0.75, 0.35), (0.85, 0.45),
        (0.85, 0.55), (0.85, 0.65), (0.95, 0.65), (1.05, 0.65),
        (1.15, 0.65), (1.25, 0.75), (1.25, 0.85), (1.25, 0.95),
        (1.35, 1.05), (1.45, 1.05), (1.55, 1.15), (1.55, 1.25),
        (1.65, 1.35), (1.75, 1.45), (1.85, 1.55), (1.95, 1.65),
        (2.05, 1.65), (2.15, 1.65), (2.25, 1.65), (2.35, 1.65),
        (2.45, 1.75), (2.55, 1.85), (2.65, 1.85), (2.75, 1.95)
    ]
]

path_test_case = [(init_path, test_expected_poses)]

# for optimized path (test_lab3_ec.py)
colinear_path = [
    (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
    (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8),
    (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14),
    (15, 14), (16, 14), (17, 14), (18, 14), (19, 14),
    (19, 15), (19, 16), (19, 17), (19, 18),
]

reduced_path = [(2, 2), (8, 2), (8, 8), (14, 14), (19, 14), (19, 18)]

opti_path = [(colinear_path, reduced_path)]

# for obstacle expansion (square)

# arr_1 = planner.obstacle_expansion(numpy_map, 1)
# arr_2 = planner.obstacle_expansion(numpy_map, 2)

# np.save('test/lab3/map_files/expanded_map.npy', arr_1)
# np.save('test/lab3/map_files/expanded_map_p2.npy', arr_2)

exp_map_1 = np.load('test/lab3/map_files/expanded_map.npy')
exp_map_2 = np.load('test/lab3/map_files/expanded_map_p2.npy')

expansion_1_sq = [(numpy_map, exp_map_1)]
expansion_2_sq = [(numpy_map, exp_map_2)]