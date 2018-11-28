import os
import cv2
import time
import json
import datetime
import sys
import glob
import numpy as np
from Service import Service



class Bars_Tones(Service):
    """Class for the Bars and Tones detection service.
        This service, may also be useful for matching other template like frames."""

    def __init__(self, video, miff=None):
        """Constructor for Bars_Tones"""
        self.sample_ratio = 10
        path_to_images = os.path.join("..","..","..","..","..","tool-data", "bars")
        print (os.listdir(path_to_images))
        self.image_list = [cv2.imread(os.path.join(path_to_images, path)) for path in os.listdir(path_to_images)]
        #super().__init__(video)
        #for python 2
        super(Bars_Tones, self).__init__(video)

    def calculate_similarity(self, frame):
        val = cv2.matchTemplate(self.image_list[0], frame, cv2.TM_SQDIFF_NORMED)[0][0]
        return (val<.89), val

    def run_service(self):
        cap = cv2.VideoCapture(self.video)
        counter = 0
        bars_tones = []
        res = []
        start_frame = True

        start_time = "/"  # something went wrong if this doesnt get set
        while cap.isOpened():
            ret, f = cap.read()
            if not ret:
                break
            if counter % self.sample_ratio == 0:
                is_similar, val = self.calculate_similarity(f)
                res.append((cap.get(cv2.CAP_PROP_POS_FRAMES), val))
                if is_similar: ## if it is bars and tones
                    if start_frame:
                        start_time = cap.get(cv2.CAP_PROP_POS_MSEC)
                        start_frame = False
                else: ## if its not bars and tones
                    if not start_frame: ## if the start time has been set to false so we're in bars and tones
                        end_time = cap.get(cv2.CAP_PROP_POS_MSEC)
                        if end_time == "0:0.0":
                            continue
                        start = datetime.timedelta(milliseconds=start_time)
                        end = datetime.timedelta(milliseconds=end_time)
                        bars_tones.append((start.total_seconds(), end.total_seconds()))
                        start_frame = True
            counter += 1
        return {"bars_tones":bars_tones, "res":res}
        #return {"bars_tones":bars_tones}

if __name__ == '__main__':
    inp = sys.argv[1]
    out = sys.argv[2]
    bt = Bars_Tones(inp)
    with open(out, 'w+') as fout:
        fout.write(str(bt.run_service()))
