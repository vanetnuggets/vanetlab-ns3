class LogHelper:

  # everything ok, just for information
  def log(self, msg, *argv):
    print(f'[debug] {msg}', *argv)
  
  # fatal, cannot simulate, should probably call exit()
  def err(self, msg, *argv):
    print(f'[error] {msg}', *argv)
  
  # something weird, not fatal but should be noted
  def warn(self, msg, *argv):
    print(f'[warn] {msg}', *argv)

dbg = LogHelper()
