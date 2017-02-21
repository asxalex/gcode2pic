#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 alex <alex@localhost>
#
# Distributed under terms of the MIT license.

from PIL import Image
import sys

class Command(object):
    def __init__(self, line, curx, cury, curz):
        self.funcmap = {
                "g1": self.handle_g1,
                "g0": self.handle_g0,
                }

        self.curx = curx
        self.cury = cury
        self.curz = curz

        codes = line.split()
        if len(codes) > 0 and codes[0].lower().startswith("n"):
            codes.pop(0)
        index = None
        for i in range(len(codes)):
            codes[i] = codes[i].lower()
            if len(codes[i]) > 2 and codes[i][0] == '/' and codes[i][1] == "/":
                index = i
        if index is not None:
            index = len(codes) - index

        if index is not None:
            for i in range(index):
                codes.pop()
        self.codes = codes

    def handle_g0(self, img):
        x1 = self.curx
        y1 = self.cury
        z1 = self.curz
        for i in range(1, len(self.codes)):
            c = self.codes[i][0]
            temp = self.codes[i][1:]
            if c == 'x':
                x1 = float(temp)
            elif c == 'y':
                y1 = float(temp)
            elif c == 'z':
                z1 = float(temp)
        return x1, y1, z1

    def handle_g1(self, img):
        x1 = self.curx
        y1 = self.cury
        z1 = self.curz
        for i in range(1, len(self.codes)):
            c = self.codes[i][0]
            temp = self.codes[i][1:]
            if c == 'x':
                x1 = float(temp)
            elif c == 'y':
                y1 = float(temp)
            elif c == 'z':
                z1 = float(temp)
        if z1 > 0: ## don't do the curve, move to that location
            print z1
            return x1, y1, z1

        x0 = self.curx
        y0 = self.cury
        if x1 == x0 and y1 == y0:
            return x1, y1, z1

        if x1 == x0:
            if y1 == y0:
                img[(x0, y0)] = 0
                return x1, y1, z1
            tx = round(x0)
            ty0 = int(round(y0))
            ty1 = int(round(y1))
            for i in range(ty1, ty0, 1 if ty1 < ty0 else -1):
                img[(tx, i)] = 0
            img[(tx, ty1 if ty1 < ty0 else ty0)] = 0
            return x1, y1, z1

        k = 1.0 * (y1 - y0) / (x1 - x0)
        b = 1.0 * (x1*y0 - x0*y1) / (x1-x0)

        x = self.curx
        y = self.cury
        if x0 > x1:
            while x > x1:
                y = k * x + b
                y = round(y)
                try:
                    img[(x, y)] = 0
                    print (x, y), " is colored"
                except Exception, e:
                    print "[ATTENTION] there are points out of the pic(%f, %f)" % (x, y)
                x -= 1
        else:
            while x < x1:
                y = k * x + b
                y = round(y)
                try:
                    img[(x, y)] = 0
                    print (x, y) , "is colored"
                except Exception, e:
                    print "[ATTENTION] there are points out of the pic(%f, %f)" % (x, y)
                x += 1

        return x1, y1, z1

    def action(self, img):
        if len(self.codes) == 0:
            return 0,0,0
        command_name = self.codes[0]
        if command_name == "g01" or command_name == "g1":
            return self.funcmap["g1"](img)

        if command_name == "g00" or command_name == "g0":
            return self.funcmap["g0"](img)

        return 0, 0, 0

class Runner(object):
    def __init__(self, width=1000, height=1000):
        self.width = width
        self.height = height
        self.img = Image.new("L", (width, height), 255)
        self.img_array = self.img.load()
        self.currentx = 0
        self.currenty = 0
        self.currentz = 0

    def run_code(self, filename, outname="test.png"):
        try:
            fp = open(filename)
        except Exception, e:
            print e
            return
       
        currentx = self.currentx
        currenty = self.currenty
        currentz = self.currentz

        while True:
            line = fp.readline()
            if not line:
                break
            command = Command(line, currentx, currenty, currentz)
            currentx, currenty, currentz = command.action(self.img_array)

        self.img.save(outname, "PNG")

def get_max_x_y(filename):
    max_x = 0
    max_y = 0
    for line in open(filename):
        codes = line.split()
        if len(codes) <= 0:
            continue
        for i in codes:
            if i.lower().startswith("x"):
                temp = float(i[1:])
                if temp > max_x:
                    max_x = temp
                continue
            if i.lower().startswith("y"):
                temp = float(i[1:])
                if temp > max_y:
                    max_y = temp
                continue

    max_x = int(max_x * 1.1)
    max_y = int(max_y * 1.1)
    return max_x, max_y
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python2 gcode_runner.py nc_filename [output_filename] [width] [height]"
        sys.exit(-1)

    x = 500
    y = 500
    max_x = -1
    max_y = -1
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    if len(sys.argv) >= 3:
        outname = sys.argv[2]
    else:
        outname = "test.png"

    if len(sys.argv) >= 4:
        max_x = int(sys.argv[3])
    if len(sys.argv) >= 5:
        max_y = int(sys.argv[4])


    if max_x == -1 and max_y == -1:
        max_x, max_y = get_max_x_y(filename)

    runner = Runner(max_x, max_y)
    runner.run_code(filename, outname)

