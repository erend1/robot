from src.Robot import Robot

# Please provide name of the first robot.
first_robot = "Fame"

# Please provide name of the second robot.
second_robot = "Crypt"

# Create Robot objects and make sure them they land on the surface.
A = Robot(first_robot).land()
B = Robot(second_robot).land()

# Now use the find_robot function to find the other robot.
A.find_robot(B)

# DONE! Please do not forget to check the logs inside
# the /src/ directory to see each step in the simulation.
