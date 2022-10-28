from imutils.video import VideoStream
import imutils, time, cv2

from aicode101.aicode101_img_utils import get_img_model, read_json
from utils.mobilenet_tflite_utils import MobilenetFeatures
from utils.img_classify_utils import ImgKNN

path = 'aicode101/model/dataset.json'
dataset = read_json(path)
classifier = ImgKNN(dataset)

mobilenet_model_path = 'utils/imagenet_mobilenet_v2_050_224_feature_vector_1.tflite'
mobnet = MobilenetFeatures(model_path=mobilenet_model_path)

# initialize the video stream and allow the camera sensor to
# warmup
vs = VideoStream(usePiCamera=1).start()

faceCascade = cv2.CascadeClassifier("utils/haarcascade_frontalface_default.xml")

time.sleep(2.0)

def FaceID(target):
    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_bigger = cv2.resize(frame, (500,500), interpolation = cv2.INTER_AREA)
    cv2.imshow("Live Video", frame_bigger)
    cv2.waitKey(50)
    
    faces = faceCascade.detectMultiScale(gray, 1.1, 5)

    if (len(faces) > 0):
        sample_features = mobnet.extract_features(gray) 
        predict, predict_proba = classifier.predict(sample_features)
        if predict == target:
            return True
    return False    
        
def loop():
    target = "Kyler"
    while True:
        if FaceID(target):
            print(target, 'was found.')
        else:
            print(target, 'was not found.')

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        vs.stop() # release the video stream pointer
        
    


