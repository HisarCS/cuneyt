#general imports
import logging

#imports for ada_motor_driver
import pins
import Adafruit_PCA9685

#imports for i2c_motor_driver
import smbus
import time


#command bytes for different commands by i2c_motor_driver
#0x00 not used, since i2ctest sends 0

module_init_command = 0x01
motor_write_command = 0x02
encoder_read_command = 0x03
encoder_zero_command = 0x04
servo_write_command = 0x05
class ada_motor_driver:

  ''' function __init__
      constructor for motor_driver,
      default/recommended parameters: 
      @param GPIO: RPi.GPIO
      @param pwm: pwm address for Adafruit_PCA9685 -> PWM
      @param logger: logger object to log to
  '''
  def __init__(self, GPIO, logger = logging.getLogger()):
    self.pwm = Adafruit_PCA9685.PCA9685()
    self.GPIO = GPIO
    self.logger = logger
        
    #initialize motor pins
    '''
       m1: front left
       m2: front right
       m3: rear right
       m4: rear left
       !!!
       Note that the pins are set for GPIO.BCM use
       a and b pins are raspberry pi pins,
       e pins are Adafruit_pwm pins
       !!!
    '''
    self.m1a = pins.motor1_a
    self.m1b = pins.motor1_b
    self.m1e = pins.motor1_e

    self.m2a = pins.motor2_a
    self.m2b = pins.motor2_b
    self.m2e = pins.motor2_e

    self.m3a = pins.motor3_a
    self.m3b = pins.motor3_b
    self.m3e = pins.motor3_e
        
    self.m4a = pins.motor4_a
    self.m4b = pins.motor4_b
    self.m4e = pins.motor4_e

    self.motors = [{'a':self.m1a, 'b':self.m1b, 'e':self.m1e},
	           {'a':self.m2a, 'b':self.m2b, 'e':self.m2e},
                   {'a':self.m3a, 'b':self.m3b, 'e':self.m3e},
                   {'a':self.m4a, 'b':self.m4b, 'e':self.m4e}]

    #set up raspi pins as output
    for i in motors:
      self.GPIO.setup(m['a'], self.GPIO.OUT)
      self.GPIO.setup(m['b'], self.GPIO.OUT)

    '''
       define motor names as numbers for convenience
       example: motor_controller.front_left --> 1
    '''
    self.front_left = 1
    self.front_right = 2
    self.rear_right = 3
    self.rear_left = 4

  ''' function motor
      runs a specified motor (1 thru 4) 
      with the given speed (-255 thru 255), negative meaning backwards
      returns True if succeeds
  '''
  def motor(self, no, speed):
    GPIO = self.GPIO
    a,b = GPIO.LOW,GPIO.LOW
    speed_pwm = speed * 16
        
    #set direction
    if speed > 0:
      a = GPIO.HIGH
    else:
      b = GPIO.LOW

    #send signals
    if no > 4 or no < 1:
      self.logger.warning("motor index out of bounds")
      return 0
    self.GPIO.output(self.motors[no-1]['a'],a)
    self.GPIO.output(self.motors[no-1]['b'],b)
    self.pwm.set_pwm(self.motors[no-1]['e'], 0, speed_pwm)
    return True

  ''' function stop_all: stops all motors, setting both inputs to high 
      and enable to 0
  '''
  def stop_all(self):
    for i in motors:
      self.pwm.set_pwm(i['e'], 0, 0)
      self.GPIO.output(i['a'], self.GPIO.LOW)
      self.GPIO.output(i['b'], self.GPIO.LOW)
    
  '''function send_servo_command: given a servo number and servo position,
     sends an appropriate command to the servo over i2c to move the
     given servo to the given position
     @param servo_no: servo number to be driven 1<=servo_no<=3
     @param servo_val: desired servo position 0<=servo_val<=255
  '''
  def send_servo_command(self, servo_pin, servo_value):
    if(servo_value > 255):
      self.logger.warning("servo value too large: "+str(servo_value))
      return 0
    self.pwm.set_pwm(servo_pin, 0, servo_value)
    return 1

  '''function send_motor_command:
     sends a roughly accurate value to the motor given a motor velocity
     @param motor_no: motor number to send command to
     @param motor_vel: motor velocity (0.0 to 2.0) in m/s
  '''
  def send_motor_command(self, motor_no, motor_vel):
    if(motor_no < 1 or motor_no > 4):
      self.logger.warning("tried to write to a motor that doesn't exist")
      return 0
    if(abs(motor_vel) > 2.0):
      self.logger.warning("tried to write a velocity that's not supported")
      return 0
    motor_val = motor_vel / motor_max * 255
    self.motor(motor_no, motor_vel)	

class i2c_motor_driver:

  def __init__(self, logger, address=0x07, rPi_model=1):
    self.bus = smbus.SMBus(rPi_model)
    self.logger = logger
    self.i2c_address = address

    
  '''function write: writes a given byte to the motor controller
     function should not be called on its own since it can mess with the
     motor controller
     @param value: byte to write to the motor controller
  '''
  def write(self, value):
    self.bus.write_byte(self.i2c_address, value)

  '''function write_values: writes given bytes from an array of bytes in
     left to right order to the motor_controller, function should not be called
     directly since it can mess with the motor controller
     @param values: array of bytes to write to motor controller
  '''
  def write_values(self, values):
    self.bus.write_i2c_block_data(self.i2c_address, 0x00, values)

  '''function init_controller:
  '''  
  def init_module(self, pid=True, enc_reset=False, motors = 2):
    if motors > 4:
      self.logger.warning("can only drive up to 4 motors")
      return 0
    command_byte = module_init_command
    self.write_values([command_byte, pid, enc_reset, motors])
    return 1
  '''function send_motor_command: given a motor number and motor velocity, 
     sends an appropriate command to the motor controller over i2c
     to drive the given motor with the given speed
     @param motor_no: motor number to be driven 1<=motor_no<=4
     @param motor_vel: desired velocity of the motor in m/s
     @param return: 1 on success 0 on error
  '''
  def send_motor_command(self, motor_no, motor_vel):
    if(motor_no > 4): 
      self.logger.warning("max of 4 motors allowed, tried: "+str(motor_no))
      return 0
    elif(abs(motor_vel) > 2.0):
      self.logger.warning("max vel of 2m/s allowed, tried: "+str(motor_vel))
      return 0
    else:
      #round velocity into one unsigned byte w ~9mm/s precision)
      #can increase precision in the future if >1cm/s needed
      motor_vel_byte = abs(int(round(motor_vel*128/2.0)))
      #command byte is 0x02 for motor_write
      command_byte = motor_write_command
      self.write_values([command_byte,motor_no,motor_vel_byte,(motor_vel > 0)])
      return 1

  '''function send_servo_command: given a servo number and servo position,
     sends an appropriate command to the servo over i2c to move the
     given servo to the given position
     @param servo_no: servo number to be driven 1<=servo_no<=3
     @param servo_val: desired servo position 0<=servo_val<=255
  '''
  def send_servo_command(self, servo_no, servo_val):
    if servo_no > self.servos:
      self.logger.warning("trying to write to uninitialized servo "+\
			  str(servo_no))
      return 0
    if servo_val < 0:
      self.logger.warning("can't write negative servo value")
      return 0
    if servo_val > 255:
      self.logger.warning("controller can't write that value")
    command_byte = servo_write_command
    self.write_values([command_byte, servo_no, servo_val]);
    return 1
