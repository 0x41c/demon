class Logger(object):

  name = "Demon"
  custom_name = ""

  def log(self, message):
    """
    Logs a message using a default name
    """
    print('[%s -> %s] %s' % (self.name, self.custom_name, message))
  
  def warn(self, message):
    """
    Logs a message and appends a warning attribute
    """
    self.log('[WARN] %s' % message)

  def error(self, message):
    """
    Logs a message and appends an error attribute
    """
    self.log('[Error] %s' % message)
