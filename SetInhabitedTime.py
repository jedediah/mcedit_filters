# Coded by last_username

from pymclevel import nbt

displayName = "Set Chunk Inhabited Time"

inputs = (
    ("Age in ticks", 0),
)

def perform(level, box, options):
    age = options[inputs[0][0]]
    worldTime = level.root_tag["Data"]["Time"].value

    for (chunk, _, _) in level.getChunkSlices(box):
        chunkLevel = chunk.root_tag["Level"]

        if "InhabitedTime" in chunkLevel:
            if chunkLevel["InhabitedTime"].value != age:
                chunkLevel["InhabitedTime"].value = age
                chunk.dirty = True
        else:
            chunkLevel["InhabitedTime"] = nbt.TAG_Long(age)
            chunk.dirty = True

        if "LastUpdate" in chunkLevel:
            if chunkLevel["LastUpdate"].value != worldTime:
                chunkLevel["LastUpdate"].value = worldTime
                chunk.dirty = True
        else:
            chunkLevel["LastUpdate"] = nbt.TAG_Long(worldTime)
            chunk.dirty = True