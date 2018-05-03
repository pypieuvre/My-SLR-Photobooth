from os.path import join, basename, expanduser


# Debug level to add Logs
debug_level = 1
 
# Load our overlay images
path_imgOverlayText3 = 'images/3bis.png'
path_imgOverlayText2 = 'images/2bis.png'
path_imgOverlayText1 = 'images/1bis.png'
path_imgOverlayText_push = 'images/OverlayTextAppuyezbis.png'
path_imgOverlayText_freeze = 'images/OverlayTextFreezebis.png'


# Where to spit out our qrcode, watermarked image, and local html
path_cr2Images = expanduser('./images')
path_jpgImages =  expanduser('/your/local/website/path')


# The watermark to apply to all images
path_logo_image = expanduser('./images/bretons.png')


#Configuration of shooting (1 = shoot, 0 = simulate without camera trigger)
shootMode = 0

#Webcam choice for preview screen (0 = laptop builtin webcam, 1 = external webcam)
previewDeviceSelect = 0

#Camera choice for shooting screen (0 = laptop builtin webcam, 1 = external webcam, 2 = Reflex Camera)
ShootingDeviceSelect = 0

# Shooting Key
shooting_key = 'b'
exit_key = 'q'


#Timer for displaying the last Photo (in seconds)
photo_display_timer = 4


# FTP configuration when real time upload on your website is activated 
ftp_upload = True
ftp_url = "your.ftp.website"
ftp_login = "username"
ftp_pwd = "password"
ftp_targetPath= "/website/photo/path"
ftp_targetPathThumbnail = "/website/photo-thumbnail/path"

#Web url of the local or external website hosting the pictures gallery
websiteUrl = "http://127.0.0.1/your/local/website"

