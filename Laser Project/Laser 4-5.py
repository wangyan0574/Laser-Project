"""
EN.540.635 Software Carpentry
Laser Project - Maze Generation and Solving
Yan Wang & Siyu Chen
"""
import numpy as np


def load_bff(ftpr):
    f = open(ftpr, "r")
    bff = f.readlines()
    f.close()
    str_grid = []
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
        split = l.split()
        for i, ele in enumerate(split):
            if ele == "0":
                split[i] = 0
            if ele == "1":
                split[i] = 1
        str_grid.append([x for x in split])

    return str_grid, pts, blk, lsr


def get_laserpos(pt1, pt2):
    for i in (pt1[0], pt2[0]):
        if (i % 2) != 0:
            x = i
    for j in (pt1[1], pt2[1]):
        if (j % 2) != 0:
            y = j
    return x // 2, y // 2


def in_bound(x, y, grid):
    if 0 <= x <= 2 * len(grid[0]) and 0 <= y <= 2 * len(grid):
        return True
    else:
        return False


def calc_path(start_xy, start_vxvy, cur_grid, refract):
    path = []
    x, y = start_xy
    vx, vy = start_vxvy
    while (in_bound(x, y, cur_grid)) & (vx != 0):
        cur_pt = x, y
        path.append([x, y])
        blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))

        if cur_grid[blk_y][blk_x] == "A":
            if x - blk_x == 0:
                vy = -vy
            else:
                vx = -vx
        elif cur_grid[blk_y][blk_x] == "B":
            vy = 0
            vx = 0
        else:
            # we now introduce a new laser from this refract block. Its first element
            # will tell which refract block it belongs to. (The original laser will have
            # this element of 0, thus the "created lsr" will have block's index + 1)
            refract.lsrPath = calc_path([x, y], [vx, vy], cur_grid, refract)
            # then reflect the original laser by alter its direction just as reflect blk
            if x - blk_x == 0:
                vy = -vy
            else:
                vx = -vx
        x, y = (x + vx, y + vy)
    return path

'''
def possible_pos(cur_grid):
    selection = []
    for x in range(len(cur_grid[0])):
        for y in range(len(cur_grid)):
            if (cur_grid[y][x] != 0) & (cur_grid[y][x] != "A") & (cur_grid[y][x] != "B") & (cur_grid[y][x] != "C"):
                selection.append([x, y])
    return selection
'''

class Block:
    def __init__(self, total, blktype):
        self.total = total
        self.position = [0] * total
        self.blktype = blktype
        self.cur_total = total

    def get_position(self):
        return self.position


class Refract(Block):
    def __init__(self, total, blktype):
        Block.__init__(self, total, blktype)
        self.lsrPath = []


class Laser:
    def __init__(self, str_xy, str_dir):
        self.str_xy = str_xy
        self.str_dir = str_dir
        self.Path = [0] * len(str_xy)

    def get_curpath(self):
        return self.Path


def solve(ftpr):
    # initializing all vars
    str_grid, pts, blk, lasers = load_bff(ftpr)
    A = Block(blk[0], "A")
    B = Block(blk[1], "B")
    C = Refract(blk[2], "C")

    cur_grid = str_grid
    lasers_xy = []
    lasers_dir = []
    for i in range(len(lasers)):
        lasers_xy.append([lasers[i][0], lasers[i][1]])
        lasers_dir.append([lasers[i][2], lasers[i][3]])
    lsr = Laser(lasers_xy, lasers_dir)
    blk_on_grid = []
    whatsavailable = []
    for i in [A, B, C]:
        for j in range(len(i.total)):
            whatsavailable.append(i.blktype)
    combination = []
    b = whatsavailable[0]
    for x in range(len(cur_grid[0])):
        for y in range(len(cur_grid)):
            if cur_grid[y][x] == 1:
                cur_grid[y][x] = b
            combination.append(cur_grid)
    for b in whatsavailable[1:]:
        new_comb = []
        for cur_grid in combination:
            for x in range(len(cur_grid[0])):
                for y in range(len(cur_grid)):
                    if cur_grid[y][x] == 1:
                        new_grid = [[c for c in r] for r in cur_grid]
                        new_grid[y][x] = b
                        new_comb.append(new_grid)
        combination = new_comb

    for grid in combination:
        if check_answer(grid, pts, lsr, C):
            return grid

    '''
    while len(blk_on_grid) <= sum(blk):
        whatsavailable = []
        selection = []
        cur_selection = possible_pos(cur_grid)
        for i in [A, B, C]:
            if i.cur_total != 0:
                whatsavailable.append(i.blktype)

        if len(whatsavailable) != 0:
            select_type = np.random.choice(whatsavailable)
            for pos in cur_selection:
                if pos not in trial[len(blk_on_grid)][select_type]:
                    selection.append(pos)
            pos = selection[0]
            cur_grid[pos[1]][pos[0]] = select_type
            trial[len(blk_on_grid)][select_type].append(select_type)
            blk_on_grid.append([pos, select_type])
            for i in [A, B, C]:
                if i.blktype == select_type:
                    i.cur_total = i.cur_total - 1

        elif whatsavailable == [] and blk_on_grid == []:
            (last_blkx, last_blky), last_blktype = blk_on_grid[-1]
            cur_grid[last_blky][last_blkx] = last_blktype
            for i in [A, B, C]:
                if i.blktype == last_blktype:
                    i.cur_total = i.cur_total + 1
            if len(blk_on_grid) != sum(blk):
                trial[len(blk_on_grid)] = {'A': [], 'B': [], 'C': []}
            blk_on_grid.pop()

        if len(blk_on_grid) == sum(blk):
            if check_answer(cur_grid, pts, lsr, C):
                return cur_grid
            else:
                continue
    '''


def check_answer(cur_grid, pts, lsr, C):
    target = pts
    for i in range(len(lsr.Path)):
        lsr.Path[i] = calc_path(lsr.str_xy[i], lsr.str_dir[i], cur_grid, C)
        for j in lsr.Path[i]:
            if j in target:
                target.remove(j)

    if len(C.lsrPath) != 0:
        for i in C.lsrPath:
            if i in target:
                target.remove(i)
    return len(target) == 0


if __name__ == '__main__':
    print(solve("tiny_5.bbf"))
