
from pymclevel import MCSchematic

inputs = (
    ("Leave Only", "blocktype"),
)


def perform(level, box, options):
    leaveBlock = options["Leave Only"]
    buf = MCSchematic(shape=box.size, mats=level.materials)
    buf.copyBlocksFrom(level, box, (0,0,0), [leaveBlock.ID])
    level.copyBlocksFrom(buf, buf.bounds, box.origin)
    level.markDirtyBox(box)
