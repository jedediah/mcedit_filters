
import itertools

from pymclevel import MCSchematic
from pymclevel.materials import Block
from pymclevel.box import BoundingBox, Vector

materials = (
    "Cobblestone",
    "Sandstone",
    "Brick",
    "Stone Brick",
    "Nether Brick",
    "Quartz",
)
    
fullBlockID = (4, 24, 45, 98, 112, 155)
stairBlockID = (67, 128, 108, 109, 114, 156)
slabBlockData = (3, 1, 4, 5, 6, 7)

slabBlockID = 44
doubleSlabBlockID = 43

inputs = (
    ("Replace", materials),
    ("With", materials),
)

def perform(level, box, options):
    fromIndex = materials.index(options["Replace"])
    toIndex = materials.index(options["With"])

    blockCount = 0
    stairCount = 0
    slabCount = 0

    for chunk, slices, point in level.getChunkSlices(box):
        Blocks = chunk.Blocks[slices]
        Data = chunk.Data[slices]

        for p in itertools.product(xrange(slices[0].start, slices[0].stop),
                                   xrange(slices[1].start, slices[1].stop),
                                   xrange(slices[2].start, slices[2].stop)):
            if Blocks[p] == fullBlockID[fromIndex]:
                Blocks[p] = fullBlockID[toIndex]
                blockCount += 1
            elif Blocks[p] == stairBlockID[fromIndex]:
                Blocks[p] = stairBlockID[toIndex]
                stairCount += 1
            elif Blocks[p] == slabBlockID or Blocks[p] == doubleSlabBlockID:
                if (Data[p] & 0x7) == slabBlockData[fromIndex]:
                    Data[p] = (Data[p] & 0x8) | slabBlockData[toIndex]
                    slabCount += 1
                    
    level.markDirtyBox(box)

    print "Converted {0} full blocks, {1} stairs, and {2} slabs/double slabs".format(
        blockCount, stairCount, slabCount)
