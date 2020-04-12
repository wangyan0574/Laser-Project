"""
EN.540.635 Software Carpentry
Laser Project - Maze Generation and Solving
Yan Wang & Siyu Chen
"""


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
    for line in bff[stop:]:
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
    x = (pt1[0] + pt2[0]) // 4
    y = (pt1[1] + pt2[1]) // 4
    return x, y


def in_bound(blk_x, blk_y, grid):
    if 0 <= blk_x <= len(grid[0]) - 1 and 0 <= blk_y <= len(grid) - 1:
        return True
    else:
        return False


def calc_path(start_xy, start_vxvy, cur_grid, refract):
    path = []
    x, y = start_xy
    vx, vy = start_vxvy
    blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))
    path.append([x,y])
    while (in_bound(blk_x, blk_y, cur_grid)) & (vx != 0):
        #print(blk_x, blk_y)
        if cur_grid[blk_y][blk_x] == "A":
            if x == blk_x * 2 + 1:
                vy = -vy
            else:
                vx = -vx
        elif cur_grid[blk_y][blk_x] == "B":
            vy = 0
            vx = 0
        elif cur_grid[blk_y][blk_x] == "C":
            # we now introduce a new laser from this refract block. Its first element
            # will tell which refract block it belongs to. (The original laser will have
            # this element of 0, thus the "created lsr" will have block's index + 1)
            refract.lsrPath = calc_path([x + vx, y + vy], [vx, vy], cur_grid, refract)
            # then reflect the original laser by alter its direction just as reflect blk
            if x == blk_x * 2 + 1:
                vy = -vy
            else:
                vx = -vx
        x, y = (x + vx, y + vy)
        blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))
        path.append([x,y])
    return path


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

    lasers_xy = []
    lasers_dir = []
    for i in range(len(lasers)):
        lasers_xy.append([lasers[i][0], lasers[i][1]])
        lasers_dir.append([lasers[i][2], lasers[i][3]])
    lsr = Laser(lasers_xy, lasers_dir)
    whatsavailable = []
    for i in [A, B, C]:
        for j in range(i.total):
            whatsavailable.append(i.blktype)
    combination = set()
    b = whatsavailable[0]
    for x in range(len(str_grid[0])):
        for y in range(len(str_grid)):
            cur_grid = [[c for c in r] for r in str_grid]
            if cur_grid[y][x] == 1:
                cur_grid[y][x] = b
                grid = tuple(map(tuple,cur_grid))
                combination.add(grid)
    for b in whatsavailable[1:]:
        new_comb = set()
        for cur_grid in combination:
            for x in range(len(cur_grid[0])):
                for y in range(len(cur_grid)):
                    if cur_grid[y][x] == 1:
                        new_cur_grid = [[c for c in r] for r in cur_grid]
                        new_cur_grid[y][x] = b
                        new_grid = tuple(map(tuple,new_cur_grid))
                        new_comb.add(new_grid)
        combination = new_comb
        
    '''
    print(len(combination))
    
    grid = [['A','B','A'],[1,1,1],['A','C',1]]
    
    if grid in combination:
        print('TRUE')
    else:
        print('No')
    
    if check_answer(grid, pts, lsr, C):
        return grid
    else:
        return False
    '''
    for grid in combination:
        if check_answer(grid, pts, lsr, C):
            return grid


def check_answer(cur_grid, pts, lsr, C):
    target = [[c for c in r] for r in pts]
    for i in range(len(lsr.Path)):
        lsr.Path[i] = calc_path(lsr.str_xy[i], lsr.str_dir[i], cur_grid, C)
        for j in lsr.Path[i]:
            if j in target:
                target.remove(j)
        #print('lsr',lsr.Path[i])

    if len(C.lsrPath) != 0:
        for i in C.lsrPath:
            if i in target:
                target.remove(i)
        #print('C',C.lsrPath)
    #print('target',target)
    return len(target) == 0

if __name__ == '__main__':
    print(solve("mad_7.bff"))
