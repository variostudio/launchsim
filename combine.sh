#!/bin/bash

mencoder mf://screens/*.tga -mf  w=1000:h=600:fps=24:type=tga -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o flight.avi

