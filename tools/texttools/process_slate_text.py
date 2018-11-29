import sys
import json
from PIL import Image
from Service import Service

class Process_Slate(Service):
    def __init__(self, video, miff=None):
        self.miff = miff
        super(Process_Slate, self).__init__(video, miff)

    def run_service(self):
        with open(self.miff) as f:
            miff_string = f.read()
        miff_contents = json.loads(miff_string)
        #OCR_results = miff_contents["slate_OCR"]
        HARDCODED_OCR_RESULT = "ON THE RECORD\n\n#000\n\nRecord: 1 1/ 13/ 92\nAir : 11/15/92\nRepeat: 11/16/92\n\nDirector: UNGER\nProducer: DOUGLAS"
        result_lines = HARDCODED_OCR_RESULT.split("\n")
        ocr_result_dict = {}
        for line in result_lines:
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
