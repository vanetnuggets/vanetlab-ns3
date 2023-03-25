class LogHelper:

  # everything ok, just for information
  def log(self, msg):
    print(f'[debug] {msg}')
  
  # fatal, cannot simulate, should probably call exit()
  def err(self, msg):
    print(f'[error] {msg}')
  
  # error, but not fatal, just ignoring the failed part
  def warn(self, msg):
    print(f'[ignore] {msg}')

dbg = LogHelper()