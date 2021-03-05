#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import time
from multiprocessing.dummy import Pool
from PIL import Image
# tinypng 批量将文件夹下的webp文件转换为png格式


def convert(pic):
    pic_list = pic.split('.')
    name = pic_list[0]
    # print(name)
    webp_im = Image.open(pic)
    rgb_im = webp_im.convert('RGB')
    new_name = name + '.jpeg'
    rgb_im.save(new_name, 'jpeg')
    
    # 转换格式后删除，如果不需要删除原来的webp文件，直接注释即可
    os.remove(pic)
    return

def folder():
    begin_time = int(time.time())
    path = os.path.abspath('.')
    pics = [x for x in os.listdir('.') if os.path.isfile(x) and (os.path.splitext(x)[1] == '.webp')]
    # pics = [x for x in os.listdir('.') if os.path.isfile(x) and (os.path.splitext(x)[1] == '.png') or (os.path.splitext(x)[1] == '.jpg')]
    # print(pics)
    # exit(0)
    if not pics:
        print('no images in this folder！')
        return
    pool = Pool(3)
    # result = pool.map(tiny_png, pics)
    result = pool.map(convert, pics)
    
    end_time = int(time.time())
    spend_time = end_time - begin_time
    print('process is over and it costs ' + str(spend_time) + ' senconds')


if __name__ == '__main__':
    folder()
    path = os.path.abspath('.')
    print(path)