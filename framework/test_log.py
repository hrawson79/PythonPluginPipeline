from logger import Log, Logger

log = Log(1)
print('------------ level 1 ------------')

log.LogMsg(Logger.ERROR, 'Hello error')
log.LogMsg(Logger.WARNING, 'Hello warning')
log.LogMsg(Logger.INFO, 'Hello info')
log.LogMsg(Logger.DEBUG, 'Hello debug')
log.LogMsg(Logger.TRACE, 'Hello trace')

log.setLevel(2)
print('------------ level 2 ------------')

log.LogMsg(Logger.ERROR, 'Hello error')
log.LogMsg(Logger.WARNING, 'Hello warning')
log.LogMsg(Logger.INFO, 'Hello info')
log.LogMsg(Logger.DEBUG, 'Hello debug')
log.LogMsg(Logger.TRACE, 'Hello trace')

log.setLevel(3)
print('------------ level 3 ------------')

log.LogMsg(Logger.ERROR, 'Hello error')
log.LogMsg(Logger.WARNING, 'Hello warning')
log.LogMsg(Logger.INFO, 'Hello info')
log.LogMsg(Logger.DEBUG, 'Hello debug')
log.LogMsg(Logger.TRACE, 'Hello trace')

log.setLevel(4)
print('------------ level 4 ------------')

log.LogMsg(Logger.ERROR, 'Hello error')
log.LogMsg(Logger.WARNING, 'Hello warning')
log.LogMsg(Logger.INFO, 'Hello info')
log.LogMsg(Logger.DEBUG, 'Hello debug')
log.LogMsg(Logger.TRACE, 'Hello trace')

log.setLevel(5)
print('------------ level 5 ------------')

log.LogMsg(Logger.ERROR, 'Hello error')
log.LogMsg(Logger.WARNING, 'Hello warning')
log.LogMsg(Logger.INFO, 'Hello info')
log.LogMsg(Logger.DEBUG, 'Hello debug')
log.LogMsg(Logger.TRACE, 'Hello trace')