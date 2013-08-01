
from pymclevel import MCSchematic
from pymclevel.box import BoundingBox, Vector

inputs = (
    ("Fill", "blocktype"),
    ("With", "blocktype"),
    ("Boundary thickness", 1)
)


def vabs(v):
    return Vector(*(abs(a) for a in v))

def copyClipped(dest, src, offset, mask):
    offset = Vector(*(BoundingBox.type(a) for a in offset))
    bounds = BoundingBox(src.bounds.origin, Vector(*src.bounds.size) - vabs(offset))
    print "perturbing {0} by {1} to {2} bounds={3}".format(src, offset, dest, bounds)
    dest.copyBlocksFrom(src, bounds, offset, mask)

def perform(level, box, options):
    fillBlock = options["Fill"]
    withBlock = options["With"]
    borderThickness = options["Boundary thickness"]

    notFillBlock = [i for i in range(4096) if i != fillBlock.ID]

    orig = MCSchematic(shape=box.size, mats=level.materials)
    orig.copyBlocksFrom(level, box, (0,0,0))
    orig.removeEntitiesInBox(orig.bounds)
    orig.removeTileEntitiesInBox(orig.bounds)

    perturbed = MCSchematic(shape=box.size, mats=level.materials)
    perturbed.copyBlocksFrom(orig, orig.bounds, (0,0,0))

    for n in xrange(0, borderThickness):
        copyClipped(perturbed, orig, ( 0, 0, 0), notFillBlock)
        copyClipped(perturbed, orig, ( 1, 0, 0), notFillBlock)
        copyClipped(perturbed, orig, (-1, 0, 0), notFillBlock)
        copyClipped(perturbed, orig, ( 0, 1, 0), notFillBlock)
        copyClipped(perturbed, orig, ( 0,-1, 0), notFillBlock)
        copyClipped(perturbed, orig, ( 0, 0, 1), notFillBlock)
        copyClipped(perturbed, orig, ( 0, 0,-1), notFillBlock)

        orig, perturbed = perturbed, orig

    orig.Blocks[orig.Blocks != fillBlock.ID] = 1 if withBlock.ID == 0 else 0
    orig.Blocks[orig.Blocks == fillBlock.ID] = withBlock.ID

    level.copyBlocksFrom(orig, orig.bounds, box.origin, [withBlock.ID])
    # level.copyBlocksFrom(orig, orig.bounds, box.origin, [i for i in range(4096)])

    level.markDirtyBox(box)
    
