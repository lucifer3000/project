import numpy as np
import cv2


def lerp(y0, y1, x0, x1, x):
    m = (y1 - y0) / (x1 - x0)
    b = y0
    return m * (x - x0) + b


def mapofx(size, aperture):
    print(size)
    h_src, w_src = size
    w_dst, h_dst = (1000, 1000)

    dst_imgx = np.zeros((h_dst, w_dst), dtype=np.float32)
    dst_imgy = np.zeros((h_dst, w_dst), dtype=np.float32)

    for y in range(h_dst):
        y_dst_norm = lerp(-1, 1, 0, h_dst, y)

        for x in range(w_dst):
            x_dst_norm = lerp(-1, 1, 0, w_dst, x)

            longitude = x_dst_norm * np.pi
            latitude = y_dst_norm * np.pi / 2
            p_x = np.cos(latitude) * np.cos(longitude)
            p_y = np.cos(latitude) * np.sin(longitude)
            p_z = np.sin(latitude)

            p_xz = np.sqrt(p_x ** 2 + p_z ** 2)
            r = 2 * np.arctan2(p_xz, p_y) / aperture
            theta = np.arctan2(p_z, p_x)
            x_src_norm = r * np.cos(theta)
            y_src_norm = r * np.sin(theta)

            x_src = lerp(0, w_src, -1, 1, x_src_norm)
            y_src = lerp(0, h_src, -1, 1, y_src_norm)

            # supppres out of the bound index error (warning this will overwrite multiply pixels!)
            x_src_ = np.minimum(w_src - 1, np.floor(x_src).astype(np.float32))
            y_src_ = np.minimum(h_src - 1, np.floor(y_src).astype(np.float32))

            dst_imgx[y, x] = x_src
            dst_imgy[y, x] = y_src

    pos = [dst_imgx, dst_imgy]

    return pos


size = (2 * 411, 293)
mapping = mapofx(size, np.pi)

np.save('mapping.npy', mapping)
# np.savetxt('mapping.txt', mapping)
