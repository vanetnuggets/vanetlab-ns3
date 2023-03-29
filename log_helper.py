class LogHelper:

  # everything ok, just for information
  def log(self, msg, *argv):
    print(f'[debug] {msg}', *argv)
  
  # fatal, cannot simulate, should probably call exit()
  def err(self, msg, *argv):
    print(f'[error] {msg}', *argv)
  
  # error, but not fatal, just ignoring the failed part
  def warn(self, msg, *argv):
    print(f'[ignore] {msg}', *argv)

dbg = LogHelper()