import itertools

inputs = (
  ("Fill with", "blocktype"),
)


def perform(level, box, options):
    blocktype = options["Fill with"]

    for chunk, slices, point in level.getChunkSlices(box):
        blocks = chunk.Blocks[slices]
        data = chunk.Data[slices]

        for x, z in itertools.product(xrange(blocks.shape[0]), xrange(blocks.shape[1])):
            height = None
            for y in xrange(blocks.shape[2]):
                block = blocks[x,z,y]
                if block in (17, 18): # log, leaves
                    break
                elif block != 0:
                    height = y
                    break

            if height:
                blocks[x,z,:height] = blocktype.ID
                data[x,z,:height] = blocktype.blockData
                #for y in xrange(height):
                #    blocks[x,z,y] = blocktype.ID
                #    data[x,z,y] = blocktype.blockData
        chunk.chunkChanged()
