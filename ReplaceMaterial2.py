
import itertools
from numpy import zeros
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

    level.fillBlocks(box,
                     level.materials.blockWithID(fullBlockID[toIndex]),
                     [level.materials.blockWithID(fullBlockID[fromIndex])])

    level.fillBlocks(box,
                     level.materials.blockWithID(stairBlockID[toIndex]),
                     [level.materials.blockWithID(stairBlockID[fromIndex])])

    level.fillBlocks(box,
                     Block(level.materials, slabBlockID, blockData=slabBlockData[toIndex]),
                     [Block(level.materials, slabBlockID, blockData=slabBlockData[fromIndex])])

    for blockID in [slabBlockID, doubleSlabBlockID]:
        for dataOffset in [0, 8]:
            fromBlockTable = zeros((256, 16), dtype='bool')
            fromBlockTable[blockID, dataOffset + slabBlockData[fromIndex]] = True

            for chunk, slices, point in level.getChunkSlices(box):
                Blocks = chunk.Blocks[slices]
                Data = chunk.Data[slices]
                mask = fromBlockTable[Blocks, Data]
                Data[mask] = dataOffset + slabBlockData[toIndex]

    level.markDirtyBox(box)

    print "Converted {0} full blocks, {1} stairs, and {2} slabs/double slabs".format(
        blockCount, stairCount, slabCount)
