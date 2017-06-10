import math
class mecanum:  
  def __init__(self):
    self.alpha = math.pi/2
  ''' function move:
      moves the robot in the given direction with the given speed
      w.r.t robot coordinates while also turning with the given speed 
      d_translate is an angle, d_turn is 1 or 0 1: CW, 0: CCW
      speeds are limited by -+255 individually and their sum is also
      limited at -+255, higher sums will be mapped accordingly to avoid
      conflicts with the motor_controller library
  '''
  #params: speed, rotation, angle from motor_controller.py
  def move(self, speed_translate, s_rotate, dir_translate):
    '''
       trig calculations to go in set direction
    '''
    #left motors: motors that move the robot leftward when rotating forward
    left_motors = (-1) * s_translate * math.sin(dir_translate - self.alpha)
    #right motors: motors that move the robot rightward when rotating forward
    right_motors = s_translate * math.cos(dir_translate - self.alpha)
        
    #modify speeds by rotation component
    m1 = left_motors + s_rotate
    m2 = right_motors - s_rotate
    m3 = left_motors + s_rotate
    m4 = right_motors - s_rotate
        
    #limit speeds to 2.0 to avoid errors
    max_speed = 2.0
    mx = max(m1,m2,m3,m4)
    if mx > max_speed:
      m1 = m1 * max_speed / mx
      m2 = m2 * max_speed / mx
      m3 = m3 * max_speed / mx
      m4 = m4 * max_speed / mx
    return [m1,m2,m3,m4]

  def turn(self,speed):
    return self.move(0, speed, 0)

class differential:
  def __init__(self, d):
    #cast c to meters from centimeters
    self.d = d/100.0

  def move(self, V, W,non=0):
    vl = V - (W*self.d / 2)
    vr = V + (W*self.d / 2)
    return [vl,vr]
    
  def turn(self, W):
    return self.move(0, W)
