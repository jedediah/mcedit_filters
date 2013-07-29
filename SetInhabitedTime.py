# Coded by last_username

from pymclevel import nbt

displayName = "Set Chunk Inhabited Time"

inputs = (
    ("Age in ticks", 0),
)

def perform(level, box, options):
    age = options[inputs[0][0]]
    for (chunk, _, _) in level.getChunkSlices(box):
        if "InhabitedTime" in chunk.root_tag["Level"]:
            if chunk.root_tag["Level"]["InhabitedTime"].value != age:
                chunk.root_tag["Level"]["InhabitedTime"].value = age
                chunk.dirty = True
        else:
            chunk.root_tag["Level"]["InhabitedTime"] = nbt.TAG_Long(age)
            chunk.dirty = True