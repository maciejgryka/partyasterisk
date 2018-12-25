import numpy as np
import skimage.transform

from imageio import mimwrite


OFFSET_MULTIPLIER = 7
OFFSET_STEP = np.pi / 3
FPS = 13


def transform(img, emphasize_channel, offset_x=0, offset_y=0):
    mask = np.ones(img.shape)
    mask[:, :, emphasize_channel] *= 1.5
    new_img = img * mask
    new_img /= new_img.max()  # normalize

    t = skimage.transform.SimilarityTransform(translation=(offset_x, offset_y))
    new_img = skimage.transform.warp(new_img, inverse_map=t, mode="edge", order=1)

    return (new_img * 255).astype("uint8")


def throw_party(img, out_file):
    """Make `img` party and save under `out_file`."""

    offsets_x = OFFSET_MULTIPLIER * np.sin(np.arange(-np.pi, np.pi, OFFSET_STEP))
    offsets_y = OFFSET_MULTIPLIER * np.cos(np.arange(-np.pi, np.pi, OFFSET_STEP))

    images = []
    NUM_CHANNELS = 3

    if len(img.shape) == 3 and img.shape[2] > 3:
        img = img[:, :, :3]

    for i, (offset_x, offset_y) in enumerate(zip(offsets_x, offsets_y)):
        c = i % NUM_CHANNELS
        images.append(
            transform(img, emphasize_channel=c, offset_x=offset_x, offset_y=offset_y)
        )
    mimwrite(out_file, images, fps=FPS)
