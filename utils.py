def checkKey(dict, key):
  if key in dict:
    return True
  return False

def sanitizeCommand(command):
  if (command.startswith('$') == False):
    command = '$' + command
  return command