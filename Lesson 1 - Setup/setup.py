import os
import sys
import time
os.system("cd /usr/bin && sudo rm python && sudo ln -s python3 python")
success = 0
'''
https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
'''
commands = ["sudo apt-get update", 
            "sudo apt-get install -y python3-dev python3-pyqt5 ",
            "pip3 install opencv-python","sudo pip3 install rpi_ws281x",
            "sudo apt-get install libhdf5-dev","pip3 install imutils",
            "sudo apt-get install libhdf5-serial-dev","pip3 install sklearn", 
            "sudo apt-get install libatlas-base-dev","pip3 install tflite-runtime",
            "sudo apt-get install libjasper-dev", "sudo modprobe bcm2835-v4l2",
            "sudo pip3 install picamera", "pip3 install --upgrade numpy"]
failed = []
for cmd in commands:
    for i in range(4):
        if os.system(cmd) == 0:
            success +=1
            print(cmd, "executed successfully.")
            break
        if (i == 3):
            failed.append(cmd)
        
if success == len(commands):
    print("The installation is successful.")
    print("Please run:\npip3 install --upgrade numpy\nIn the terminal seperatly.")
else:
    print ("Some libraries have not been installed yet. Please run the setup again")
    print("These command(s) failed.")
    for cmd in failed:
        print(cmd)

