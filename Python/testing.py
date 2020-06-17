import cv2
import numpy as np
import py360convert

# press q to exit the video
mapping = np.load('mapping.npy')
# load the parameters for perspective image in the variable list below
# fov_deg: Field of view given in int or tuple (h_fov_deg, v_fov_deg).
# u_deg: Horizontal viewing angle in range [-pi, pi]. (- Left / + Right).
# v_deg: Vertical viewing angle in range [-pi/2, pi/2]. (- Down/ + Up).
# out_hw: Output image (height, width) in tuple.
# in_rot_deg: Inplane rotation.
# mode: bilinear or nearest.

u_deg = 30
v_deg = 50
out_hw = (500, 500)
fov_deg = (50, 10)


def transform(src_img):
    dim = (2 * 411, 293)

    src_img = cv2.resize(src_img, dim, interpolation=cv2.INTER_AREA)

    mapx = mapping[0]
    mapy = mapping[1]

    dst1 = cv2.remap(src_img, mapx, mapy, cv2.INTER_NEAREST)
    dst1 = dst1.astype(np.uint8)
    return dst1


# location of video to be tested

cap = cv2.VideoCapture("test.mp4")
if not cap.isOpened():
    print("Unable to read")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame_width, frame_height))
while True:
    ret, frame = cap.read()
    if ret:
        # transformation to equi-rectangular
        frame = transform(frame)
        # Fill the parameter above
        # Transformation to Perspective
        frame = py360convert.e2p(frame, fov_deg, u_deg, v_deg, out_hw, in_rot_deg=0, mode='bilinear')
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
