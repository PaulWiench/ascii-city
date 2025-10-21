import numpy as np
from PIL import Image


def downsample(
        img: np.ndarray,
        factor: int = 4
) -> np.ndarray:
    img_height = img.shape[0]
    img_width = img.shape[1]
    
    ds_img_height = img_height // factor
    ds_img_width = img_width // factor

    ds_img = np.zeros((ds_img_height, ds_img_width, 3))

    for height_step in range(0, img_height, factor):
        column = img[height_step:height_step+factor, :, :]
        column = np.mean(column, axis=0)
        
        for width_step in range(0, img_width, factor):
            pixel = column[width_step:width_step+factor, :]
            pixel = np.mean(pixel, axis=0)
            
            ds_img[height_step // factor, width_step // factor] = pixel

    return ds_img


pil = Image.open(r"C:\Code\Projects\ascii-city\images\husky.jpg")
img = np.asarray(pil)

ds_img = downsample(img, factor=8)

ds_pil = Image.fromarray(ds_img.astype(np.uint8))
ds_pil.save(r"C:\Code\Projects\ascii-city\images\husky_downsampled.jpg")
