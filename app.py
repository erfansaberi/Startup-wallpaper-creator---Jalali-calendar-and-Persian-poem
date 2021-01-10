import ctypes
import datetime
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


def create_wallpaper():
    # Load font
    fontFile = 'fonts/{}'.format(config.default_font)
    font = ImageFont.truetype(fontFile, config.font_size)
    # Load Image
    wallpaper_name = get_wallpaper()
    imageFile = wallpaper_name
    image = Image.open(imageFile)
    draw = ImageDraw.Draw(image)
    # Poem
    if config.write_poem:
        poem = get_poem()
        reshaped_text = arabic_reshaper.reshape(poem)
        bidi_text = get_display(reshaped_text)
        w, h = draw.textsize(text=poem, font=font)
        draw.text((image.width-w-config.position_for_poem[0], image.height-h-config.position_for_poem[1]),
                  bidi_text, (255, 255, 255), font=font)
    # Jalali Datetime
    if config.write_jalali_datetime:
        trans = str.maketrans('1234567890', '۱۲۳۴۵۶۷۸۹۰')
        jtoday = str(jdatetime.datetime.now().date()).translate(trans)
        w, h = draw.textsize(text=jtoday, font=font)
        draw.text((image.width-w-config.position_for_jdatetime[0], image.height-h-config.position_for_jdatetime[1]),
                  jtoday, (255, 255, 255), font=font)
    # Gregorian Datetime
    if config.write_gregorian_datetime:
        gtoday = str(datetime.datetime.now().date())
        w, h = draw.textsize(text=gtoday, font=font)
        draw.text((image.width-w-config.position_for_gdatetime[1], image.height-h-config.position_for_gdatetime[1]),
                  gtoday, (255, 255, 255), font=font)
    # Quran
    if config.write_quran:
        reshaped_text = arabic_reshaper.reshape(get_quran())
        bidi_text = get_display(reshaped_text)
        w, h = draw.textsize(text=bidi_text, font=font)
        draw.text((image.width-w-config.position_for_ayat[0], image.height-h-config.position_for_ayat[1]),
                  bidi_text, (255, 255, 255), font=font)
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
                'https://picsum.photos/{}/{}'.format(config.system_resolution[0],config.system_resolution[1]), out='wallpapers')
            return image_filename
        elif config.offline_random_wallpaper:
            image_filename = random.choice(
                os.listdir(os.getcwd()+'\\wallpapers'))
            return 'wallpapers\\'+image_filename
    except:
        return 'wallpapers/alternative.jpg'


def get_quran():
    # Need a valid api or library for this
    return ''


def start():
    create_wallpaper()
    set_wallpaper('\output.jpg')


if __name__ == '__main__':
    start()
