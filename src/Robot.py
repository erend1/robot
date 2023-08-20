# Import random integer chooser and util function.
# Notice that importing path begins with /src/ directory,
# hence the script must be called from another script that
# lies in the same directory with /src/. For instance: main.py
from random import randint
from src.utils.Utils import Logger
from src.utils.config import (default_name,
                              default_direction,
                              velocity,
                              land_range_normal,
                              max_count,
                              acceleration)
from src.utils import msg

# Define logger object.
logger = Logger(__name__).get_robot_logger()


class Robot:
    """
    Description:
        The class Robot will perform landing operation, movement, and finding other robots and the real line.
        In order to move along any direction, the robot must first lan on the surface. Then it will be possible to
        use move, find functions as well. The only optional input for generating a Robot object is just name of it.
        Any change occurring in the object will be logged so that one can always check the journey of the Robot.

    Example Usage:
        a = Robot("Metu")
        b = Robot("Math")
        a.land()
        b.land()
        a.find_robot(b)

    Inputs:
    :param str name:

    """
    def __init__(self, name: str = None):
        # Name of the robot
        self.name = name or default_name
        # Logger object to log events.
        self.logger = logger
        # Landing position of the robot.
        self.land_position = None
        # Current position of the robot.
        self.position = None
        # List of positions of the robot.
        self.position_hist = list()
        # Current velocity of the robot.
        # Sign corresponding to direction and
        # absolute value of the variable corresponding to its speed.
        self.velocity = 0
        # Is it landed or not.
        self.on_air = True

    def _get_summary(self, other_robot: "Robot", parachute_found_at: int, parachute_found_by: str, count: int):
        """
        Description:
            To save a long journey string to sum up total process of find_robot algorithm.

        :param other_robot:
        :param parachute_found_at:
        :param parachute_found_by:
        :param count:
        :return:
        """
        summary = msg.journey_summary.format(first_robot=self.name,
                                             first_robot_land_position=self.land_position,
                                             second_robot=other_robot.name,
                                             second_robot_land_position=other_robot.land_position,
                                             total_distance=abs(self.land_position - other_robot.land_position),
                                             parachute_found_at=parachute_found_at,
                                             parachute_found_by=parachute_found_by,
                                             acceleration=acceleration,
                                             total_step=count,
                                             last_position=self.position)
        return summary

    def _did_you_just_found_parachute(self, other_robot: "Robot"):
        """
        Description:
            An algorithm to check the current position of objective robot
            is same with the landing position of the other robot.

        :param other_robot:
        :return:
        """
        if self.position == other_robot.land_position:
            self.logger.info(msg.found_parachute.format(first_robot=self.name,
                                                        second_robot=other_robot.name,
                                                        position=self.position))
            self._accelerate()
            return True
        return False

    def _accelerate(self):
        """
        Description:
            Change the magnetite of the velocity of the robot.

        :return:
        """
        self.velocity = acceleration * self.velocity
        self.logger.info(msg.accelerated.format(name=self.name, acceleration=acceleration))
        return self

    def _set_position(self, new_position: int):
        """
        Description:
            Update the position of the robot.

        :param new_position:
        :return:
        """
        self.position = new_position
        self.position_hist.append(self.position)
        return self

    def land(self):
        """
        Description:
            Land on the surface. To do that so, algorithm will assign a random integer on a suitable domain.

        :return:
        """
        if self.on_air:
            self.land_position = randint(-int(land_range_normal), int(land_range_normal))
            self.on_air = False
            self._set_position(self.land_position)
            self.logger.info(msg.landed.format(name=self.name, position=self.land_position))
        else:
            self.logger.warning(msg.already_landed.format(name=self.name, position=self.land_position))
        return self

    def move(self):
        """
        Description:
            Move along the real line.

        :return:
        """
        if not self.on_air:
            new_position = self.position + self.velocity
            self._set_position(new_position)
            self.logger.info(msg.moved.format(name=self.name, position=new_position))
        else:
            self.logger.error(msg.cant_move)
        return self

    def find_robot(self, other_robot: "Robot", print_summary: bool = True):
        """
        Description:
            Main algorithm to find another robot is provided as input.
            The details of the algorithm have been provided in the document.
            In short, both robots will go in the same direction until one of them
            finds the other's landing position and gets faster to catch it up.
            The algorithm has two main while loops, one is corresponding to finding the landing position,
            and the other one is catching up. Both loops are protected by a maximum iteration number so that
            if the distance between the robots is too vast, the algorithm will raise an error to decrease
            the landing range or increase the maximum iteration number. All processes will be saved on logs.

        Inputs:
            :param Robot other_robot:
            :param bool print_summary:
            :return:
        """
        # Make sure that they both landed.
        if self.on_air or other_robot.on_air:
            self.logger.error(msg.cant_find)
            return self

        # Set up to move same direction.
        common_direction = default_direction
        self.velocity = velocity[common_direction]
        other_robot.velocity = velocity[common_direction]

        # Start first loop for parachute finding operation.
        count = 0
        parachute_found_by = None
        parachute_found_at = None
        while self.velocity == other_robot.velocity and count < max_count:
            if self._did_you_just_found_parachute(other_robot):
                parachute_found_by = self.name
                parachute_found_at = self.position
            elif other_robot._did_you_just_found_parachute(self):
                parachute_found_by = other_robot.name
                parachute_found_at = other_robot.position
            else:
                self.move()
                other_robot.move()
                count += 1

        # Start second loop for catching the robot operation.
        while self.position != other_robot.position and count < max_count:
            self.move()
            other_robot.move()
            count += 1

        # Final, found you.
        if self.position == other_robot.position:
            self.logger.info(msg.fond_each_other.format(first_robot=self.name,
                                                        second_robot=other_robot.name,
                                                        position=self.position))
            summary = self._get_summary(other_robot, parachute_found_at, parachute_found_by, count)
            self.logger.info(summary)
            if print_summary:
                print(summary)

        # It escaped, but how ...
        else:
            self.logger.error(msg.above_max_count.format(first_robot=self.name,
                                                         second_robot=other_robot.name,
                                                         first_robot_position=self.position,
                                                         second_robot_position=other_robot.position))
        return self


if __name__ == "__main__":
    pass
