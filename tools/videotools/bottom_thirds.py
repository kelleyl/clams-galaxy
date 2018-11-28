import datetime
import os
import cv2
import time
import json

import numpy as np
from pytesseract import pytesseract, TesseractError
from difflib import SequenceMatcher
from Service import Service

class Bottom_Thirds(Service):
    """Class for the Bottom Thirds ocr service."""

    def __init__(self, video, miff=None):
        """Constructor for Bars_Tones"""
        self.sample_ratio = 30
        self.psm = '6'
        self.oem = None
        super().__init__(video)


    def run_service(self):
        default_whitelist = "'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()-.,'"

        def similar_image(ffc, frames, image):
            # accumulate lists of frames with similar text
            try:
                if not frames:  # If this is the first frame in the potential bottom third
                    return pytesseract.image_to_string(image), True
                else:
                    if len(pytesseract.image_to_string(image)) < 3:
                        return ffc, False
                    return ffc, SequenceMatcher(None, ffc, pytesseract.image_to_string(image)).ratio() > .5
            except TesseractError as e:
                print (e)
                return ffc, True

        def extract_text(frames, tess_psm="", tess_char_whitelist=default_whitelist, oem=""):
            config = "-c tessedit_char_whitelist=" + tess_char_whitelist + " --oem " + oem + " --psm " + tess_psm
            res = pytesseract.image_to_string(frames[0], config=config)
            return res

        cap = cv2.VideoCapture(self.video)
        counter = 0
        frames = []
        first_frame_content = ""
        is_new = False
        timestamps = []
        results = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if counter % self.sample_ratio == 0:
                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                text_image = np.array(frame)[-100:, 0:]  # this is the bottom "third"
                if text_image is None:
                    continue
                else:
                    first_frame_content, is_similar = similar_image(first_frame_content, frames, text_image)
                    if is_similar:
                        is_new = False
                        frames.append(text_image)
                        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
                    else:
                        if is_new:
                            if (len(frames) * (self.sample_ratio / 10)) > 10:
                                text = extract_text(frames, self.psm)
                                start = datetime.timedelta(milliseconds=timestamps[0])
                                end = datetime.timedelta(milliseconds=timestamps[-1])
                                times = [start.total_seconds(),end.total_seconds()]
                                results.append({"text":text, "timestamps":times})
                            frames = []
                            timestamps = []
                            is_new = False
                        else:
                            is_new = True
            counter += 1
        return {"bottom_thirds":results}