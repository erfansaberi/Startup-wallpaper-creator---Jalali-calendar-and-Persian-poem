import ctypes
import os
import urllib.request
import json
import sys
import time
import wget

import arabic_reshaper
import jdatetime
import requests
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont


def set_wallpaper(wallpaper_name='\output.jpg'):
    cwd = os.getcwd()
    print(cwd+wallpaper_name)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, cwd+wallpaper_name , 0)


def write_on_image(wallpaper_name='wallpapers/wallpaper.jpg',text='روز خوبی داشته باشید',font='fonts/Sahel.ttf'):
    fontFile = font
    imageFile = wallpaper_name
    font = ImageFont.truetype(fontFile, 50)
    image = Image.open(imageFile)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    trans = str.maketrans('1234567890','۱۲۳۴۵۶۷۸۹۰')
    today = str(jdatetime.datetime.now().date()).translate(trans)
    draw = ImageDraw.Draw(image)
    w,h = draw.textsize(text=text,font=font)
    draw.text((image.width-w,image.height-120-h), bidi_text, (255,255,255), font=font)
    w,h = draw.textsize(text=today,font=font)
    draw.text((image.width-w-100,image.height-100-h), today, (255,255,255), font=font)
    draw = ImageDraw.Draw(image)
    image.save("output.jpg")


def get_text():
    #try:
    if 1:
        r = requests.get('http://c.ganjoor.net/beyt-json.php')
        res = r.json()
        text = res['m1'] + '\n    ' + res['m2'] + '\n' + res['poet']
        return text
    try:
        pass
    except Exception as e:
        return '''
        عیب رندان مکن ای زاهد پاکزه سرت
        که گناه دگران بر تو نخواهند نوشت
        نه من از پرده تقوا به در افتادم و بس
        پدرم نیز بهشت ابد از دست بهشت
        '''


def get_wallpaper():
    try:
        image_filename = wget.download('https://picsum.photos/1920/1080',out='wallpapers')
        return image_filename
    except:
        return 'wallpapers/alternative.jpg'


def start():
    text = get_text()
    today = jdatetime.datetime.now().date
    wallpaper = get_wallpaper()
    write_on_image(text=text,wallpaper_name=wallpaper)
    set_wallpaper('\output.jpg')


if __name__ == '__main__':
    start()
