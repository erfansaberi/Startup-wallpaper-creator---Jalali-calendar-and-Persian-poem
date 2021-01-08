import ctypes
import json
import os
import platform
import random
import sys
import time
import urllib.request

import arabic_reshaper
import jdatetime
import requests
import wget
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

import config


def set_wallpaper(wallpaper_name='\output.jpg'):
    cwd = os.getcwd()
    if platform.system() == 'Windows':
        ctypes.windll.user32.SystemParametersInfoW(
            20, 0, cwd+wallpaper_name, 0)
    elif platform.system() == 'Linux':
        # I did not tested this line.
        os.system(
            f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {cwd+wallpaper_name}")
    else:
        input('Your operating system is not supported')


def write_on_image(wallpaper_name='wallpapers/wallpaper.jpg', poem=config.alternative_poem, font='Sahel.ttf'):
    # Load font
    fontFile = f'fonts/{font}'
    font = ImageFont.truetype(fontFile, config.font_size)
    # Load Image
    imageFile = wallpaper_name
    image = Image.open(imageFile)
    draw = ImageDraw.Draw(image)
    # Poem
    if config.write_poem:
        reshaped_text = arabic_reshaper.reshape(poem)
        bidi_text = get_display(reshaped_text)
        w, h = draw.textsize(text=poem, font=font)
        draw.text((image.width-w, image.height-120-h),
                  bidi_text, (255, 255, 255), font=font)
    # Jalali Datetime
    if config.write_jalali_datetime:
        trans = str.maketrans('1234567890', '۱۲۳۴۵۶۷۸۹۰')
        today = str(jdatetime.datetime.now().date()).translate(trans)
        w, h = draw.textsize(text=today, font=font)
        draw.text((image.width-w-100, image.height-100-h),
                  today, (255, 255, 255), font=font)
    draw = ImageDraw.Draw(image)
    image.save("output.jpg")


def get_poem():
    if config.online_random_poem:
        try:
            r = requests.get('http://c.ganjoor.net/beyt-json.php')
            res = r.json()
            text = res['m1'] + '\n    ' + res['m2'] + '\n' + res['poet']
            return text
        except:
            return config.alternative_poem
    elif config.offline_random_poem:
        return ''
    else:
        return config.alternative_poem


def get_wallpaper():
    try:
        if config.online_random_wallpaper:
            image_filename = wget.download(
                'https://picsum.photos/1920/1080', out='wallpapers')
            return image_filename
        elif config.offline_random_wallpaper:
            image_filename = random.choice(
                os.listdir(os.getcwd()+'\\wallpapers'))
            return 'wallpapers\\'+image_filename
    except:
        return 'wallpapers/alternative.jpg'


def start():
    poem = get_poem()
    wallpaper = get_wallpaper()
    write_on_image(poem=poem, wallpaper_name=wallpaper)
    set_wallpaper('\output.jpg')


if __name__ == '__main__':
    start()
