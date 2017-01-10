#import Cuneyt libraries
import motor_controller
import lidar
import camera_controller
import logger

#import standard libraries
from multiprocessing import Process
from Adafruit_PWM_Servo_Driver import PWM
import math
import subprocess

''' class cuneyt:
    The class where all the components of Cuneyt, the robot, are put together
    includes the most basic functionality of Cuneyt
    Conventions for ALL functions:
    - angles are given in radians
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
        self.motors = motor_controller.motor_controller(self.GPIO, self.pwm, 
                                                        (math.pi / 2), logger)

        #create camera controlller object without flipping the image
        self.camera = camera_controller.camera_controller(self.pwm, False, logger)

       # self.lidar_process = Process(target = self.lidar.sweep)
       # self.lidar_running = False
    '''
        runs the update script
    '''
    def update(self):
        subprocess.call("./update.sh")

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
