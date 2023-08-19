# Messages for the Robot class logging.

found_parachute = "{first_robot} just found the parachute of {second_robot} at position {position}."

accelerated = "Speed of the {name} has been accelerated by the factor {acceleration} unit(s)."

landed = "{name} has landed successfully into the position {position}."

already_landed = "{name} has already landed into the position {position}."

moved = "{name} has moved to {position}."

cant_move = "Robot can not move until it lands on the surface."

cant_find = "Robots can not find each other until both land on the surface."

fond_each_other = "{first_robot} and {second_robot} found each other at {position}."

above_max_count = """{first_robot} and {second_robot} COULD NOT found each other. 
The reason is the maximum number of iteration provided for the while loop on movement. 
Please try to increase the max_count in configuration or decrease the range of the possible landing on real line. 
The last positions of the robots,{first_robot}: {first_robot_position} and {second_robot}: {second_robot_position}."""

journey_summary = """Summary of the Journey: 
{first_robot} has landed to {first_robot_land_position} and {second_robot} has landed to {second_robot_land_position}. 
Total distance between them was {total_distance} unit(s), but they weren't know that. 
Both started to move along the same direction with the same speed.
At the position {parachute_found_at}, {parachute_found_by} found the parachute of the other robot, and
hence its speed has been accelerated by the factor {acceleration} unit(s). 
After {total_step} number of steps, eventually they found each other at {last_position}."""
