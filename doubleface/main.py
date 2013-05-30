#!/usr/bin/env python

import PIL.Image
import sys

top_name = 'top.png'
bot_name = 'bot.png'
top_bot_name = 'top_bot.png'
if (len(sys.argv) > 1): top_name = sys.argv[1]
if (len(sys.argv) > 2): bot_name = sys.argv[2]
if (len(sys.argv) > 3): top_bot_name = sys.argv[3]

top_im = PIL.Image.open(top_name)
bot_im = PIL.Image.open(bot_name)

top_dpi = 800.0
top_size = top_im.size
top_mode = top_im.mode
bot_size = bot_im.size
bot_mode = bot_im.mode

if ((top_size[0] != bot_size[0]) or (top_size[1] != bot_size[1])):
    print('sizes differ')
    sys.exit(-1)

if (top_mode != bot_mode):
    print('sizes differ')
    sys.exit(-1)

band_inches = 0.16 / 2.54
band_pixels = band_inches * top_dpi

top_bot_size = (int(top_size[0] * 2 + band_pixels), top_size[1])
top_bot_im = PIL.Image.new(top_mode, top_bot_size)

# flop the images
top_im = top_im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
# bot_im = bot_im.transpose(PIL.FLIP_LEFT_RIGHT)

top_bot_im.paste(top_im, (0, 0))
# top_bot_im.paste(bot_im, (int(top_size[0] + band_pixels), 0))

top_bot_im.save(top_bot_name)
