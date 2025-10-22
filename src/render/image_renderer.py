import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont


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


def convert_rgb_to_luminance(
        img: np.ndarray
) -> np.ndarray:
    img_height = img.shape[0]
    img_width = img.shape[1]

    r_coef, g_coef, b_coef = (0.2126, 0.7152, 0.0722)

    lum_img = np.zeros((img_height, img_width))

    img = img / 255.0

    for height_idx in range(img_height):
        for width_idx in range(img_width):
            lum_img[height_idx, width_idx] = \
                  r_coef * img[height_idx, width_idx, 0] \
                + g_coef * img[height_idx, width_idx, 1] \
                + b_coef * img[height_idx, width_idx, 2]

    return lum_img


def discretize_luminance(
        img: np.ndarray
) -> np.ndarray:
    disc_img = np.floor(img * 9.999)/10

    return disc_img


def convert_char_to_array(
        char_set: list,
        font_name: str,
        font_size: int = 4
) -> list:
    font_path = r"C:\Users\paulw\AppData\Local\Microsoft\Windows\Fonts"
    font = ImageFont.truetype(os.path.join(font_path, font_name + ".ttf"), font_size)

    char_array = []

    for char in char_set:
        canvas = Image.new("L", (font_size, font_size), color=0)
        draw = ImageDraw.Draw(canvas)
        draw.text((0,0), char, fill=255, font=font)

        char_array.append(np.array(canvas) / 255.0)

    return char_array


def convert_luminance_to_ascii(
        img: np.ndarray,
        texture: list,
        factor: int = 4
) -> np.ndarray:
    img_height = img.shape[0]
    img_width = img.shape[1]

    img_ascii = np.zeros((img_height * factor, img_width * factor))
    
    for height_idx in range(img_height):
        for width_idx in range(img_width):
            lumidx = int(img[height_idx, width_idx] * 10)
            char = texture[lumidx]

            hidx = height_idx * factor
            widx = width_idx * factor
            img_ascii[hidx:hidx+factor, widx:widx+factor] = char

    return img_ascii


ascii_texture = [" ", ".", ";", "c", "o", "P", "O", "?", "@", "■"]
texture_font = "BigBlueTerm437NerdFont-Regular"
font_size = 8

pil = Image.open(r"C:\Code\Projects\ascii-city\images\husky.jpg")
img = np.asarray(pil)

ds_img = downsample(img, factor=font_size)

# ds_pil = Image.fromarray(ds_img.astype(np.uint8))
# ds_pil.save(r"C:\Code\Projects\ascii-city\images\husky_01_ds.jpg")

lum_img = convert_rgb_to_luminance(ds_img)

# lum_pil = Image.fromarray((lum_img * 255).astype(np.uint8))
# lum_pil.save(r"C:\Code\Projects\ascii-city\images\husky_02_lum.jpg")

disc_img = discretize_luminance(lum_img)

# disc_pil = Image.fromarray((disc_img * 255).astype(np.uint8))
# disc_pil.save(r"C:\Code\Projects\ascii-city\images\husky_03_disc.jpg")

texture = convert_char_to_array(ascii_texture, texture_font, font_size)
ascii_img = convert_luminance_to_ascii(disc_img, texture, font_size)

ascii_pil = Image.fromarray((ascii_img * 255).astype(np.uint8))
ascii_pil.save(r"C:\Code\Projects\ascii-city\images\husky_04_ascii.jpg")
