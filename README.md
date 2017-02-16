## CNC curve emulator
this is a gcode emulator, which draws the picture accroding to the g-code which is widely used in CNC.

the output is stored in test.png under the folder.

## usage
$ python2 gcode_runner.py gcode_filename [width] [height]

## example
this is generated by a bezier curvy.

![img](http://asxalex.qiniudn.com/cnc_emulator.png)

## next
the script currently implemented `G00` and `G01` gcode commands, other commands need to be added to it.
