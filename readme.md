This module provides a function, `show_image`, which lets you render an image (without fumbly ASCII representations) to a supported X11 terminal (such as `urxvt`).

This requires `w3mimgdisplay` (this is usually available in package managers, e.g. `apt-get install w3m-img`).

Usage:

    from termimg import render_image
    render_image('~/downloads/masashi_wakui.png', margin=2)

This is all based on [research by z3bra](http://blog.z3bra.org/2014/01/images-in-terminal.html).

Arguments to `render_image`:

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
    bin: path to the `w3mimgdisplay` binary

# Example

![`termimg` example](shot.png)

Photo by [Masashi Wakui](https://www.flickr.com/photos/megane_wakui/).

# License

The MIT License (MIT)

Copyright (c) 2016 Francis Tseng

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.