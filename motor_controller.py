import math
import pins

class motor_controller:

    ''' function __init__
        constructor for motor_controller,
        default/recommended parameters:
        GPIO: RPi.GPIO
        pwm: PWM(0x40) where pwm is Adafruit_PWM_Servo_Driver -> PWM
    '''

    def __init__(self, GPIO, pwm, alpha, logger):
        '''
        copy pin controllers and logger
        '''
        self.pwm = pwm
        self.GPIO = GPIO
        self.logger = logger
        self.alpha = alpha
        '''
            set the wheel angle, the angle towards which the robot moves 
            when wheel turns in the positive direction
        '''
        self.wheel_angle = alpha        
        
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

        #set up raspi pins as output
        for i in [self.m1a,self.m1b,self.m2a,self.m2b,
		  self.m3a,self.m3b,self.m4a,self.m4b]:
            self.GPIO.setup(i,self.GPIO.OUT);

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
        if no == 1:
            GPIO.output(self.m1a,a)
            GPIO.output(self.m1b,b)
            self.pwm.set_pwm(self.m1e, 0, speed_pwm)

        elif no == 2:
            GPIO.output(self.m2a,a)
            GPIO.output(self.m2b,b)
            self.pwm.set_pwm(self.m2e, 0, speed_pwm)

        elif no == 3:
            GPIO.output(self.m3a,a)
            GPIO.output(self.m3b,b)
            self.pwm.set_pwm(self.m3e, 0, speed_pwm)

        elif no == 4:
            GPIO.output(self.m4a,a)
            GPIO.output(self.m4b,b)
            self.pwm.set_pwm(self.m4e, 0, speed_pwm)
    
        else:
            self.logger.error("motor index out of bounds")
            return False
        return True
    ''' function stop_all:
        stops all motors, setting both inputs to high and enable to 0
    '''
    def stop_all(self):
        for i in [self.m1e,self.m2e,self.m3e,self.m4e]:
            self.pwm.set_pwm(i, 0, 0)
        for i in [self.m1a,self.m1b,self.m2a,self.m2b,self.m3a,self.m3b,self.m4a,self.m4b]:
            self.GPIO.output(i, self.GPIO.LOW)
    ''' function move:
        moves the robot in the given direction with the given speed
        w.r.t robot coordinates while also turning with the given speed 
        d_translate is an angle, d_turn is 1 or 0 1: CW, 0: CCW
        speeds are limited by -+255 individually and their sum is also
        limited at -+255, higher sums will be mapped accordingly to avoid
        conflicts with the motor_controller library
    '''

    def move(self, dir_translate, s_translate, s_rotate):
        '''
            trig calculations to go in set direction
        '''
        #left motors: motors that move the robot leftward when rotating forward
        left_motors = (-1) * s_translate * math.sin(dir_translate - self.alpha)
        #right motors: motors that move the robot rightward when rotating forward
        right_motors = s_translate * math.cos(dir_translate - self.alpha)
        
        #modify speeds by rotation component
        m1 = left_motors + s_rotate
        m2 = right_motors + s_rotate
        m3 = left_motors + s_rotate
        m4 = right_motors + s_rotate
        print("cycle")
        
        #limit speeds to 255 to avoid errors
        mx = max(m1,m2,m3,m4)
        if mx > 255:
            m1 = m1 * 255 / mx
            m2 = m2 * 255 / mx
            m3 = m3 * 255 / mx
            m4 = m4 * 255 / mx
        print(int(m1))
        print(int(m2))
        print(int(m3))
        print(int(m4))
        #send speed to motors
        self.motor(1, int(m1))
        self.motor(2, int(m2))
        self.motor(3, int(m3))
        self.motor(4, int(m4))

    '''
        wrapper for move for only turning the robot around its axis
    '''
    def turn(self, speed):
        self.move(0,0,speed)

    '''
        wrapper for move for only translating the robot
    '''
    def translate(self, direction, speed):
        self.move(direction, speed, 0)
