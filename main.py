#CUNEYT LIBRARY IMPORTS
import motor_controller
import lidar

#STANDARD LIBRARY IMPORTS
import RPi.GPIO as GPIO
import time
from multiprocessing import Process

motors = motor_controller(GPIO)
lidar = lidar(GPIO,time)
time.sleep(2)
lidar_process = Process(target = lidar.sweep)

