import imutils
import cv2
import numpy as np
import PIL.ImageOps
import pytesseract
import sys
import json
from PIL import Image
from Service import Service

class slate_OCR(Service):
    def __init__(self, video, miff=None):
        self.video = video
        self.stop_frame = 300
        self.sample_ratio = 30
        self.miff = miff
        super(slate_OCR, self).__init__(video, miff)

    def run_service(self):
        def process_image(f):
            '''
            Process the image, right now this is just inverting the colors, which helps for some frames
            :param f: image to process
            :return: processed image
            '''
            f = invert_image(f)
            return f

        def invert_image(f):
            '''
            Invert the colors of the image
            :param f: image
            :return: inverted image
            '''
            f = Image.fromarray(np.uint8(f))
            f = PIL.ImageOps.invert(f)
            f = np.array(f)
            return f

        cap = cv2.VideoCapture(self.video)

        counter = 0
        output = {}
        while cap.isOpened():
            if counter > self.stop_frame:
                break
            ret, f = cap.read()
            f = invert_image(f)

            if not ret:
                break
            if counter % self.sample_ratio == 0:
                # resize the frame, maintaining the aspect ratio
                f = imutils.resize(f, width=900)
                processed = process_image(f)
                result = pytesseract.image_to_string(processed)
                output[counter] = result
            counter += 1

        with open(self.miff) as m:
            miff_string = m.read()
        miff_contents = json.loads(miff_string)
        miff_contents.update({"slate_OCR":output})
        return miff_contents

if __name__ == '__main__':
    inp = sys.argv[1]
    miff = sys.argv[2]
    out = sys.argv[3]
    slate = slate_OCR(inp, miff)
    with open(out, 'w+') as fout:
        fout.write(json.dumps(slate.run_service()))
