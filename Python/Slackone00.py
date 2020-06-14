import cv2
# import argparse
import numpy as np
# import time

mapping = np.load('mapping.npy')


def transform(src_img):
    # src_img = cv2.imread('crop.jpg')
    dim = (2 * 411, 293)

    # src = np.zeros(dim, np.float32)

    src_img = cv2.resize(src_img, dim, interpolation=cv2.INTER_AREA)

    # size = src_img.shape[:2]

    mapx = mapping[0]
    mapy = mapping[1]

    # t0 = time.time()

    dst1 = cv2.remap(src_img, mapx, mapy, cv2.INTER_NEAREST)
    dst1 = dst1.astype(np.uint8)

    # t1 = time.time()
    # print(t1 - t0)
    return dst1


cap = cv2.VideoCapture("test.mp4")
if not cap.isOpened():
    print("Unable to read")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame_width, frame_height))
while True:
    ret, frame = cap.read()
    if ret:
        frame = transform(frame)
        print(frame.shape)
        # out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
