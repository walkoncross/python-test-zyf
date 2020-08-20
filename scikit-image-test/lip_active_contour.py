import os
import glob

import numpy as np
import cv2
import matplotlib.pyplot as plt

from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.io import imread, imsave

def show_lmks(im, landmarks, color=(0, 0, 255), show_txt=False, scale=10):
    for i in range(landmarks.shape[0]):
        x, y = landmarks[i, 0], landmarks[i, 1]
        if show_txt:
            cv2.putText(im, str(i), (int(x), int(y)),
                        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                        fontScale=0.5, color=color)
        cv2.circle(im, (int(x), int(y)), scale, color, -1)
    return im


def show_img(img, wait=1):
    cv2.namedWindow('debugg', cv2.WINDOW_NORMAL)
    cv2.imshow('debugg', img)
    cv2.waitKey(wait)


def skimage2opencv(src):
    src *= 255
    src = src.astype(np.uint8)
    src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    return src


def opencv2skimage(src):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    src = src.astype(np.float32)
    src /= 255
    return src


def get_bounding_rect(points):
    max_vals = np.max(points, axis=0)
    min_vals = np.min(points, axis=0)

    print('max_vals: {}'.format(max_vals))
    print('min_vals: {}'.format(min_vals))

    y_max = int(max_vals[0]+0.5)
    y_min = int(min_vals[0]-0.5)
    x_max = int(max_vals[1]+0.5)
    x_min = int(min_vals[1]-0.5)

    return (x_min, y_min, x_max, y_max)


def extend_rect(x_min, y_min, x_max, y_max, ratio=0.25):
    ht = y_max - y_min
    wd = x_max - x_min

    ext_y = ht*ratio
    ext_x = wd*ratio

    y_min -= ext_y
    y_max += ext_y
    x_min -= ext_x
    x_max += ext_x

    y_max = int(y_max+0.5)
    y_min = int(y_min-0.5)
    x_max = int(x_max+0.5)
    x_min = int(x_min-0.5)

    return (x_min, y_min, x_max, y_max)


img_path = 'material/00218.jpg'
mouth_img_path = 'material/00218_mouth.jpg'
lmks_path = 'material/00218_lmks.txt'
mouth_lmks_path = 'material/00218_lmks_mouth.txt'
# scale = 4.0

img = cv2.imread(img_path)
print('img.shape: {}'.format(img.shape))

lmks = np.loadtxt(lmks_path).reshape(-1, 2)
lmks = lmks[:, ::-1]  # (x,y) to (r,c)

# img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)))
# lmks = lmks / scale

# #####crop face area
# (x_min, y_min, x_max, y_max) = get_bounding_rect(lmks)
# (x_min, y_min, x_max, y_max) = get_bounding_rect(lmks)
# (x_min, y_min, x_max, y_max) = extend_rect(x_min, y_min, x_max, y_max, ratio=0.25)


# img = img[y_min:y_max, x_min:x_max, :]

# outer_mouth_lmks -= np.array([y_min, x_min])
############

#outer_mouth_index = [58, 118, 119, 59, 120, 121, 60, 122, 123, 61, 124, 125, 62, 126, 127, 63, 128, 129, 64, 130, 131, 65, 132, 133, 58]
outer_mouth_index = [58, 118, 119, 59, 120, 121, 60, 122, 123, 61,
                     124, 125, 62, 126, 127, 63, 128, 129, 64, 130, 131, 65, 132, 133]
outer_mouth_lmks = lmks[outer_mouth_index, :]
print('outer mouth landmarks: {}'.format(outer_mouth_lmks))

#inner_mouth_index = [116, 134, 135, 66, 136, 137, 67, 138, 139, 68, 140, 141, 117, 142, 143, 69, 144, 145, 70, 146, 147, 71, 148, 149, 116]
inner_mouth_index = [116, 134, 135, 66, 136, 137, 67, 138, 139, 68,
                     140, 141, 117, 142, 143, 69, 144, 145, 70, 146, 147, 71, 148, 149]
inner_mouth_upper_index = [116, 134, 135, 66, 136, 137, 67, 138, 139, 68,
                           140, 141, 117]
inner_mouth_lower_index = [142, 143, 69, 144, 145, 70, 146, 147, 71, 148, 149]

inner_mouth_lmks = lmks[inner_mouth_index, :]
# inner_mouth_lmks = lmks[inner_mouth_upper_index, :]
print('inner mouth landmarks: {}'.format(inner_mouth_lmks))

# crop face area
(x_min, y_min, x_max, y_max) = get_bounding_rect(outer_mouth_lmks)
print("bounding box: {}".format((x_min, y_min, x_max, y_max)))
(x_min, y_min, x_max, y_max) = extend_rect(
    x_min, y_min, x_max, y_max, ratio=0.25)
print("extended bounding box: {}".format((x_min, y_min, x_max, y_max)))

img = img[y_min:y_max, x_min:x_max, ::-1]
imsave(mouth_img_path, img)
############

outer_mouth_lmks -= np.array([y_min, x_min])
print('outer mouth landmarks (after crop): {}'.format(outer_mouth_lmks))

inner_mouth_lmks -= np.array([y_min, x_min])
print('inner mouth landmarks (after crop): {}'.format(inner_mouth_lmks))

# lmks_cropped = lmks - np.array([y_min, x_min])
# print('landmarks (after crop): {}'.format(lmks_cropped))
# lmks_cropped = lmks_cropped[:,:-1] # (r,c) to (x,y)
# np.savetxt(mouth_lmks_path, lmks_cropped.flatten(), fmt='%.2f')
mouth_lmks = np.vstack([outer_mouth_lmks, inner_mouth_lmks])
mouth_lmks = mouth_lmks[:,::-1] # (r,c) to (x,y)
np.savetxt(mouth_lmks_path, mouth_lmks.flatten(), fmt='%.2f')

img_skimage = opencv2skimage(img)
img_skimage_gray = rgb2gray(img_skimage)
print('img_skimage_gray.shape: {}'.format(img_skimage_gray.shape))

init_contour = inner_mouth_lmks
# init_contour = outer_mouth_lmks
print('init contour landmarks: {}'.format(init_contour))

#snake = active_contour(gaussian(img_skimage_gray, 3), init_contour, alpha=0.015, beta=10, gamma=0.001, coordinates='rc')
# snake = active_contour(gaussian(img_skimage_gray, 3), init_contour, coordinates='rc')
snake = active_contour(img_skimage_gray, init_contour,
                        alpha=0.015, beta=10, gamma=0.001,
                        w_line=-1, w_edge=1,
                        max_px_move=5,
                        boundary_condition='free', coordinates='rc')

snake2 = active_contour(img_skimage_gray, init_contour,
                        alpha=0.015, beta=1, gamma=0.001,
                        w_line=2, w_edge=1,
                        max_px_move=5,
                        boundary_condition='fixed', coordinates='rc')
print('active contour landmarks: {}'.format(snake))
print('active contour landmarks 2: {}'.format(snake2))

# img = show_lmks(img, init_contour, scale=1, color=(0, 0, 255))
# img = show_lmks(img, snake, scale=1, color=(0, 255, 0))

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(img_skimage_gray, cmap=plt.cm.gray)
# ax.plot(init_contour[:, 1], init_contour[:, 0], '--r', lw=1)
ax.plot(init_contour[:, 1], init_contour[:, 0], 'or', ms=5)
ax.plot(snake[:, 1], snake[:, 0], 'ob', ms=5)
ax.plot(snake2[:, 1], snake2[:, 0], 'og', ms=5)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img_skimage_gray.shape[1], img_skimage_gray.shape[0], 0])

plt.show()

# show_img(img, 0)
# cv2.destroyAllWindows()
