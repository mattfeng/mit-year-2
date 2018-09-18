#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel_naive(self, x, y):
        return self.pixels[y * self.width + x] # should be a single index, not multiple
    
    def get_pixel(self, x, y):
        # Add boundary checks
        if x < 0:
            x = 0
        if x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        if y >= self.height:
            y = self.height - 1
        return self.get_pixel_naive(x, y)

    def set_pixel(self, x, y, c):
        self.pixels[y * self.width + x] = c # same as get_pixel

    def apply_per_pixel(self, func):
        result = Image.new(self.width, self.height) # swap height and width
        for y in range(result.height):
            for x in range(result.width):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor) # swap x, y, indent
        return result

    def inverted(self):
        return self.apply_per_pixel(lambda c: 255 - c) # should be changed to 255

    def hadamard(self, A, B): # element-wise vector product
        assert(len(A) == len(B))
        ret = [a * b for a, b in zip(A, B)]
        return ret
    
    def cross(self, *sets):
        assert(len(sets) > 0)
        def cross2(set1, set2):
            ret = []
            for i in set1:
                for j in set2:
                    ret.append((*i, j))
            return ret
        
        ret = [(elt, ) for elt in sets[0]]
        for set_ in sets[1:]:
            ret = cross2(ret, set_)
        return ret
    
    def clip(self, num):
        return max(0, min(num, 255))

    def correlate(self, kernel, clip=True):
        dim = len(kernel[0])
        off = list(map(lambda d: d - dim // 2, range(dim)))
        offsets = self.cross(off, off)
        corr = []
        for y in range(self.height):
            for x in range(self.width):
                result = sum(self.get_pixel(x + dx, y + dy) * kernel[dy + dim // 2][dx + dim // 2] for dx, dy in offsets)
                if clip:
                    result = self.clip(int(round(result)))
                corr.append(result)
        return corr

    def blurred(self, n):
        blur_filter = [[1 / (n * n) for __ in range(n)] for _ in range(n)]
        return Image(self.width, self.height, self.correlate(blur_filter))
    
    def sharpened(self, n):
        sharpen_filter = [[-1 / (n * n) for __ in range(n)] for _ in range(n)]
        sharpen_filter[n // 2][n // 2] = 2 - (1 / (n * n))
        return Image(self.width, self.height, self.correlate(sharpen_filter))

    def edges(self):
        Kx = [[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]]

        Ky = [[-1, -2, -1],
              [ 0,  0,  0],
              [ 1,  2,  1]]

        kx_filtered = self.correlate(Kx, clip=False)
        ky_filtered = self.correlate(Ky, clip=False)
        edge_filtered = [self.clip(int(round((x ** 2 + y ** 2) ** 0.5))) for x, y in zip(kx_filtered, ky_filtered)]
        return Image(self.width, self.height, edge_filtered)
    
    def compute_energy_map(self):
        edges = self.edges().pixels
        energy = {}
        for x in range(self.width):
            energy[x] = sum(edges[y * self.width + x] for y in range(self.height))
        return energy
    
    def min_energy_col(self):
        energy = self.compute_energy_map()
        min_energy = sorted(energy.items(), key=lambda x: x[1])[0]
        return min_energy[0]
    
    def delete_col(self, ix):
        for y in range(self.height - 1, -1, -1):
            del self.pixels[y * self.width + ix]

    def seam_carve(self, num_cols):
        for _ in range(num_cols):
            self.delete_col(self.min_energy_col())
            self.width -= 1
        
    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    im = Image.load("test_images/bluegill.png")
    inv = im.inverted()
    inv.save("inverted_bluegill.png")

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
