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
        with open(self.miff) as m:
            miff_contents = json.load(m)

        if "slate_detection" not in miff_contents:
            miff_contents["slate_OCR":"ERROR:no slate frames detected, run slate detection first."]
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
        candidates = miff_contents["slate_detection"]
        for candidate in candidates:
            cap.set(cv2.CAP_PROP_POS_FRAMES, candidate)
            ret, f = cap.read()
            processed = process_image(f)
            res = pytesseract.image_to_string(processed)
            if len(res) > 20:
                output[candidate] = res

        miff_contents.update({"slate_OCR":output})
        return miff_contents

if __name__ == '__main__':
    inp = sys.argv[1]
    miff = sys.argv[2]
    out = sys.argv[3]
    slate = slate_OCR(inp, miff)
    with open(out, 'w+') as fout:
        fout.write(json.dumps(slate.run_service()))
