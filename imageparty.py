from io import BytesIO
from base64 import b64encode

import imageio
import numpy as np
import skimage.transform


OFFSET_MULTIPLIER = 7
OFFSET_STEP = np.pi / 3
FPS = 13


def transform(
    img: np.array, emphasize_channel: int, offset_x: int = 0, offset_y: int = 0
) -> np.array:
    mask = np.ones(img.shape)
    mask[:, :, emphasize_channel] *= 1.5
    new_img = img * mask
    new_img /= new_img.max()  # normalize

    t = skimage.transform.SimilarityTransform(translation=(offset_x, offset_y))
    new_img = skimage.transform.warp(new_img, inverse_map=t, mode="edge", order=1)

    return (new_img * 255).astype("uint8")


def throw_party(img: np.array) -> str:
    """Make `img` party and return it a Base64 string."""
    f = BytesIO()
    f.write(throw_party_in_memory(img))
    return b64encode(f.getvalue()).decode("utf-8")


def throw_party_in_memory(img: np.array) -> bytes:
    """Make `img` party and return it as bytes."""

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
    return imageio.mimwrite(imageio.RETURN_BYTES, images, format="gif", fps=FPS)
