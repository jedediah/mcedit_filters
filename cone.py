
inputs = (
    ("Material", "blocktype"),
    ("Top radius", (0.0,1.0)),
    ("Exponent", (1.0,0.01,100.0)),
    ("Include air", False)
)


def perform(level, box, options):
    material = options["Material"]
    topRadius = options["Top radius"]
    exponent = options["Exponent"]
    includeAir = options["Include air"]

    for y in xrange(box.miny, box.maxy):
      r = 1.0 - (float(y) - box.miny) / (box.height - 1)
      #r = topRadius + (1.0 - fy ** exponent) * (1.0 - topRadius)
      r = topRadius + r**exponent * (1.0 - topRadius)

      for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
          fx = (float(x) + 0.5 - box.minx) / box.width * 2.0 - 1.0
          fz = (float(z) + 0.5 - box.minz) / box.length * 2.0 - 1.0

          if fx*fx + fz*fz <= r*r:
            level.setBlockAt(x,y,z,material.ID)
            level.setBlockDataAt(x,y,z,material.blockData)
          elif includeAir:
            level.setBlockAt(x,y,z,0)
    
    level.markDirtyBox(box)
