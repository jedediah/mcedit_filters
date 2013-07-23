
# Coded by last_username

import re
from pymclevel.nbt import TAG_String

displayName = "Translate Command Block Coordinates"

inputs = (
    ("Delta X", 0),
    ("Delta Y", 0),
    ("Delta Z", 0),
    ("Debug", False),
)

def translateTeleportCoord(coord, delta):
    if coord[0] == '~':
        return coord
    if '.' in coord:
        return str(float(coord) + delta)
    else:
        return str(int(coord) + delta)


def perform(level, box, options):
    delta = (options["Delta X"], options["Delta Y"], options["Delta Z"])

    def debug(msg):
        if options["Debug"]:
            print msg

    for (chunk, _, _) in level.getChunkSlices(box):
        for tile in chunk.TileEntities:
            pos = (tile["x"].value, tile["y"].value, tile["z"].value)

            if pos in box and tile["id"].value == "Control":
                command = tile["Command"].value
                originalCommand = command

                if not command:
                    continue

                try:
                    def translateSelector(match):
                        index = 0
                        prefix = match.group(1)
                        args = re.split(r'\s*,\s*', match.group(2))

                        for i in xrange(len(args)):
                            m = re.match(r'(?:(x|y|z)=)?(-?\d+)', args[i])
                            if m:
                                coord, value = m.groups()
                                value = int(value)
                                if coord:
                                    args[i] = "{0}={1}".format(coord, value + delta[('x','y','z').index(coord)])
                                    debug("Translating explicit coord {0}={1}".format(coord, value))
                                elif i < 3:
                                    args[i] = str(value + delta[index])
                                    debug("Translating implicit coord {0}={1}".format(('x','y','z')[index], value))
                                    index += 1

                        return "@{0}[{1}]".format(prefix, ",".join(args))

                    command = re.sub(r'(?:^|(?<=\s))@([pra])\[([^\]]*)\](?:(?=\s)|$)', translateSelector, command)

                    words = re.split(r'\s+', command)
                    first = re.sub(r'^/', '', words[0])

                    def translate(offset):
                        debug("Translating /{0} coords: {1}".format(first, " ".join(words[offset:offset+3])))

                        for axis in xrange(3):
                            coord = words[offset+axis]
                            if coord[0] != '~':
                                if '.' in coord:
                                    coord = str(float(coord) + delta[axis])
                                else:
                                    coord = str(int(coord) + delta[axis])
                            words[offset+axis] = coord

                    if first == 'tp' and len(words) == 5:
                        translate(2)
                    elif first == 'spawnpoint' and len(words) == 5:
                        translate(2)
                    elif first == 'playsound' and len(words) >= 6:
                        translate(3)

                    command = " ".join(words)
                    if command != originalCommand:
                        tile["Command"] = TAG_String(command)
                        chunk.dirty = True
                except Exception as ex:
                    print "Failed to translate the command block at {0} with the following command:\n{1}\n".format(pos, originalCommand)
                    raise

