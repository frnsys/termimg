from __future__ import division

import os
import curses
from subprocess import Popen, PIPE, check_output


def render_image(img_path, x=0, y=0, margin=0, scale_to_fit=True, keep_aspect=True, width='', height='', x_offset=0, y_offset=0, bin='/usr/lib/w3m/w3mimgdisplay'):
    """
    renders an image to a terminal using `w3mimgdisplay` (only works on supported X11 terminals, such as urxvt).
    the terminal cursor will be placed after the image (if possible; if it takes up the entire terminal space,
    the cursor is moved to the last row)

    this is based on research from <http://blog.z3bra.org/2014/01/images-in-terminal.html>.

    args:
        img_path: path to image to display
        x: x position, in pixels (top-left anchor)
        y: y position, in pixels (top-left anchor)
        margin: margin around image, in terminal rows/columns
        scale_to_fit: scale image automatically to fit within available space (taking margins into account)
        keep_aspect: maintain aspect ratio if only one of width or height is specified
        width: width, in pixels, image should be rendered at
        height: height, in pixels, image should be rendered at
        x_offset: x offset, in pixels
        y_offset: y offset, in pixels
        bin: path to the `w3mimgdisplay` binary"""

    img_path = os.path.expanduser(img_path)
    img_width, img_height = _image_size(img_path, bin)
    aspect_ratio = img_width/img_height

    # prep image dimensions as necessary
    if not height:
        height = img_height
        if not width and keep_aspect:
            width = height * aspect_ratio
    if not width:
        width = img_width
        if not height and keep_aspect:
            height = width/aspect_ratio

    # get some useful info about the terminal
    term_px_width, term_px_height = _term_px_size(bin)
    term_width, term_height = _term_size()
    px_per_row = term_px_height/term_height
    px_per_col = term_px_width/term_width

    # setup margin
    x_margin_px = int(px_per_col * margin)
    y_margin_px = int(px_per_row * margin)

    # get available canvas dimensions
    canvas_px_width = term_px_width - (x_margin_px * 2)
    canvas_px_height = term_px_height - (y_margin_px * 2)

    if scale_to_fit:
        width, height = _scale_to_fit(width, height, canvas_px_width, canvas_px_height)

    # dimensions must be integers
    height = int(height)
    width = int(width)
    x += x_margin_px
    y += y_margin_px

    # prep command to pipe to w3mimgdisplay
    cmd = '0;{n};{x};{y};{width};{height};{x_offset};{y_offset};{source_width};{source_height};{img_path}\n4;\n3;'.format(
        n=1, # number of images
        x=x,
        y=y,
        width=width,
        height=height,
        x_offset=x_offset,
        y_offset=y_offset,
        source_width=img_width,
        source_height=img_height,
        img_path=img_path)

    # pipe command to w3mimgdisplay to render the image
    ps = Popen(bin, stdin=PIPE, stdout=PIPE)
    ps.stdin.write(cmd)
    ps.stdin.flush()

    # place terminal cursor after the image
    # (or the last row of the image, if it takes up the full terminal)
    total_height = y + height + y_offset
    row = int(total_height/px_per_row)
    _tput(row, 0)


def _scale_to_fit(width, height, max_width, max_height):
    """scales input dimensions to fit within max dimensions"""
    height_scale = height/max_height
    width_scale = width/max_width
    scale = max(height_scale, width_scale)
    if scale > 1:
        height /= scale
        width /= scale
    return width, height


def _term_size():
    """get terminal dimensions in rows and columns"""
    win = curses.initscr()
    x, y = win.getmaxyx()
    curses.endwin()
    return x, y


def _term_px_size(bin):
    """get terminal dimensions in pixels"""
    term_px_width, term_px_height = check_output([bin, '-test']).strip().split()
    return int(term_px_width), int(term_px_height)


def _tput(row, col):
    """place the terminal cursor at the specified row and column"""
    print('\033[{row};{col}H'.format(row=row, col=col))


def _image_size(img_path, bin):
    """get the dimensions of an image, in pixels"""
    ps = Popen(bin, stdout=PIPE, stdin=PIPE)
    out, err = ps.communicate(input='5;{}'.format(img_path))
    width, height = out.strip().split()
    return int(width), int(height)