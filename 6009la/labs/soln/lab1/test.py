#!/usr/bin/env python3

import os
import lab
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

class TestImage(unittest.TestCase):
    def test_load(self):
        result = lab.Image.load('test_images/centered_pixel.png')
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)


class TestInvert(unittest.TestCase):
    def test_invert_1(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.inverted()
        expected = lab.Image(11, 11,
                             [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        print(result.pixels)
        self.assertEqual(result, expected)

    def test_invert_2(self):
        # REPLACE THIS from your test case from section 3.1
        im = lab.Image(4, 1, [20, 85, 144, 197])
        result = im.inverted()
        expected = lab.Image(4, 1, [235, 170, 111, 58])
        self.assertEqual(result, expected)

    def test_invert_images(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
                result = lab.Image.load(inpfile).inverted()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)


class TestFilters(unittest.TestCase):
    def test_blur(self):
        for kernsize in (1, 3, 7):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
                    result = lab.Image.load(inpfile).blurred(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(result,  expected)

    def test_sharpen(self):
        for kernsize in (1, 3, 9):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
                    result = lab.Image.load(inpfile).sharpened(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(result,  expected)

    def test_edges(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
                result = lab.Image.load(inpfile).edges()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)
    
    def test_trivial_5(self):
        im = lab.Image.new(6, 5, [0] * 30)
        expected = lab.Image.new(6, 5, [0] * 30)
        result = im.blurred(5)
        self.assertEqual(result, expected)

    def test_trivial_7(self):
        im = lab.Image(6, 5, [0] * 30)
        expected = lab.Image(6, 5, [0] * 30)
        result = im.blurred(5)
        self.assertEqual(result, expected)

    def test_centered_1(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        expected = lab.Image(11, 11, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        result = im.blurred(1)
        self.assertEqual(result, expected)

    def test_centered_3(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        expected = lab.Image(11, 11, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                                          0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                                          0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        result = im.blurred(3)
        print(result.pixels)
        self.assertEqual(result, expected)




if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
