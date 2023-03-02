class LogHelper:
  def log(self, msg):
    print(f'[debug] {msg}')
  
  def err(self, msg):
    print(f'[error] {msg}')

dbg = LogHelper()