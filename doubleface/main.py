#!/usr/bin/env python

import PIL.Image
import PIL.PSDraw
import sys
import os


# retrieve circuit borders

def scanx(pix, y, w, step):
    if (step == 1):
        not_found = w - 1
        r = range(0, w)
    else:
        not_found = 0
        r = range(w - 1, -1, -1)
    for x in r:
        if pix[x, y] == 0: return x
    return not_found

def scany(pix, x, h, step):
    if (step == 1):
        not_found = h - 1
        r = range(0, h)
    else:
        not_found = 0
        r = range(h - 1, -1, -1)
    for y in r:
        if pix[x, y] == 0: return y
    return not_found

def crop_borders(im):
    w = im.size[0]
    h = im.size[1]

    pix = im.load()

    # find height
    miny = h
    maxy = 0
    for x in range(0, w):
        miny = min(scany(pix, x, h, +1), miny)
        maxy = max(scany(pix, x, h, -1), maxy)

    # find width
    minx = w
    maxx = 0
    for y in range(0, h):
        minx = min(scanx(pix, y, w, +1), minx)
        maxx = max(scanx(pix, y, w, -1), maxx)

    croped_im = im.crop((minx, miny, maxx, maxy))
    croped_im.info['dpi'] = im.info['dpi']
    return croped_im


# print image format

def print_im_format(im):
    wsizes = (210, 148, 105, 0)
    hsizes = (297, 210, 148, 0)

    w = (im.size[0] * 25.4) / 800.0
    h = (im.size[1] * 25.4) / 800.0

    for i in range(0, len(wsizes)):
        if w >= wsizes[i]:
            break

    for j in range(0, len(hsizes)):
        if h >= hsizes[j]:
            break

    if j < i: i = j

    print('dim: ' + str(w) + ' x ' + str(h))
    print('fmt: a' + str(4 + i))

    return


# save to ps

def save_ps(im, path):
    im.save('/tmp/__eda.png', dpi=im.info['dpi'])
    os.system('convert /tmp/__eda.png ' + path)
    return


# main

top_name = 'top.png'
bot_name = 'bot.png'
top_bot_name = 'top_bot.png'
if (len(sys.argv) > 1): top_name = sys.argv[1]
if (len(sys.argv) > 2): bot_name = sys.argv[2]
if (len(sys.argv) > 3): top_bot_name = sys.argv[3]

top_im = crop_borders(PIL.Image.open(top_name))
bot_im = crop_borders(PIL.Image.open(bot_name))

top_dpi = top_im.info['dpi'][0]
top_size = top_im.size
top_mode = top_im.mode
bot_size = bot_im.size
bot_mode = bot_im.mode

if ((top_size[0] != bot_size[0]) or (top_size[1] != bot_size[1])):
    print('sizes differ')
    sys.exit(-1)

if (top_mode != bot_mode):
    print('modes differ')
    sys.exit(-1)

# flop the top image
top_im = top_im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
# bot_im = bot_im.transpose(PIL.FLIP_LEFT_RIGHT)

# create top bottom image after transpose
border_inches = 0.8 / 2.54
border_pixels = border_inches * top_dpi
band_inches = 0.153 / 2.54
band_pixels = band_inches * top_dpi
top_bot_size = (int(top_size[0] * 2 + border_pixels + band_pixels + 4), int(border_pixels + top_size[1] + 4))
top_bot_im = PIL.Image.new('1', top_bot_size)
top_bot_im.info['dpi'] = (top_dpi, top_dpi)

# paste top into top_bot
top_bot_im.paste(top_im, (int(border_pixels), int(border_pixels)), None)
top_bot_im.paste(bot_im, (int(border_pixels + top_size[0] + band_pixels), int(border_pixels)))

if (top_bot_im.size[0] > top_bot_im.size[1]):
    top_bot_im = top_bot_im.rotate(90)

if (top_bot_name[-3:] == '.ps'):
    save_ps(top_bot_im, top_bot_name)
else:
    top_bot_im.save(top_bot_name, dpi=(top_dpi, top_dpi))

print_im_format(top_bot_im)
