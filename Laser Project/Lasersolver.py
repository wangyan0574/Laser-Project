"""
EN.540.635 Software Carpentry
Laser Project - Maze Generation and Solving
Yan Wang & Siyu Chen
"""
import time


def load_bff(ftpr):
    """
    This will load the information of the board from the bff file

    **Parameters**
        ftpr: *str*, the string name of the file.
    **Returns**
        str_grid: *list*, 2d array, the starting grid of the board
        pts: *list*, target points need to be crossed by laser/lasers
        blk: *list*, kind and number of blocks we have for the board
        lsr: *list*, the start point and start vx vy of the laser

    """
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
    target = tuple(map(tuple, pts))
    return str_grid, target, blk, lsr


def get_laserpos(pt1, pt2):
    """
    This function will return the grid position of two adjacent points of 1 laser of 1 crossing
    block. Using x,y and x+vx, y+vy: to get the grid position from half block increment to full
    block increment. For example, the points are in a 8*8 grid, but the grid position are 4*4

    **Parameters**
        pt1: *list*, the xy of the current laser point (half increment, 8*8 style)
        pt2: *list*, the xy of the next laser point (half increment, 8*8 style)
    **Returns**
        x: *int*, the x value of the crossing blk, (full block increment 4*4 style)
        y: *int*, the y value of the crossing blk, (full block increment 4*4 style)

    """
    x = (pt1[0] + pt2[0]) // 4
    y = (pt1[1] + pt2[1]) // 4
    return x, y


def in_bound(blk_x, blk_y, grid):
    """
    This function will check if a block position (full, increment 4*4 style) is
    in the boundary of the grid

    **Parameters**
        blk_x: *int*, the x of the current block position (full increment, 4*4 style)
        blk_y: *int*, the y of the current block position (full increment, 4*4 style)
    **Returns**
        True or False

    """
    if 0 <= blk_x <= len(grid[0]) - 1 and 0 <= blk_y <= len(grid) - 1:
        return True
    else:
        return False


def calc_path(start_xy, start_vxvy, cur_grid, refract):
    """
    this function will calculate the path of the given laser: by storing its path in points (half
    point increment 8*8 style). By given the current grid, the function will alternate this laser's
    vx vy if it meet a block, either change direction (when hitting reflect); set vxvy to 0 (opaque);
    or reflect and create a new one (refract)

    **Parameters**
        start_xy: *list*, the xy of this laser's starting point 8*8 style grid position
        start_vxvy: *list*, the vx vy of this laser's starting direction (-1,-1) (1,-1) (1,1) or (-1,1)
        cur_grid: *tuple*, contain the cur_grid information, with all blocks placed on the grid
    **Returns**
        path: *list* the path of the given laser:[[x,y], [x+ vx,y+vy], ...]

    """
    path = []
    refract.lsrPath = []
    x, y = start_xy
    vx, vy = start_vxvy
    blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))
    path.append([x, y])
    while in_bound(blk_x, blk_y, cur_grid):
        if cur_grid[blk_y][blk_x] == "A":
            if x == blk_x * 2 + 1:
                vy = -vy
            else:
                vx = -vx
        elif cur_grid[blk_y][blk_x] == "B":
            return path
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
        blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))
        if in_bound(blk_x, blk_y, cur_grid):
            if cur_grid[get_laserpos((x, y), (x + vx, y + vy))[1]][get_laserpos((x, y), (x + vx, y + vy))[0]] == "A":
                return path
        x, y = (x + vx, y + vy)
        blk_x, blk_y = get_laserpos((x, y), (x + vx, y + vy))
        path.append([x, y])
    return path


class Block:
    """
    the block class, note reflect and opaque share the same class, but refract blocks will have
    its own laser as its attribute.
    """

    def __init__(self, total, blktype):
        self.total = total
        self.position = [0] * total
        self.blktype = blktype

    def get_position(self):
        return self.position


class Refract(Block):
    def __init__(self, total, blktype):
        Block.__init__(self, total, blktype)
        self.lsrPath = []


class Laser:
    """
    the laser class, there is only 1 Laser object for this program, but the length of the
    laser object may be more than 1 depend on the setup. Each their path will be stored
    in the Path attribute.
    """

    def __init__(self, str_xy, str_dir):
        self.str_xy = str_xy
        self.str_dir = str_dir
        self.Path = [0] * len(str_xy)

    def get_curpath(self):
        return self.Path


def solve(ftpr):
    """
    this function will takes the bff file as input, it then initialize the values using the load_bff
    function. Follow up by initialize all A, B, C block objects with their type and total number.
    The laser is then initialized. It then run a couple of loops to try out all possible combination
    of block setups, storing in set. Finally, it will validate the stored grids by calling the check
    function to return the solution.

    **Parameters**
        ftpr: *str*, the name of the bff file
    **Returns**
        grid: *tuple*, the final solution of the grid
    """
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
                grid = tuple(map(tuple, cur_grid))
                combination.add(grid)
    for b in whatsavailable[1:]:
        new_comb = set()
        for cur_grid in combination:
            for x in range(len(cur_grid[0])):
                for y in range(len(cur_grid)):
                    if cur_grid[y][x] == 1:
                        new_cur_grid = [[c for c in r] for r in cur_grid]
                        new_cur_grid[y][x] = b
                        new_grid = tuple(map(tuple, new_cur_grid))
                        new_comb.add(new_grid)
        combination = new_comb

    for comb in combination:
        if check_answer(comb, pts, lsr, C):
            return comb, str_grid


def check_answer(cur_grid, pts, lsr, C):
    """
    this function will check the grid be given, calculate the lasers from the current grid. And
    see if all the points are inside the laser path. Please note since we store the refract lasers
    in the C object, we need to input C as well to see if any target points are hit by the C lsr.

    the function will calulate the path of lasers by using the calc_path function, if a target pt
    is in the path, it will remove that pt from the target array.

    **Parameters**
        cur_grid: *tuple*, 2d tuple that stores the current combination of blocks setup
        pts: *list*, the points we want our laser to hit
        lsr: *laser object*, the lsr object that we store the path
        C: *refract block object*, the object we also store laser that may be created by refract
            block
    **Returns**
        True / False, whether we find all target pts in the paths or not.

    """
    target = [[c for c in r] for r in pts]
    for i in range(len(lsr.Path)):
        lsr.Path[i] = calc_path(lsr.str_xy[i], lsr.str_dir[i], cur_grid, C)
        for j in lsr.Path[i]:
            if j in target:
                target.remove(j)
    if len(C.lsrPath) != 0:
        for i in C.lsrPath:
            if i in target:
                target.remove(i)
    if len(target) == 0:
        return True
    else:
        return False


def save_sol(solved_grid, original_grid, bff):
    name = bff.split(".")[0] + "_SOLVED.txt"
    f = open(name, "w+")
    f.write("Below is the solution for: "
            + bff + "\n\n" + "Legend: \n1: free space" +
            "\n0: unavailable space, no blocks can move here\n" +
            "A: reflect block\nB: opaque block\n" +
            "C: refract block\n\n" +
            "Note: if there are fixed blocks in the original grid, the following\n" +
            "      solved grid will present that fixed block to its type. Hence it\n" +
            "      may appear to be more available blocks than the original.\n" +
            "      Simply put the blocks accordingly!\n\n"
            )

    f.write("Original:\n")
    for row in original_grid:
        f.write(" ".join(str(s) for s in row) + '\n')
    f.write("\nSolved:\n")
    for row in solved_grid:
        f.write(" ".join(str(s) for s in row) + '\n')
    f.close()


if __name__ == '__main__':
    print("\n*** Please enter the string name of the bff file name ***")
    ftpr = input()
    print("\n*** Please note some boards may take up to 18s to solve ***")
    start_time = time.time()
    solved, original = solve(ftpr)
    save_sol(solved, original, ftpr)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("*** Now please check the solved generated txt file :) ***")
