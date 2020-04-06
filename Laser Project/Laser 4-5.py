"""
EN.540.635 Software Carpentry
Laser Project - Maze Generation and Solving
"""
from typing import List


def load_bff(ftpr):
    f = open(ftpr, "r")
    bff = f.readlines()
    f.close()
    grid = []
    blk = [0] * 3
    pts = []
    lsr = []
    for i, line in enumerate(bff):
        if "GRID START" in line:
            start = i + 1
        if "GRID STOP" in line:
            stop = i
        if not line.startswith("#"):
            if line.startswith("A"):
                blk[0] = int(line[2])
            if line.startswith("B"):
                blk[1] = int(line[2])
            if line.startswith("C"):
                blk[2] = int(line[2])
            if line.startswith("P"):
                pts.append([int(line[2]), int(line[4])])
            if line.startswith("L"):
                laser = line.split()
                lsr.append([int(laser[1]), int(laser[2]), int(laser[3]), int(laser[4])])

    # initialized the grid into a 2d array
    for l in bff[start:stop]:
        l = l.replace("o", "1")
        l = l.replace("x", "0")
        grid.append([int(x) for x in l.split()])

    return grid, pts, blk, lsr
