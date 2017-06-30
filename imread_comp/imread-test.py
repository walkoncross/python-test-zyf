# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 19:58:02 2017

@author: zhaoy
"""
import cv2
import PIL
import numpy as np
import scipy.misc as spm
import skimage.io as skio
import matplotlib.pyplot as plt


'''
"Try to read a image using cv2.imread, PIL.Image.open, scipy.misc.imread, skimage.io.imread"
'''


print "Try to read a image using cv2.imread, PIL.Image.open, scipy.misc.imread, skimage.io.imread"

im_fn = 'c:/zyf/test_imgs/lena.jpg'

print im_fn

im_pil = PIL.Image.open(im_fn)
im_pil_np = np.array(im_pil)
im_cv = cv2.imread(im_fn)
im_spm = spm.imread(im_fn)
im_ski = skio.imread(im_fn)

print "===>image load by PIL.Image.open():"
print 'type: ', type(im_pil)
print 'size or shape: ', im_pil.size
print 'color mode: ', im_pil.mode
print 'plt.imshow: '
fig = plt.figure()
plt.title('PIL.Image.open')
plt.imshow(im_pil)

print "===>numpy array converted from image load by PIL.Image.open():"
print type(im_pil_np)
print 'size or shape: ', im_pil_np.shape
print 'max valuse: ', im_pil_np.max()
print 'plt.imshow: '
plt.figure()
plt.title('numpy array from PIL.Image.open')
plt.imshow(im_pil_np)

print "===>image load by PIL.Image.open():"
print type(im_cv)
print 'size or shape: ', im_cv.shape
print 'max valuse: ', im_cv.max()
print 'plt.imshow: '
plt.figure()
plt.title('cv2.imread')
plt.imshow(im_cv)

print "===>image load by PIL.Image.open():"
print type(im_spm)
print 'size or shape: ', im_spm.shape
print 'max valuse: ', im_spm.max()
print 'plt.imshow: '
plt.figure()
plt.title('scipy.misc.imread')
plt.imshow(im_spm)

print "===>image load by PIL.Image.open():"
print type(im_ski)
print 'size or shape: ', im_ski.shape
print 'max valuse: ', im_ski.max()
print 'plt.imshow: '
plt.figure()
plt.title('skimage.io.imread')
plt.imshow(im_ski)
