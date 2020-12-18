def readUserConfig(configPath):
  configKey = [ 'user', 'password', 'pin' ]
  userConfig = {}

  with open(configPath) as f:
    allConfig = f.readlines()
    for config in allConfig:
      dictConfig = config.strip().split('=')
      if len(dictConfig) != 2 or \
          dictConfig[0].strip() not in configKey:
        raise ValueError('Invalid user config file')

      userConfig[dictConfig[0].strip()] = dictConfig[1].strip()

  return userConfig
