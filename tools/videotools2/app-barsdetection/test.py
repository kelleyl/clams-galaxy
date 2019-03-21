import sys
from bars_detection import BarsDetection

sd = BarsDetection()
a = open(sys.argv[1])
b = a.read()
c = sd.annotate(b)
with open(sys.argv[2], "w") as f:
    f.write(str(c))