import sys

# Default name of a robot.
default_name = "Iron Giant"

# Default direction movement of the robot on real line, can be positive or negative.
default_direction = "positive"

# Default unit speed for robots to move along the real axis.
unit_speed = 1

# Velocity of a robot.
velocity = {
    "positive": unit_speed,
    "negative": -1 * unit_speed
}

# Range of the possible landing points.
land_range_inf = sys.maxsize
land_range_normal = 50

# Maximum number of steps for robots to find each others.
max_count = 1000

# Acceleration rate of the robot that found others parachutes. For the discrete case it should be exactly 2.
acceleration = 2
