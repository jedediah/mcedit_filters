
import numpy
from pymclevel import MCSchematic

inputs = (
    ("Fill", "blocktype"),
    ("With", "blocktype"),
    ("Boundary thickness", 1)
)

def perform(level, box, options):
    fillBlock = options["Fill"]
    withBlock = options["With"]
    borderThickness = options["Boundary thickness"]

    orig = MCSchematic(shape=box.size, mats=level.materials)
    orig.copyBlocksFrom(level, box, (0,0,0))
    orig.removeEntitiesInBox(orig.bounds)
    orig.removeTileEntitiesInBox(orig.bounds)

    a = orig.Blocks[:] != fillBlock.ID
    b = numpy.copy(a)

    for n in xrange(borderThickness):
        b[:] = a[:]
        b[ 1:  ,  :  ,  :  ] |= a[  :-1,  :  ,  :  ]
        b[  :-1,  :  ,  :  ] |= a[ 1:  ,  :  ,  :  ]
        b[  :  , 1:  ,  :  ] |= a[  :  ,  :-1,  :  ]
        b[  :  ,  :-1,  :  ] |= a[  :  , 1:  ,  :  ]
        b[  :  ,  :  , 1:  ] |= a[  :  ,  :  ,  :-1]
        b[  :  ,  :  ,  :-1] |= a[  :  ,  :  , 1:  ]
        a, b = b, a

    orig.Blocks[~a] = withBlock.ID
    level.copyBlocksFrom(orig, orig.bounds, box.origin, [withBlock.ID])
    level.markDirtyBox(box)
    
