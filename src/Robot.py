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
    def __init__(self, name: str = None):
        self.name = name or default_name
        self.logger = logger
        self.land_position = None
        self.position = None
        self.position_hist = list()
        self.velocity = 0
        self.on_air = True

    def _get_summary(self, other_robot: "Robot", parachute_found_at: int, parachute_found_by: str, count: int):
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
        if self.position == other_robot.land_position:
            self.logger.info(msg.found_parachute.format(first_robot=self.name,
                                                        second_robot=other_robot.name,
                                                        position=self.position))
            self._accelerate()
            return True
        return False

    def _accelerate(self):
        self.velocity = acceleration * self.velocity
        self.logger.info(msg.accelerated.format(name=self.name, acceleration=acceleration))
        return self

    def _set_position(self, new_position: int):
        self.position = new_position
        self.position_hist.append(self.position)
        return self

    def land(self):
        if self.on_air:
            self.land_position = randint(-int(land_range_normal), int(land_range_normal))
            self.on_air = False
            self._set_position(self.land_position)
            self.logger.info(msg.landed.format(name=self.name, position=self.land_position))
        else:
            self.logger.warning(msg.already_landed.format(name=self.name, position=self.land_position))
        return self

    def move(self):
        if not self.on_air:
            new_position = self.position + self.velocity
            self._set_position(new_position)
            self.logger.info(msg.moved.format(name=self.name, position=new_position))
        else:
            self.logger.error(msg.cant_move)
        return self

    def find_robot(self, other_robot: "Robot", print_summary: bool = True):
        if self.on_air or other_robot.on_air:
            self.logger.error(msg.cant_find)
            return self

        common_direction = default_direction
        self.velocity = velocity[common_direction]
        other_robot.velocity = velocity[common_direction]
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

        while self.position != other_robot.position and count < max_count:
            self.move()
            other_robot.move()
            count += 1

        if self.position == other_robot.position:
            self.logger.info(msg.fond_each_other.format(first_robot=self.name,
                                                        second_robot=other_robot.name,
                                                        position=self.position))
            summary = self._get_summary(other_robot, parachute_found_at, parachute_found_by, count)
            self.logger.info(summary)
            if print_summary:
                print(summary)
        else:
            self.logger.error(msg.above_max_count.format(first_robot=self.name,
                                                         second_robot=other_robot.name,
                                                         first_robot_position=self.position,
                                                         second_robot_position=other_robot.position))
        return self


if __name__ == "__main__":
    pass
