import os
import surl
import Image
import subprocess
import datetime
import ftplib
from subprocess import call
from uuid import uuid4
from os.path import join, basename, expanduser
import cv2  # OpenCV Library
import time
import sys
import photoboothconfig as cfg




class PhotoBooth(object):

    def __init__(self):

	# set debug level to add logs
	self.debug_level = cfg.debug_level

        # -----------------------------------------------------------------------------
	#       Setting all global variables from photoboothconfig.py file
	# -----------------------------------------------------------------------------

	# Load our overlay images (on the webcam preview for the countdown)
	print "[NOTICE] : loading Overlay Images"
	imgOverlayText3 = cv2.imread(cfg.path_imgOverlayText3, -1)
	imgOverlayText2 = cv2.imread(cfg.path_imgOverlayText2, -1)
	imgOverlayText1 = cv2.imread(cfg.path_imgOverlayText1, -1)
	imgOverlayText_push = cv2.imread(cfg.path_imgOverlayText_push, -1)
	imgOverlayText_freeze = cv2.imread(cfg.path_imgOverlayText_freeze, -1)
	if imgOverlayText3 is None or imgOverlayText2 is None or imgOverlayText1 is None or imgOverlayText_freeze is None or imgOverlayText_push is None :
		sys.exit("[FATAL] : Error with Overlay images access. Exiting ...")

	# Convert OverlayText images to BGR
	self.imgOverlayText_freeze = imgOverlayText_freeze[:, :, 0:3]
	self.imgOverlayText3 = imgOverlayText3[:, :, 0:3]
	self.imgOverlayText2 = imgOverlayText2[:, :, 0:3]
	self.imgOverlayText1 = imgOverlayText1[:, :, 0:3]
	self.imgOverlayText_push	  = imgOverlayText_push[:, :, 0:3]

	# Where to store the photos locally (cr2 for reflex cameras, jpg for the converted photo or directly from the webcam)
	self.outcr2 = cfg.path_cr2Images

	if os.path.isdir(self.outcr2):  # testing cr2 directory existing
	    print("[NOTICE] : Directory for CR2 files : " + self.outcr2 + " : OK")
	else:
	    sys.exit("[FATAL] : with CR2 repository: cannot access directory '" + self.outcr2 + "'. Exiting ...")

	self.outjpg = cfg.path_jpgImages
	if os.path.isdir(self.outjpg):  # testing jpg directory existing
	    print("[NOTICE] : Directory for jpg files : " + self.outjpg + " : OK")
	else:
	    sys.exit("[FATAL] : Error with jpg repository: cannot access directory '" + self.outjpg + "'. Exiting ...")
	if os.path.isdir(self.outjpg + "/thumbnails"):  # testing jpg Thumbnail directory existing
	    print("[NOTICE] : Directory for jpg thumbnail files : " + self.outjpg + "/thumbnails : OK")
	else:
	    print(
		"[WARNING] : Error with jpg thumbnail repository: cannot access directory '" + self.outjpg + "/thumbnail'. Trying to create it")
	    os.mkdir(self.outjpg + "/thumbnails")
	    print("[NOTICE] : Directory created")

	# filename of the pictures in JPG to be uploaded on the photobooth live gallery
	self.filenamejpg = ""
	self.filenamejpgthumb = ""
	self.filenamecr2 = ""

	# The logo to apply to all images
	self.logo_img = cfg.path_logo_image

	# Configuration of shooting (1 = shoot, 0 = simulate without camera trigger)
	self.shootMode = cfg.shootMode

	# Webcam choice for preview screen (0 = laptop builtin webcam, 1 = external webcam)
	self.previewDeviceSelect = cfg.previewDeviceSelect


	# Camera choice for shooting screen (0 = laptop builtin webcam, 1 = external webcam, 2 = Reflex Camera)
	self.ShootingDeviceSelect = cfg.ShootingDeviceSelect

	# Shooting Key
	self.shooting_key = cfg.shooting_key
	self.exit_key = cfg.exit_key
	

	# FTP configuration when real time upload on your website is activated 
	self.ftp_upload = cfg.ftp_upload
	self.ftp_url = cfg.ftp_url
	self.ftp_login = cfg.ftp_login
	self.ftp_pwd = cfg.ftp_pwd
	self.ftp_targetPath = cfg.ftp_targetPath
	self.ftp_targetPathThumbnail = cfg.ftp_targetPathThumbnail

	# Web url of the local or external website hosting the pictures gallery
	self.website_url = cfg.websiteUrl

	#Timer for displaying the last Photo (in seconds)
	self.photo_display_timer=cfg.photo_display_timer


	
	""" Detect the camera and set the various settings """
        # cfg = ['--set-config=%s=%s' % (k, v) for k, v in gphoto_config.items()]
        print '[NOTICE] : Detecting Camera...'
        subprocess.call('gphoto2 --auto-detect ', shell=True)

    def webcam_preview(self):
        # collect video input from first webcam on system
        video_capture = cv2.VideoCapture(self.previewDeviceSelect)

        startTime = time.time()
        startshootcountdown = 0
        startshoot = 0
        print '[NOTICE] : %f : starting preview streaming' % (startTime)
	if (self.debug_level > 0):
		print '[DEBUG] : %f' % (startTime)
	
        while True:
            currentTime = time.time()
            currentDelay = currentTime - startTime
            imgOverlayText = self.imgOverlayText_push

            if (startshoot == 1):
                break

            if (currentDelay > 3 and startshootcountdown == 1):
                startshootcountdown = 0
                startshoot = 1
                imgOverlayText = self.imgOverlayText_freeze
                print "[NOTICE] : Shooting button pressed"

            if (startshootcountdown == 1 and currentDelay < 3):
                imgOverlayText = self.imgOverlayText1

            if (startshootcountdown == 1 and currentDelay < 2):
                imgOverlayText = self.imgOverlayText2

            if (startshootcountdown == 1 and currentDelay < 1):
                imgOverlayText = self.imgOverlayText3

            # Capture video feed
            ret, frame = video_capture.read()
	    if frame is None :
		sys.exit("FATAL : Cannot read from device for preview, please check configuration for 'previewDeviceSelect'. Exiting ...")


            heightframe, widthframe, channelsframe = frame.shape

            OverlayText = cv2.resize(imgOverlayText, (widthframe, heightframe), interpolation=cv2.INTER_AREA)

            if (startshootcountdown == 1):
                frame = cv2.addWeighted(frame, 0.7, OverlayText, 0.3, 0)
            else:
                # I want to put logo on top-left corner, So I create a ROI
                rows, cols, channels = OverlayText.shape
                roi = frame[0:rows, 0:cols]

                # Now create a mask of logo and create its inverse mask also
                img2gray = cv2.cvtColor(OverlayText, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)

                # Now black-out the area of logo in ROI
                frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

                # Take only region of logo from logo image.
                OverlayText_fg = cv2.bitwise_and(OverlayText, OverlayText, mask=mask)

                # Put logo in ROI and modify the main image
                dst = cv2.add(frame_bg, OverlayText_fg)
                frame[0:rows, 0:cols] = dst

            # Display the resulting frame
            cv2.namedWindow('photoboothVideo', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('photoboothVideo', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
            cv2.imshow('photoboothVideo', frame)

            # press any key to exit
            # NOTE;  x86 systems may need to remove: &quot;&amp; 0xFF == ord('q')&quot;

            if cv2.waitKey(1) & 0xFF == ord(self.shooting_key):
                startTime = time.time()
                startshootcountdown = 1

            if cv2.waitKey(1) & 0xFF == ord(self.exit_key):
                sys.exit("END : Quitting program.")

            # When everything is done, release the capture
        print "[NOTICE] : stopping webcam streaming"
        video_capture.release()
        cv2.destroyAllWindows()
        return


    def set_photo_filenames(self):
        
        """ Capture a photo and download it from the camera """

        # filename = join(out, '%s.jpg' % str(uuid4()))
        self.filenamecr2 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".cr2"

        # if self.shootMode==0:
        #	self.filenamecr2 = "19900101-060606.cr2"

        self.filenamejpg = self.filenamecr2.replace(".cr2", ".jpg")
        self.filenamejpgthumb = self.filenamecr2.replace(".cr2", "-thumb.jpg")
        self.filenamecr2 = self.outcr2 + "/" + self.filenamecr2
        return


    def capture_photo_from_SLR_camera(self):
        # Umount anyprocess using the camera

        print "[NOTICE] : Umount any Camera ..."
        subprocess.call('gvfs-mount -s gphoto2',
                        shell=True)

        # take a picture with the camera
        # cfg = ['--set-config=%s=%s' % (k, v) for k, v in gphoto_config.items()]
        startTime = time.time()
        print "[NOTICE] : Capture Photo ..."
        ret = subprocess.call('gphoto2 ' +
                              '--keep --capture-image-and-download ' +
                              '--filename="%s" ' % self.filenamecr2,
                              shell=True)
        if ret != 0:
            if ret < 0:
                print "[ERROR] : Killed by signal", -ret
            else:
                print "[ERROR] : Command failed with return code", ret
                sys.exit("[FATAL] : Error with gphoto2 command : cannot capture the picture. Exiting ...")
        else:
            print "[NOTICE] : Shoot Success !"

        tempo = time.time() - startTime
        if (self.debug_level > 0):
		print "[DEBUG] : temps : %f.2" % tempo

        # convert the CR2 picture into jpg
        print "[NOTICE] : Convert RAW Picture to JPG  : %s" % self.filenamecr2
        subprocess.call('ufraw-batch ' +
                        '%s --out-type=jpg --overwrite --shrink=2 --output=%s' % (self.filenamecr2, self.outjpg + "/" + self.filenamejpg),
                        shell=True)

        tempo = time.time() - startTime
        if (self.debug_level > 0):
		print "[DEBUG] : temps : %f.2" % tempo

        return self.filenamejpg


    def process_thumbnail(self):
        # rezize the picture into jpg thumbnail
        print "[NOTICE] : Resize Picture for thumbnail..."
        pictureJpg = cv2.imread(self.outjpg + "/" + self.filenamejpg, -1)
        pictureJpg = pictureJpg[:, :, 0:3]
        pictureJpgHeight, pictureJpgWidth, pictureJpgChannel = pictureJpg.shape
        # pictureJpg = cv2.resize(pictureJpg, (pictureJpgWidth/10,pictureJpgHeight/10), interpolation = cv2.INTER_AREA)
        pictureJpg = cv2.resize(pictureJpg, (200, 130), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.outjpg + "/thumbnails/" + self.filenamejpgthumb, pictureJpg)
        return


    def process_image(self):
        print "[NOTICE] : Processing %s..." % self.filenamecr2

        image = self.apply_logo(self.outjpg + "/" + self.filenamejpg)

        self.display_last_picture()

        if self.ftp_upload == True:
            url = self.upload_photos_to_website()


    def apply_logo(self, image):
        print "[NOTICE] : Applying logo..."
        print "[NOTICE] : Image : " + self.outjpg + self.filenamejpg
 
        """ Apply a Logo to an image """
        mark = Image.open(self.logo_img)
        im = Image.open(image)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        # resizing the logo
        mark_w = int(im.size[0] * 0.10)
        mark_h = int(mark.size[1] * mark_w / mark.size[0])
        mark = mark.resize((mark_w, mark_h))

        # applying watermark
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        position = (im.size[0] - mark.size[0], im.size[1] - mark.size[1])
        layer.paste(mark, position)
        outfile = image
        Image.composite(layer, im, layer).save(outfile)
        print "[NOTICE] : Logo Applied on " + outfile
        return outfile


    def upload_photos_to_website(self):
        """ Upload this image to a remote server """
	
	print "[NOTICE] : Uploading to remote server..."
            
        # subprocess.call('scp "%s" %s' % (image, ssh_image_repo), shell=True)
        # if delete_after_upload:
        #    os.unlink(image)
        try:
            session = ftplib.FTP(self.ftp_url, self.ftp_login, self.ftp_pwd)
            session.cwd(self.ftp_targetPath)
        except:
            print("Cannot connect to the FTP server,check connection configuration and network. Skipping upload ...")
            return

        session = ftplib.FTP(self.ftp_url, self.ftp_login, self.ftp_pwd)
        session.cwd(self.ftp_targetPath)

        # transfer first jpg photo
        session.cwd(self.ftp_targetPath)
        file = open(self.outjpg + "/" + self.filenamejpg)  # file to send
        print "[NOTICE] : Uploading Picture: %s" % (self.filenamejpg)
        session.storbinary("STOR " + self.filenamejpg, file, 1024)
        file.close()

        # transfer first jpg photo
        session.cwd(self.ftp_targetPathThumbnail)
        file = open(self.outjpg + "/thumbnails/" + self.filenamejpgthumb)  # file to send
        print "[NOTICE] : Uploading Thumbnail: %s" % (self.filenamejpgthumb)
        session.storbinary("STOR " + self.filenamejpgthumb, file, 1024)
        file.close()

        # close FTP
        session.quit()
        return


    def capture_photo_from_webcam(self):
        print "[NOTICE] : Capturing image from webcam stream"
        video_capture = cv2.VideoCapture(self.ShootingDeviceSelect)
        for i in range(20):
            return_value, image = video_capture.read()
            cv2.imwrite(self.outjpg + "/" + self.filenamejpg, image)
        del (video_capture)
        return

    def display_last_picture(self):
	#Opening browser to my local website, but could be the image directly, or any other way to display the photo	
	print "[NOTICE] : opening Browser to Show last Photo"
        subprocess.call('xdg-open "%s"' % self.website_url, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'),shell=True)
   	return


if __name__ == "__main__":


    photobooth = PhotoBooth()

    photobooth.display_last_picture

    time.sleep(photobooth.photo_display_timer)

    try:
        while True:
            photobooth.webcam_preview()

            photobooth.set_photo_filenames()

            if (photobooth.ShootingDeviceSelect == 2):
                photobooth.capture_photo_from_SLR_camera()
            else:
                photobooth.capture_photo_from_webcam()

            photobooth.process_thumbnail()

            photobooth.process_image()

            time.sleep(photobooth.photo_display_timer)

            print "[NOTICE] : Timer for last picture preview is finished"

            subprocess.call('wmctrl -c firefox', shell=True)
    except KeyboardInterrupt:
        print "\n[NOTICE] : Exiting..."
print "[NOTICE] : Program Closed."
