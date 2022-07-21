
import os
from os import path
from IPython.display import Image, clear_output
import shutil
if path.exists("/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs"):
    # path
    path = "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs"
    directory = "runs"
    # Parent Directory
    parent = "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5"
    # Path
    path = os.path.join(parent, directory)
    # Remove the Directory if precvious runs are there
    shutil.rmtree(path)
