from picamera2 import Picamera2, Preview
from PIL import Image
import time
import numpy as np
from model import ObjectDetection

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

detector = ObjectDetection()


start_time = time.time()

while True:
    buffer = picam2.capture_arrays()
    buffer = np.array(buffer[0][0])
    image = buffer[:,:,:3]

    pil_img = Image.fromarray(image)

    print(image.shape, pil_img)

    result = detector.predict(buffer)
    print(result)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the result
    print(1/elapsed_time)
    start_time = time.time()
