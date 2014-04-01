
from pymclevel import alphaMaterials

TileEntityIds = {
  "Furnace":      [alphaMaterials.Furnace.ID],
  "Sign":         [alphaMaterials.Sign.ID, alphaMaterials.WallSign.ID],
  "MobSpawner":   [alphaMaterials.MonsterSpawner.ID],
  "Chest":        [alphaMaterials.Chest.ID],
  "Music":        [alphaMaterials.NoteBlock.ID],
  "Trap":         [alphaMaterials.Dispenser.ID],
  "RecordPlayer": [alphaMaterials.Jukebox.ID],
  "Cauldron":     [117],
  "Skull":        [144],
  "Beacon":       [138],
  "EnchantTable": [116]
}

def perform(level, box, options):
  for (chunk, slices, point) in level.getChunkSlices(box):
    for te in chunk.getTileEntitiesInBox(box):
      pos = (te["x"].value, te["y"].value, te["z"].value)
      entityId = te["id"].value
      if entityId in TileEntityIds.keys():
        expectedBlockIds = [e for e in TileEntityIds[entityId]]
        actualBlockId = level.blockAt(*pos)
        if actualBlockId not in expectedBlockIds:
          chunk.TileEntities.remove(te)

  level.markDirtyBox(box)
