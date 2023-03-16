from .Rover import Rover
from .Mongo import find_position
import math
from time import sleep
from shapely.geometry import LineString, Point

# Reposition rover after it completes cleaning cycle
def reposition(rover:Rover, drone_collection):
    print('Turn Right')
    rover.change_yaw(angle=math.radians(90), speed=0.1)
    sleep(1)
    
    print('Move Forward')
    while rover.ul_front_edge.check_drive_ok() == False:
        rover.move_forward(speed=1)
    sleep(1)

    print('Turn Right')
    rover.change_yaw(angle=math.radians(90), speed=0.1)
    sleep(1)

    lat, lon, angle = find_position(rover=rover, drone_collection=drone_collection)
    slope = math.tan(math.radians(angle))
    line = create_line(x=lon, y=lat, slope=slope)
    
    while True:
        rover.update_rover()
        point = Point(rover.lon, rover.lat)
        if line.distance(point) < 0.000001:
            rover_yaw = rover.current_yaw()
            rotation_angle = abs(rover_yaw - angle)
            rover.change_yaw(angle=math.radians(rotation_angle), speed=0.1)
            sleep(1)
            break

        if rover.ul_front_edge.check_drive_ok() == True:
            rover.move_forward(speed=0.1)
            sleep(1)
        else:
            print('Drone not found')
            break

def create_line(x, y, slope):
    line_x = [x - 10, x + 10]
    line_y = [y + (slope * (possible_x - x)) for possible_x in line_x]
    line = LineString([(line_x[0], line_y[0]), (line_x[1], line_y[1])])
    
    return line