import platform


def determin_sys():
  sysinfo = platform.system()
  sysinfo = sysinfo.upper()
  if sysinfo.find("WINDOWS") >= 0:
    str = "win"
  elif sysinfo.find("LINUX") >= 0:
    str = "linux"
  elif sysinfo.find("CYGWIN") >= 0:
    str = "cygwin"
  else:
    str = "unknown"

  return str
