#import Cuneyt libraries
import motor_controller
import lidar
import camera_controller
import logger

#import standard libraries
from multiprocessing import Process
from Adafruit_PWM_Servo_Driver import PWM

''' class cuneyt:
    The class where all the components of Cuneyt, the robot, are put together
    includes the most basic functionality of Cuneyt
    Conventions for ALL functions:
    - angles are given in degrees
    - all angles and directions are relative to Cuneyt coordinates:
        - +x : forward
        - +y : right
'''
class cuneyt:

    '''function __init__():
       constructor for cuneyt, initializes basic cuneyt components:
            lidar,
            motor_controller,
            camera,
            logging
    '''
            #TODO: senseHat,
            #TODO: alexa

    def __init__(self):
        #set logger field and setup logger
        self.logger = logger.logger()
        self.logger.basicConfig(filename = "logs.txt", level = logging.DEBUG)
 
        #try to connect to the pwm shield via i2c
        try:
            self.pwm = PWM(0x40)
        except:
            self.logger.critical("Could not connect to pwm via i2c")

        #create lidar object
        self.lidar = lidar.lidar(self.pwm, logger)

        #create motor controller object
        self.motors = motor_controller.motor_controller(self.GPIO, self.pwm, logger)

        #create camera controlller object without flipping the image
        self.camera = camera_controller.camera_controller(self.pwm, False, logger)

       # self.lidar_process = Process(target = self.lidar.sweep)
       # self.lidar_running = False

    ''' function move:
        moves the robot in the given direction with the given speed
        w.r.t robot coordinates while also turning in the given 
        direction and speed 
        d_translate is an angle, d_turn is 1 or 0 1: CW, 0: CCW
        speeds are limited by 255 individually and their sum is also
        limited at 255, higher sums will be mapped accordingly to avoid
        conflicts with the motor_controller library
    '''
    def move(self, d_translate, d_turn, s_translate, s_turn):
        raise Exception("Not Yet Implemented")

    ''' function go_towards:
        moves the robot in the given direction, with the given speed
        keeping all axes stable i.e. No rotational motion
    '''
    def go_towards(self, direction, speed):
        self.move(direction, 0, speed, 0)
    ''' function start_sensor_sweep:
        starts ultrasonic sensors in sweeping motion, in parallel
    '''
    def start_sensor_sweep(self):
        raise Exception("Not Yet Implemented")

    ''' function get_sensor_sweep:
        returns the environment array from the lidar object
    '''
    def get_sensor_sweep(self):
        raise Exception("Not Yet Implemented")

    ''' function turn:
        turns the robot in the given direction (1 : CW, 0 : CCW)
        by the given angle, at the given speed
    '''
    def turn(self, direction, angle, speed):
        raise Exception("Not Yet Implemented")

    ''' function go_towards:
        moves the robot in the given direction, with the given speed
        keeping all axes stable i.e. No rotational motion
    '''
    def go_towards(self, direction, speed):
        raise Exception("Not Yet Implemented")
        #TODO: Implement the trig calculations as a function

    ''' function capture_panorama:
        captures multiple pictures, at the given bounds, and stitches
        them together in the background. Because this process requires the 
        robot to stand still, all previous motions will be terminated
        bounds are given as a tuple of two angles (a,b) such that 0<=a<=b<=180
        running capture_panorama with h_bounds = (0,0) will result in an
        exclusively vertical panorama image
    '''
    def capture_panorama(self, h_interval, v_interval, h_bounds, v_bounds):
        raise Exception("Not Yet Implemented")
