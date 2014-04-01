
import itertools
from numpy import zeros
from pymclevel import MCSchematic
from pymclevel.materials import Block
from pymclevel.box import BoundingBox, Vector

inputs = (
    ("X", ("+", "-")),
    ("Z", ("+", "-")),
)

def perform(level, box, options):
    dim = box.size[0]
    if dim != box.size[2]:
        raise Exception("Selection must have equal length and width")

    step =  (int(options["X"] + "1"), 0, int(options["Z"] + "1"))

    buf = MCSchematic((dim, box.size[1], dim))
    buf.copyBlocksFrom(level, box, (0,0,0))
    buf.rotateLeft()
    if step[0] == step[2]:
        buf.flipNorthSouth()
    else:
        buf.flipEastWest()

    start = (0 if step[0] < 0 else dim - 1,
             0,
             0 if step[2] < 0 else dim - 1)
    stop =  (0 if step[0] > 0 else dim - 1,
             0,
             0 if step[2] > 0 else dim - 1)

    z = 1
    for x in xrange(start[0], stop[0], -step[0]):
        if step[2] < 0:
            level.copyBlocksFrom(buf,
                                 BoundingBox(origin=(x, 0, 0),
                                             size=(1, box.size[1], dim - z)),
                                 box.origin + (x, 0, 0))
        else:
            level.copyBlocksFrom(buf,
                                 BoundingBox(origin=(x, 0, z),
                                             size=(1, box.size[1], dim - z)),
                                 box.origin + (x, 0, z))
        z += 1

    level.markDirtyBox(box)
