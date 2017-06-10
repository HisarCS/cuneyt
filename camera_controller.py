#standard library imports
from multiprocessing import Process
import picamera

#import cuneyt config info
import config
import pins

#set error types
PiCameraError = picamera.PiCameraError

class camera_controller:

    '''
        all functions for camera_controller handle exceptions internally,
        printing them. (Will create error log in the future)
        all functions return True if no exceptions occured, False if they
        could not run to completion
    '''
    def __init__(self, pwm, flip, logger):
        #initialize the raspberry pi camera module
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024, 768)
         
	#setup servo pin and initial servo angle   
        
        #add pwm controller as a field
        self.pwm = pwm
        
	#setup servo pin and initial servo angle
        self.servo_pin = pins.camera_servo
        self.pwm.set_pwm(self.servo_pin, 0, 1175)
        self.servo_process = None
        self.servo_value = 1175
	
        #add error logger as a field
        self.logger = logger

        #set recording to false
        self.recording = False
        #set previewing to false
        self.previewing = False
 
        #flip the camera vertically, if flip = True
        self.camera.vflip = flip

    ''' function look_at:
        sets servo angle to the given angle
        note that for our servo and pwn shield, the scaling -angle -> pwm-
        is theta * 3 + 160
    '''
    def look_at(self,angle):
        if(angle < 30):
            return False
	
        val = (angle-90) % 180
        servo_val = 500 + angle * 1350/180
        self.pwm.set_pwm(self.servo_pin,0,servo_val)
        self.servo_value = servo_val
        return True

    ''' function take_picture:
        wrapper for camera.capture, saves image with the given name
        returns a boolean, True if capture was successful, false if not
        handles errors internally
    '''
    def take_picture(self, name):
        try:
            self.camera.capture("./" + config.captures_folder +'/images/' + 
				name)
            return True
        except PiCameraError as err:
            self.logger.error("Camera error: " + err)
            return False

    ''' function take_picture_at:
        sets servo angle to the given angle and takes a picture
        wrapper for look_at AND take_picture
    '''
    def take_picture_at(self, angle, name):
        self.look_at(angle) and self.take_picture(name)
        

    ''' function start_video_recording:
        wrapper for camera.start_recording()
        starts saving the video with the given name
    '''
    def start_video_recording(self, name):
        if self.recording:
            self.logger.warning("tried to start an existing process: "+
                                "video recording")
            return False
        else:
            try:
                self.camera.start_recording(config.captures_folder + 
					    './videos' + name)
                self.recording = True
                return True
            except PiCameraError as err:
                self.logger.error("Camera error: " + err)
                return False

    ''' function stop_video_recording:
        wrapper for camera.stop_recording()
        stops video recording, if exists
    '''
    def stop_video_recording(self):
        if (not self.recording):
            self.logger.warning("Tried to stop a non-existent process: "+
                                "video recording")
            return False
        else:
            try: 
                self.camera.stop_recording()
                return True
            except PiCameraError as err:
                self.logger.error("Camera error: " + err)
                return False

    ''' function start_camera_preview:
        wrapper for camera.start_preview()
        starts a camera preview on the screen
    '''
    def start_camera_preview(self):
        if (self.previewing):
            logger.warning("Tried to start an existing process: "+
                           "camera preview")
            return False
        else:
            try:
                self.camera.start_preview()
                self.previewing = True
                return True
            except PiCameraError as err:
                self.logger.error("Camera error: " + err)
                return False
        
    
    ''' function stop_camera_preview:
        wrapper for camera.stop_preview()
        stops the camera preview on the screen
    '''
    def stop_camera_preview(self):
        if (not self.previewing):
            self.logger.warning("Tried to stop a non-existent process: " +
                           "camera preview")
            return False
        else:
            try:
                self.camera.stop_preview()
                self.previewing = False
                return True
            except PiCameraError as err:
                self.logger.warning("Camera error: " + err)
                return False
   
    ''' function start_camera_stream:
        starts a camera stream, as a background process
        streams the entire camera feed to the local network with the ip
        address of the raspberry pi
    '''
    def start_camera_stream(self):
        raise Exception("Not Yet Implemented")

    ''' function stop_camera_stream:
        stops the camera stream, if on
        raises an Exception if camera stream is not running
    '''
    def stop_camera_stream(self):
        raise Exception("Not Yet Implemented")

    ''' function capture_vertical_panorama
        captures multiple images at different vertical angles
        with the given interval and stitches them together, in the background
        to create a vertical panoramic image
        interval is an integer i, such that 0 < i < 180
    '''
    def capture_vertical_panorama(self, interval):
        raise Exception("Not Yet Implemented")

    ''' function capture_vertical_panorama_at:
        captures multiple images at the specified angles,
        angles is an array of integers a, where for all i in a,
        0 < i < 180 and no two members of the array are equal
    '''
    def capture_vertical_panorama_at(self, angles):
        raise Exception("Not Yet Implemented")
