def __readConfig(configPath, configName, configKey):
  filterConfig = {}

  with open(configPath) as f:
    allConfig = f.readlines()
    for config in allConfig:
      if config.strip().startswith('#') or \
          config.strip() == '':
        continue

      dictConfig = config.strip().split('=')
      if len(dictConfig) != 2:
        raise ValueError('Invalid ' + configName + ' config file')

      if dictConfig[0].strip() not in configKey:
        continue

      filterConfig[dictConfig[0].strip()] = dictConfig[1].strip()

  return filterConfig

def readUserConfig(configPath):
  userKey = [ 'poemsUser', 'poemsPassword', 'poemsPin' ]
  userConfig = __readConfig(configPath, 'user', userKey)

  for key in userKey:
    if key not in userConfig:
      raise RuntimeError('Invalid user config file')

  return userConfig

def readDbConfig(configPath):
  dbKey = [ 'dbHost', 'dbPort', 'dbUser', 'dbPassword' ]
  dbConfig = __readConfig(configPath, 'db', dbKey)

  for key in dbKey:
    if key not in dbConfig:
      raise RuntimeError('Invalid db config file')

  return dbConfig
