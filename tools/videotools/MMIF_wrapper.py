import sys
import json

from Service import Service

class MMIF_wrapper(Service):
    """Class for the Bottom Thirds ocr service."""

    def __init__(self, video, miff=None):
        """Constructor for Bars_Tones"""
        #super().__init__(video)
        #for python2
        super(MMIF_wrapper, self).__init__(video)

    def run_service(self):
        MMIF_dict = {}
        MMIF_dict["filename"] = self.video
        return MMIF_dict

if __name__ == '__main__':
    inp = sys.argv[1]
    out = sys.argv[2]
    MMIF = MMIF_wrapper(inp)
    with open(out, 'w+') as fout:
        json.dump(MMIF.run_service(), fout)
