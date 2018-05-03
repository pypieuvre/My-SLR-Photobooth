# My SLR Photobooth


This is a small program running a simple photobooth. It can be used as a standalone setup, or with a real time update of an internet website to share the photos to people partying

### Set up :

![Photobooth Set Up](https://github.com/pypieuvre/My-SLR-Photobooth/blob/master/images/photobooth.png)


This is my personal set up, used to run this program :

- A **Laptop** running the program (can be any desktop, raspberry pi, etc ....)

- A **screen** used by the laptop to show preview, countdown, and photo

- A **SLR Camera** (Old Canon 500D without preview screen)

- An **external webcam** for the preview, (you can use the embedded laptop camera)

- A **remote control** to trigger photoshoot


### Features :

- Preview the photobooth scene with the laptop or an external webcam

- Shooting triggered from keyboard or remote control

- Countdown to let people get ready

- Taking picture from the SLR Camera (or a webcam)

- [OPTIONAL] Applying watermark Logo on the picture

- Displaying photo on the preview screen

- [OPTIONAL] Upload photo to a website


## Getting Started

These instructions will get you an instance of the project up and running on your local machine for execution.

### Prerequisites

What things you need to install the software and run the program

#### Hardware :

- A webcam for preview

- A SLR Camera (or webcam) to take photos

- A device (laptop/desktop) running python to execute the program (Linux Ubuntu for me)

- *[optional] a remote control to trigger picture*

- *[optional] a screen to display preview and Photo*

 

#### Software :

- Python + libraries (pip install)

               - Os, surl, ftplib, etc ...
               - OpenCV
- gphoto2

## Configuration

 

The configuration is done by updating the file photoboothconfig.py (root of the project)

## Running the program

A simple script launch is executing the program

```
python photobooth.py

```

## Product Improvement
Several additional features can be implemented to make this photobooth better. Here are a few ideas of stories to be implemented :
- With compatible SLR, use preview from camera instead of webcam
- use Text overlay instead of images for countdown
- send photo to emails
- Use a real logging library

## Contributing

This program is far from perfect, so please feel free to contact me or create pull requests to fix issues or propose new features

## Authors

* **Pierre-Yves AIMON** - *Initial work*

## License

This project is licensed under the GPL-3.0 - see the [LICENSE.md](LICENSE) file for details

