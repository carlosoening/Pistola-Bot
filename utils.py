from typing import Dict

def check_key(dict: Dict[str, str], key) -> bool:
  """
  Verifies if key is in the given dictionary
  """
  if key in dict:
    return True
  return False

def sanitize_command(command: str) -> str:
  """
  Sanitize and prepare command to the right pattern
  """
  command = command.strip()
  if (command.startswith('$') == False):
    command = '$' + command
  return command