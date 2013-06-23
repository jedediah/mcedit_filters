
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
    debug = options["Debug"]

    for (chunk, _, _) in level.getChunkSlices(box):
        for tile in chunk.TileEntities:
            pos = (tile["x"].value, tile["y"].value, tile["z"].value)

            if pos in box and tile["id"].value == "Control":
                command = tile["Command"].value
                originalCommand = command

                if not command:
                    continue

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
                                if debug:
                                    print "Translating explicit coord {0}={1}".format(coord, value)
                            else:
                                args[i] = str(value + delta[index])
                                if debug:
                                    print "Translating implicit coord {0}={1}".format(('x','y','z')[index], value)
                                index += 1

                    return "@{0}[{1}]".format(prefix, ",".join(args))

                command = re.sub(r'(?:^|(?<=\s))@([pra])\[([^\]]*)\](?:(?=\s)|$)', translateSelector, command)

                if re.match(r'^\s*/?(?:tp|spawnpoint)', command):
                    words = re.split(r'\s+', command)
                    if len(words) == 5:
                        if debug:
                            print "Translating spawnpoint/tp coords: {0}".format(" ".join(words[2:5]))
                        for i in xrange(3):
                            words[2+i] = translateTeleportCoord(words[2+i], delta[i])
                        command = " ".join(words)

                if command != originalCommand:
                    tile["Command"] = TAG_String(command)
                    chunk.dirty = True

