import sys
import json
from PIL import Image
from Service import Service

class Process_Slate(Service):
    def __init__(self, video, miff=None):
        self.miff = miff
        super(Process_Slate, self).__init__(video, miff)

    def run_service(self):
        with open(self.miff) as m:
            miff_contents = json.load(m)
        OCR_result = miff_contents["slate_OCR"][miff_contents["slate_OCR"].keys()[0]] # right now we're just picking the first result in the list, but we should do something more sophisticated
        OCR_lines = OCR_result.split('\n')
        ocr_result_dict = {}
        for line in OCR_lines:
            if ":" in line:
                k, v = line.split(":", 1)
                ocr_result_dict[k] = v
        miff_contents.update({"Process_Slate":ocr_result_dict})
        return miff_contents

if __name__ == '__main__':
    input_miff = sys.argv[1]
    out = sys.argv[2]
    slate = Process_Slate(None, miff=input_miff)
    with open(out, 'w+') as fout:
        json.dump(slate.run_service(), fout)
