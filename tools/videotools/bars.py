import os
import cv2
import datetime
import sys
import json
from Service import Service


class Bars_Tones(Service):
    """Class for the Bars and Tones detection service.
        This service, may also be useful for matching other template like frames."""

    def __init__(self, video, miff):
        """Constructor for Bars_Tones"""
        self.sample_ratio = 10
        self.miff = miff
        path_to_images = os.path.join("..","..","..","..","..","tool-data", "bars")
        self.image_list = [cv2.imread(os.path.join(path_to_images, path)) for path in os.listdir(path_to_images)]
        #super().__init__(video)
        #for python 2
        super(Bars_Tones, self).__init__(video)

    def calculate_similarity(self, frame):
        val = cv2.matchTemplate(self.image_list[0], frame, cv2.TM_SQDIFF_NORMED)[0][0]
        return (val<.89), val

    def run_service(self):
        return self.miff
        # miff_dict = json.loads(self.miff)
        # cap = cv2.VideoCapture(self.video)
        # counter = 0
        # bars_tones = []
        # res = []
        # start_frame = True
        #
        # start_time = "/"  # something went wrong if this doesnt get set
        # while cap.isOpened():
        #     ret, f = cap.read()
        #     if not ret:
        #         break
        #     if counter % self.sample_ratio == 0:
        #         is_similar, val = self.calculate_similarity(f)
        #         res.append((cap.get(cv2.CAP_PROP_POS_FRAMES), val))
        #         if is_similar: ## if it is bars and tones
        #             if start_frame:
        #                 start_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        #                 start_frame = False
        #         else: ## if its not bars and tones
        #             if not start_frame: ## if the start time has been set to false so we're in bars and tones
        #                 end_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        #                 if end_time == "0:0.0":
        #                     continue
        #                 start = datetime.timedelta(milliseconds=start_time)
        #                 end = datetime.timedelta(milliseconds=end_time)
        #                 bars_tones.append((start.total_seconds(), end.total_seconds()))
        #                 start_frame = True
        #     counter += 1
        # return miff_dict.update({"bars_tones":bars_tones})

if __name__ == '__main__':
    video = sys.argv[1]
    miff = sys.argv[2]
    output = sys.argv[3]
    service = Bars_Tones(video, miff)
    with open(output, 'w+') as fout:
        fout.write(str(service.run_service()))
