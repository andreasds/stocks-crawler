def readUserConfig(configPath):
  configKey = [ 'poemsUser', 'poemsPassword', 'poemsPin' ]
  userConfig = {}

  with open(configPath) as f:
    allConfig = f.readlines()
    for config in allConfig:
      dictConfig = config.strip().split('=')
      if len(dictConfig) != 2:
        raise ValueError('Invalid user config file')

      if dictConfig[0].strip() not in configKey:
        continue

      userConfig[dictConfig[0].strip()] = dictConfig[1].strip()

  return userConfig
