class motor_controller:

    ''' function __init__
        constructor for motor_controller,
        default/recommended parameters:
        GPIO: RPi.GPIO
        pwm: PWM(0x40) where pwm is Adafruit_PWM_Servo_Driver -> PWM
    '''

    def __init__(self, GPIO, pwm, logger):
        self.pwm = pwm
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
        self.m1a = 17   
        self.m1b = 4
        self.m1e = 7

        self.m2a = 27
        self.m2b = 18
        self.m2e = 6

        self.m3a = 12
        self.m3b = 16
        self.m3e = 8
        
        self.m4a = 20
        self.m4b = 21
        self.m4e = 9

        #set up raspi pins as output
        for i in [m1a,m1b,m2a,m2b,m3a,m3b,m4a,m4b]:
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
        in the given direction (1 : forward, 0 : backward)
        with the given speed (0 thru 255)
        returns True if succeeds
    '''
    def motor(self, no, direction, speed):
        GPIO = self.GPIO
        a,b = GPIO.LOW,GPIO.LOW
        speed_pwm = speed * 16
        
        #set direction
        if direction == 1:
            a = GPIO.HIGH
        else:
            b = GPIO.HIGH

        #send signals
        if no == 1:
            GPIO.output(m1a,a)
            GPIO.output(m1b,b)
            self.pwm.setPWM(m1e, 0, speed_pwm)

        elif no == 2:
            GPIO.output(m2a,a)
            GPIO.output(m2b,b)
            self.pwm.setPWM(m2e, 0, speed_pwm)

        elif no == 3:
            GPIO.output(m3a,a)
            GPIO.output(m3b,b)
            self.pwm.setPWM(m3e, 0, speed_pwm)

        elif no == 4:
            GPIO.output(m4a,a)
            GPIO.output(m4b,b)
            self.pwm.setPWM(m4e, 0, speed_pwm)
    
        else:
            self.logger.error("motor index out of bounds")
            return False
        return True
    ''' function stop_all:
        stops all motors, setting both inputs to high and enable to 0
    '''
    def stop_all(self):
        for i in [m1e,m2e,m3e,m4e]:
            self.pwm.setPWM(i, 0, 0)
        for i in [m1a,m1b,m2a,m2b,m3a,m3b,m4a,m4b]:
            self.GPIO.output(i, GPIO.LOW)
