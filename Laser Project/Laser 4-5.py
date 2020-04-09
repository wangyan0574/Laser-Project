"""
EN.540.635 Software Carpentry
Laser Project - Maze Generation and Solving
Yan Wang & Siyu Chen
"""
from typing import List


def load_bff(ftpr):
    f = open(ftpr, "r")
    bff = f.readlines()
    f.close()
    start_grid = []
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
                lsr.append([int(laser[3]), int(laser[4]), int(laser[1]), int(laser[2])])

    # initialized the grid into a 2d array
    for l in bff[start:stop]:
        l = l.replace("o", "1")
        l = l.replace("x", "0")
        start_grid.append([int(x) for x in l.split()])

    return start_grid, pts, blk, lsr


def get_laserpos(pt1, pt2):
    for i in (pt1[0], pt2[0]):
        if (i % 2) != 0:
            x = i
    for j in (pt1[1], pt2[1]):
        if (j % 2) != 0:
            y = j
    return x/2, y/2
"""
def check_pos(pt1, pt2, cur_grid):
    x, y = get_laserpos(pt1, pt2)
    if cur_grid(x, y):
        return 0
    else:
        return 1
"""
def in_bound(x, y, grid):
    if 0 <= x <= 2 * len(grid[0]) and 0 <= y <= 2 * len(grid):
        return True
    else:
        return False


def calc_path(start_x, start_y, start_vx, start_vy, grid, cur_grid):
    path = []
    x, y = start_x, start_y
    vx, vy = start_vx, start_vy
    while (in_bound(x, y, grid)) & (vx != 0):
        cur_pt = x, y
        path.append(x,y)
        blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))

        if cur_grid(blk_x, blk_y) == "A":
            if x - blk_x == 0:
                vy = -vy
            else:
                vx = -vx
        elif cur_grid(blk_x, blk_y) == "B":
            vy = 0
            vx = 0
        else:
            # we now introduce a new laser from this refract block. Its first element
            # will tell which refract block it belongs to. (The original laser will have
            # this element of 0, thus the "created lsr" will have block's index + 1)
            refract.lsr = [[refract.pos.index([x, y])]]
            refract.lsr.append(calc_path(x, y, vx, vy, grid, cur_grid))
            # then reflect the original laser by alter its direction just as reflect blk
            if x - blk_x == 0:
                vy = -vy
            else:
                vx = -vx
        x, y = (x + vx, y + vy)
    return path


class Block:
    def __init__(self, total, blktype):
        self.total = total
        self.position = []
        self.blktype = blktype
    def get_position(self):
        return self.position

class Opaque(Block):
    def __init__(self, total, blktype):
        Block.__init__(self, total, blktype)
        self.lsr = []

class Laser:
    def __init__(self, str_xy, str_dir):
        self.str_pos = str_pos
        self.str_dir = str_dir
        self.CurPath = []

    def get_CurPath(self):
        return self.CurPath




"""
for i in xrange(0, len(prices)):
    exec("price%d = %s" % (i + 1, repr(prices[i])));
"""
def main():

