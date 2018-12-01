import os
import cv2
import datetime
import sys
import json
from Service import Service


class SlateDetection(Service):

    def __init__(self, video, miff):
        """Constructor for Bars_Tones"""
        self.sample_ratio = 30
        self.miff = miff
        path_to_images = os.path.join("..","..","..","..","..","tool-data", "slates")
        self.image_list = [cv2.imread(os.path.join(path_to_images, path)) for path in os.listdir(path_to_images)]
        hist = cv2.calcHist([self.image_list[0]], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        self.hist = cv2.normalize(hist, hist).flatten()

        #super().__init__(video)
        #for python 2
        super(SlateDetection, self).__init__(video, miff)


    def run_service(self):
        result = []
        with open(self.miff) as m:
            miff_contents = json.load(m)
        cap = cv2.VideoCapture(self.video)
        counter = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if counter % self.sample_ratio == 0:
                try:
                    frame_hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8],
                                          [0, 256, 0, 256, 0, 256])
                    frame_hist = cv2.normalize(frame_hist, frame_hist).flatten()
                    if (cv2.compareHist(self.hist, frame_hist, 0) >.98):
                        result.append(counter)
                except Exception:
                    counter += 1
                    continue
            counter += 1
        miff_contents["slate_detection"] = result
        return miff_contents

    # def calculate_similarity(self, frame):
    #     val = cv2.matchTemplate(self.image_list[1], frame, cv2.TM_SQDIFF_NORMED)[0][0]
    #     return (val<.89), val
    #
    # def run_service(self):
    #     with open(self.miff) as m:
    #         miff_dict = json.load(m)
    #     cap = cv2.VideoCapture(self.video)
    #     counter = 0
    #     slates = []
    #     res = []
    #     start_frame = True
    #
    #     start_time = "/"  # something went wrong if this doesnt get set
    #
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, float(start_search)) #jump forward to start_search
    #     while cap.isOpened():
    #         ret, f = cap.read()
    #         if not ret:
    #             break
    #         if counter % self.sample_ratio == 0:
    #             is_similar, val = self.calculate_similarity(f)
    #             res.append((cap.get(cv2.CAP_PROP_POS_FRAMES), val))
    #             if is_similar: ## if it is bars and tones
    #                 if start_frame:
    #                     start_time = cap.get(cv2.CAP_PROP_POS_MSEC)
    #                     start_frame = False
    #             else: ## if its not slate
    #                 if not start_frame: ## if the start time has been set to false so we're in slate
    #                     end_time = cap.get(cv2.CAP_PROP_POS_MSEC)
    #                     if end_time == "0:0.0":
    #                         continue
    #                     start = datetime.timedelta(milliseconds=start_time)
    #                     end = datetime.timedelta(milliseconds=end_time)
    #                     slates.append((start.total_seconds(), end.total_seconds()))
    #                     if full_video == "0":
    #                         break
    #                     start_frame = True
    #         counter += 1
    #
    #     miff_dict.update({"slate_detection":slates})
    #     return miff_dict

if __name__ == '__main__':
    video = sys.argv[1]
    miff = sys.argv[2]
    output = sys.argv[3]
    advanced = sys.argv[4]
    if advanced == "0":
        print "not advanced"
        full_video = "1" # process the whole video
        start_search = "0"
    else:
        print "advanced"
        full_video = sys.argv[5]
        start_search = sys.argv[6]

    service = SlateDetection(video, miff)
    with open(output, 'w+') as fout:
        json.dump(service.run_service(), fout)
