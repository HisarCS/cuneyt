import smbus
import time

#command bytes for different commands
#0x00 not used, since i2ctest sends 0

module_init_command = 0x01
motor_write_command = 0x02
encoder_read_command = 0x03
encoder_zero_command = 0x04
servo_write_command = 0x05

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
    for value in values:
      self.write(value)

  '''function init_controller:
  '''  
  def init_controller(self, pid=True, enc_reset=False, motors = 2, servos = 2):
    if(servos+motors > max_pwm):
      self.logger.warning("tried initializing more pwm controls "+\
                          "than available: " + str(servos+motors))
      return 0
    else:
      command_byte = module_init_command
      write_values([command_byte, pid, enc_reset, servos])

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
      motor_vel_byte = int(round(abs(motor_vel)*255.0/2.0))
      #command byte is 0x02 for motor_write
      command_byte = motor_write_command
      self.write_values([command_byte, motor_no, motor_vel_byte])
      return 1

