from __future__ import print_function

import numpy as np
import skimage.transform

from images2gif import writeGif


def transform(img, emphasize_channel, offset=0):
    mask = np.ones(img.shape)
    mask[:, :, emphasize_channel] *= 1.5
    new_img = img * mask
    new_img /= new_img.max()  # normalize

    t = skimage.transform.SimilarityTransform(translation=(offset, 0))
    new_img = skimage.transform.warp(new_img, inverse_map=t, mode='edge', order=1)

    return new_img


def throw_party(out_file, img):
    """Make a party img. Might overwrite `img`!"""
    offsets = [0, 2, 4, 2, 0, -2, -4, -2]
    images = []
    NUM_CHANNELS = 3

    if len(img.shape) == 3 and img.shape[2] > 3:
        img = img[:, :, :3]

    for i in range(16):
        offset = offsets[i % len(offsets)]
        c = i % NUM_CHANNELS
        images.append(transform(img, emphasize_channel=c, offset=offset))
    writeGif(out_file, images, loops=float('inf'))
