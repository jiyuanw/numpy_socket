from my_socket import client
import cv2, sys, time
from io import BytesIO
import numpy as np

iname = 'test.jpg'
if (len(sys.argv) == 2):
    iname = sys.argv[1]
im = cv2.imread(iname, cv2.IMREAD_COLOR)
c = client().connect()
c.send(im)

# send second frame
c.send(im)
