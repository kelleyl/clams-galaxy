import cv2
import sys
import json
import pytesseract
from Service import Service


class Slate_Detection(Service):

    def __init__(self, video, miff=None):
        """Constructor for Slate_Detection"""
        self.sample_ratio = 30
        self.max_frame_num = 1800
        self.miff = miff
        #super().__init__(video)
        #for python2
        super(Slate_Detection, self).__init__(video, miff)

    def run_service(self):
        cap = cv2.VideoCapture(self.video)
        counter = 0
        results = {}
        while cap.isOpened():
            ret, frame = cap.read()
            if counter > self.max_frame_num:
                break
            if not ret:
                break
            if counter % self.sample_ratio == 0:
                boxes = pytesseract.image_to_boxes(frame)
                number_of_boxes =  len(boxes.split('\n'))
                if number_of_boxes > 20:
                    results[counter] = number_of_boxes
            counter += 1
        with open(self.miff) as m:
            miff_string = m.read()
        miff_contents = json.loads(miff_string)
        miff_contents.update({"slate_detection":results})
        return miff_contents

if __name__ == '__main__':
    inp = sys.argv[1]
    miff = sys.argv[2]
    out = sys.argv[3]
    bt = Slate_Detection(inp, miff)
    with open(out, 'w+') as fout:
        fout.write(json.dumps(bt.run_service()))
