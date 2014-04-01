
import itertools
from numpy import ndarray, shape
from pymclevel import MCSchematic
from pymclevel.materials import Block
from pymclevel.box import BoundingBox, Vector

displayName = "SmoothSurface"

inputs = (
    ("Surface material", "blocktype"),
    ("Surrounding material", "blocktype"),
    ("Passes", 1)
)

def perform(level, box, options):
    solidBlock = options["Surface material"]
    airBlock = options["Surrounding material"]
    offsets = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
    solidCount = ndarray(box.size)
    airCount = ndarray(box.size)

    for _ in xrange(options["Passes"]):
        for p in box.positions:
            p = Vector(*p)
            do = p - box.origin
            solidCount[do] = 0
            airCount[do] = 0
            for o in offsets:
                n = p + o
                if n in box:
                    block = level.blockAt(*n)
                    if block == solidBlock.ID:
                        solidCount[do] += 1
                    if block == airBlock.ID:
                        airCount[do] += 1

        for p in box.positions:
            p = Vector(*p)
            do = p - box.origin
            block = level.blockAt(*p)
            if block == solidBlock.ID and airCount[do] >= 5:
                level.setBlockAt(p[0], p[1], p[2], airBlock.ID)
            elif block == airBlock.ID and solidCount[do] >= 5:
                level.setBlockAt(p[0], p[1], p[2], solidBlock.ID)
                    
    level.markDirtyBox(box)
