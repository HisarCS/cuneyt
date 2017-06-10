import math
import pins
import sources.motor_controllers as motor_controllers
import sources.motor_drivers as motor_drivers
import RPi.GPIO as GPIO
import wiringpi

#motor setup types
mecanum = 0
differential = 1
omni = 2

#motor driver types
i2c = 0
gpio = 1

class motor_controller:
  def __init__(self, logger, d = 20, motor_setup = 0, motor_driver = 1,\
               pid = 1, reset = 1, r = 10):
    self.logger = logger
    GPIO.setmode(GPIO.BCM)
    self.GPIO = GPIO
    self.motor_controller = motor_setup
    self.motor_driver = motor_driver
    if motor_driver == gpio:
      self.driver = motor_drivers.ada_motor_driver(GPIO, logger)
    elif motor_driver == i2c:
      self.driver = motor_drivers.i2c_motor_driver(logger)
    if motor_setup == mecanum:
      self.controller = motor_controllers.mecanum(logger)
      if motor_driver == i2c:
        self.driver.init_module(pid,reset,4)
    elif motor_setup == differential:
      self.controller = motor_controllers.differential(d)
      if motor_driver == i2c:
        self.driver.init_module(pid,reset,2)

    #TODO: write motor_setup == omni
    #TODO: fix wiringpi
    #    wiringpi.wiringPiSetup()
    #    wiringpi.pinMode(1, 2)
  ''''function move: moves the robot with the given speed, rotation and angle
      note that angle is not a valid parameter for differential drive and thus
      will not affect the behavior of the robot
      @param speed: linear velocity of the robot in m/s (-2 to 2 m/s)
      @param rotation: angular velocity of the robot in rad/s
      @return: motor values array
  '''
  def move(self, speed, rotation, angle=0):
    motors = self.controller.move(speed,rotation,angle)
    for i in range(len(motors)):
      self.driver.send_motor_command(i,motors[i])
    return motors

  def turn(self, speed):
    self.driver.turn(speed)

  def get_encoders(self):
    if self.controller_type != i2c:
      self.logger.warning("this controller currently does not support"+\
			  "encoder feedback")
    return self.driver.read_encoders()

  def write_rpi_servo(self, pos):
    if pos < 0:
      self.logger.warning("cannot write negative servo value")
      return 0
    if pos > 255:
      self.logger.warning("servo value too large")
      return 0
    #TODO: fix wiringpi
    #wiringpi.pwmWrite(1,pos)    
    return 1

  def send_servo_command(self, pin, pos):
    self.driver.send_servo_command(pin, pos)
