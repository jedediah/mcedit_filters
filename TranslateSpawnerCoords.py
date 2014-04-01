
displayName = "Translate Spawner Coordinates"

inputs = (
    ("Delta X", 0),
    ("Delta Y", 0),
    ("Delta Z", 0),
    ("Debug", False),
)

def entityPos(entity):
    return entity['Pos'][0].value, entity['Pos'][1].value, entity['Pos'][2].value

def tileEntityPos(tileEntity):
    return tileEntity['x'].value, tileEntity['y'].value, tileEntity['z'].value

def translateEntity(entityId, entityData, delta, debug=False):
    """
    Translate any spawner data contained in the given entity
    """
    changed = False

    if entityId == 'MinecartSpawner':
        changed = translateSpawner(entityData, delta, debug) or changed
    elif (entityId == 'FallingSand' and
          (('Tile' in entityData and entityData['Tile'].value == 52) or
           ('TileID' in entityData and entityData['TileID'].value == 52)) and
          'TileEntityData' in entityData):
        changed = translateSpawner(entityData['TileEntityData'], delta, debug) or changed

    if 'Riding' in entityData:
        changed = translateEntity(entityData['Riding']['id'].value,
                                  entityData['Riding'],
                                  delta,
                                  debug) or changed

    return changed

def translateSpawnedEntity(entityId, entityData, delta, debug=False):
    """
    Translate the given entity and any spawner data it contains
    """
    changed = False

    if 'Pos' in entityData:
        for i in xrange(3):
            entityData['Pos'][i].value += delta[i]
        changed = True
        if debug:
            print "  Translated {0} to {1}".format(entityId, entityPos(entityData))

    if 'Riding' in entityData:
        changed = translateSpawnedEntity(entityData['Riding']['id'].value,
                                         entityData['Riding'],
                                         delta,
                                         debug) or changed

    return translateEntity(entityId, entityData, delta, debug) or changed

def translateSpawner(spawner, delta, debug=False):
    """
    Translate spawner data
    """
    changed = False
    if 'EntityId' in spawner and 'SpawnData' in spawner:
        changed = translateSpawnedEntity(spawner['EntityId'].value,
                                         spawner['SpawnData'],
                                         delta,
                                         debug) or changed
    if 'SpawnPotentials' in spawner:
        for potential in spawner['SpawnPotentials']:
            if 'Type' in potential and 'Properties' in potential:
                changed = translateSpawnedEntity(potential['Type'].value,
                                                 potential['Properties'],
                                                 delta,
                                                 debug) or changed
    return changed

def translateChunk(chunk, bounds, delta, debug=False):
    """
    Translate any spawner data contained in the given chunk
    """
    for tileEntity in chunk.TileEntities:
        pos = tileEntityPos(tileEntity)
        if pos in bounds and tileEntity['id'].value == 'MobSpawner':
            if translateSpawner(tileEntity, delta, debug):
                chunk.dirty = True
    for entity in chunk.Entities:
        if entityPos(entity) in bounds:
            if translateEntity(entity['id'].value, entity, delta, debug):
                chunk.dirty = True

def perform(level, box, options):
    delta = (options['Delta X'], options['Delta Y'], options['Delta Z'])
    debug = options['Debug']

    for chunk, _, _ in level.getChunkSlices(box):
        translateChunk(chunk, box, delta, debug)

