class motor_controller:

    def __init__(self,GPIO):
        self.GPIO = GPIO
        #initialize motor pins
        #TODO: correct these
        self.m1a = 0
        self.m1b = 0
        self.m1e = 0
        self.m2a = 0
        self.m2b = 0
        self.m2e = 0
        self.m3a = 0
        self.m3b = 0
        self.m3e = 0
        self.m4a = 0
        self.m4b = 0

        for i in [m1a,m1b,m2a,m2b,m3a,m3b,m4a,m4b]:
            self.GPIO.setup(i,self.GPIO.OUT);


    def motor(self, no, direction, speed):
        GPIO = self.GPIO
        a,b = GPIO.LOW,GPIO.LOW
        if direction == 1:
            a = GPIO.HIGH
        else:
            b = GPIO.HIGH

        if no == 1:
            GPIO.output(m1a,a)
            GPIO.output(m1b,b)
        #TODO: write code for enable pin
        #TODO: map 0-255 to pwm
        elif no == 2:
            GPIO.output(m2a,a)
            GPIO.output(m2b,b)
        elif no == 3:
            GPIO.output(m3a,a)
            GPIO.output(m3b,b)
        elif no == 4:
            GPIO.output(m4a,a)
            GPIO.output(m4b,b)
        else:
            raise Exception("Motor Number Out Of Bounds")


