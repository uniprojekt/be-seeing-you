from picamera2 import Picamera2, Preview
from PIL import Image
import time
import numpy as np
from detect import detect_objects
import sys 
import cv2
from printer import Printer

MIN_DETECTION_FRAMES = 3
MIN_WAIT_FRAMES = 15
CONF_THRESH = 0.35
DO_PRINT = False

LABEL_THRESHOLDS = {
	"finger": 0.5,
}

detection_frames = 0
wait_frames = 0
last_detection = None

picam2 = Picamera2()
camera_config = picam2.create_video_configuration(main={"format":"YUV420","size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

printer = Printer()
#printer.ticket('poop')

start_time = time.time()
frame_count = 0
#np.set_printoptions(threshold=sys.maxsize)
while True:
    #buffer = picam2.capture_arrays()
    #buffer = np.array(buffer[0][0])
    #image = buffer[:,:,:3]

    yuv420 = picam2.capture_array()
    image = cv2.cvtColor(yuv420, cv2.COLOR_YUV420p2RGB)
    #print(image.shape, pil_img)

    res = detect_objects(image, frame_count)
    #print(res)

    best_index = np.argmax(res['scores'])
    best_score = res['scores'][best_index]
    best_label = res['classes'][best_index]

    threshold = LABEL_THRESHOLDS.get(best_label, CONF_THRESH)

    if best_score > threshold:
        print(f"{frame_count}: Found {best_label} with score {best_score}")
        if last_detection == best_label and wait_frames > MIN_WAIT_FRAMES:
            detection_frames += 1
            if detection_frames >= MIN_DETECTION_FRAMES:
                print(f"Detected! printing ticket for {best_label}")
                if DO_PRINT:
                    printer.ticket(best_label)
                detection_frames = 0
                wait_frames = 0
        else:
            last_detection = best_label
            detection_frames = 0
    else:
        detection_frames = 0

    wait_frames += 1

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the result
    #print(f"{(1/elapsed_time):.1f}fps")
    start_time = time.time()
    frame_count += 1

    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.destroyAllWindows()
