# Laser-Project
Laser group project for Software Carpenter JHU

This project will solve the app game Lazors' puzzles

HOW TO USE:

    1. Be sure to have your bff file in the same directory (bff: board file format, explained below)
    2. Simply load the program "Lazersolver.py" in your python IDE
    3. After prompt, simply type the name of the file (including the file extension, this case is .bff): for example, tiny_5.bff
    4. After some time, the program will output a txt file containing the original grid as well as the solved grid.
    
    
BFF file:\
Board file format is how we save the board information. (Check out any bff in the repo to know how they are formatted:) 
Essentially, BFFs will include:
    
    1. The starting grid, with spaces in the form of
        - "o" (a free space, all available blocks can move here)
        - "x" (a filled space, non blocks can move here)
        - "A" (a fixed reflect block, the white block)
        - "B" (a fixed opaque block, the brown one)
        - "C" (a fixed refract block, the transparent one)
        ***just like the examples of bff in the repo, be sure to use spaces to separate the spaces types! 
        And use "GRID START" and "GRID STOP" to indicate the grid style***
     
    2. What kind of blocks we will have and how many are there
        - the line will start with "A" or "B" or "C", follow up by how many A or B or C is available for us to use
    4. The laser
        - the line will start with "L", follow by its starting position (in half increments, if a grid is 4 by 4, half increment style
        will be 8*8), and direction: -1,-1 or 1,-1 or 1,1 or -1,1
    3. The target pts we want to hit by the laser (also in half increment axis style)
        - the line start with P, and follow by x and y position
    Check out "mad_1.bff" to know more about the specific styling of bff file.
    
HOW TO READ THE OUTPUT TXT:\
The output txt will be stored with "name + _SOLVED.txt" filename: for example, "tiny_5.bff" will have an output of "tiny_5_SOLVED.txt"\
Inside the txt will have some legend info and contain the original grid as well as the solved grid (all in the same grid style of bff files):\

***Please note the fixed blocks will also be present by the style name of it in the solved grid***: \
(this means a fixed opaque block and a placed opaque will both be "B"), for example:

***tiny_5***

        Original:                    Solved:
            1 B 1                       A B A
            1 1 1                       1 1 1
            1 1 1                       A C 1
        
Note: in the original grid we have a fixed opaque block ("B") at grid's row 1, col 2. It will be at the same location in the solved grid, too. \
But we can certainly figure that out by just comparing the two.

Thx, happy puzzling!
    
