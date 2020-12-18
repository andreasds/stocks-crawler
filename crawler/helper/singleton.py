class Singleton(type):
  _instances = {}

  # Singleton class using metaclass will invoke __call__ at first
  def __call__ (cls, *args, **kwargs):
    if cls not in cls._instances:
      # this type.__call__ will call class.__new__ and class.__init__
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    #else:
    #  # if we need to re-initiate our class every time class is called
    #  cls._instances[cls].__init__(*args, **kwargs)

    return cls._instances[cls]
