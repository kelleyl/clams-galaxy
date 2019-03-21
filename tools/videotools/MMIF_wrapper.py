import sys
import json

from Service import Service

class MMIF_wrapper(Service):
    """Class for the Bottom Thirds ocr service."""

    def __init__(self, media_path, miff=None):
        """Constructor for Bars_Tones"""
        #super().__init__(video)
        #for python2
        super(MMIF_wrapper, self).__init__(media_path)

    def media_dict(self, media_path):
        if media_path.endswith(".mp4"): #TODO support more file types
            md["type"] = "audio-video"

        md = {}
        md["id"] = 0
        md["type"] = "image-only"
        md["location"] = video_path
        md["metadata"] = {}
        return md

    def run_service(self):
        MMIF_dict = {}
        MMIF_dict["context"] = ""
        MMIF_dict["contains"] = {}
        MMIF_dict["metadata"] = {}
        MMIF_dict["media"] = [self.media_dict(self.video)]
        MMIF_dict["views"]= []
        return MMIF_dict

if __name__ == '__main__':
    inp = sys.argv[1]
    out = sys.argv[2]
    MMIF = MMIF_wrapper(inp)
    with open(out, 'w+') as fout:
        json.dump(MMIF.run_service(), fout)
