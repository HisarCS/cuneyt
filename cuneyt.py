#import Cuneyt libraries
import motor_controller
import lidar
import camera_controller
import logger
import resources
import motor_controller
from motor_controller import motor_controller as m_con
#import standard libraries
from multiprocessing import Process
import subprocess
import tweepy
import config

print("""
	Welcome to Cuneyt
	to init using the default configuration just run: cuneyt()
	otherwise:
	motor_setups: mecanum->0, differential->1, omni->2
	motor_drivers: i2c->0, adafruit->1
	usage: c = cuneyt(motor_setup=1, motor_driver=0)
	NOT: @canparlar @emirerdogdu, siz c = cuneyt() diceksiniz

      """)
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
            logging,
	    resources,
            tweepy
    '''
            #TODO: senseHat,
            #TODO: alexa
    camera = None
    pwm = None
    lidar = None
    motors = None
    logger = None
    resources = None

    def __init__(self, d = 20, motor_driver = motor_controller.gpio, 
                       motor_setup = motor_controller.mecanum):
        #set logger field and setup logger
        self.logger = logger.logger()
        self.resources = resources.resources()
	
        self.motors = m_con(self.logger, d, motor_setup, motor_driver)
        
	#create lidar object
        #self.lidar = lidar.lidar(self.pwm, logger)
	
	#camera is not eseential, so we can ignore erros:
        #create camera controlller object without flipping the image
        try:
            self.camera = camera_controller.camera_controller(self.pwm, False, 
        							  self.logger)
        except Exception as e:
            self.logger.warning("camera init error: "+repr(e))
	#the following are NOT essential, so we can ignore errors if any occur
        try:
            auth = tweepy.OAuthHandler(config.twitter_consumer_key, 
                                       config.twitter_consumer_secret)
            auth.set_access_token(config.twitter_access_token, 
                                  config.twitter_access_secret)
            self.twitter = tweepy.API(auth)
        except Exception as e:
            self.logger.warning("failed to initiate tweepy: "+repr(e))
       # self.lidar_process = Process(target = self.lidar.sweep)
       # self.lidar_running = False
 
    def close(self):
        self.m_con.cleanup()
    '''
        runs the update script
    '''
    def update(self):
        subprocess.call("./update.sh")

    ''' function tweet(message):
        Tweets the message on @cuneytBot
    '''
    def tweet(self, message):
        self.twitter.update_status(message)
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
