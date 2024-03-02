# OpenCV + MediaPipe Virtual Paint App


https://github.com/Techie-Ernie/virtualpaint/assets/80609056/53ca7607-f8ba-4625-a202-0e0d78002891


## FUNCTIONS
1. Holding up index finger only allows you to draw
2. Holding up index and middle finger allows you to navigate
3. Holding up all 5 fingers acts as an eraser

## HOW TO USE
1. Clone this repo
  'git clone https://github.com/Techie-Ernie/virtualpaint.git`
2. Install required dependencies
    'pip install -r requirements.txt`
4. Set up the virtual camera: 
To send frames to the virtual camera, I used pyvirtualcam: https://pypi.org/project/pyvirtualcam/
Follow the instructions for pyvirtualcam to set up the virtual camera for your OS. (e.g. On Windows, install OBS Studio)
5. Run virtualpaint.py
    'python virtualpaint.py`
6. Note that some applications (e.g. Google Meet) have mirroring on by default and cannot be changed. To undo automatic flipping of the camera (to make it easier for the user to write), edit the line that says flip=True to flip=False in virtualpaint.py

### Credits
https://www.youtube.com/watch?v=ZiwZaAVbXQo&t=3530s
