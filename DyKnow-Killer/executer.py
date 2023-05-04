import os, sys
import signal

protectedProcesses = [] # Add some protected processes

def getDyKnowExes():
    allCrucial = []
    for folderName, folders, files in os.walk(r'C:\Program Files\DyKnow'):
      for item in files:
        if item.endswith('.exe'):
          allCrucial.append(item)
    return allCrucial


def killProcess(name):
  try:
    os.kill(name, signal.SIGTERM)
    return 0
  except Exception as e:
    print(f'ERROR: An unknown error was encountered. \n{e}\n')
    return 1


def get_PID(process):
  try:
    retlist = []
    output = os.popen(f'powershell ps -Name {process}').read()
    for line in output.splitlines():
      if '.' in line:
        index = line.find(f'  1 ')
        diffrence = line[0:index]
        list = diffrence.split('  ')
        retlist.append(list[-1].replace(' ', ''))
    return retlist
  except Exception as e:
    print(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)


def nameFinder(PID):
  index = PID.find('.exe')
  output = os.popen(f'tasklist /svc /FI "PID eq {PID[0:index]}"').read()
  for line in str(output).splitlines():
    if '.exe' in line:
      index = line.find('.exe')
      diffrence = line[0:index]
      retvalue = f'{diffrence}.exe'
  return retvalue


def getProcesses():
  try:
    retlist = []
    output = os.popen('wmic process get description, processid').read()
    for line in output.splitlines():
      if '.exe' in line:
        index = line.find('.exe')
        itemobj = line[index + 5:].replace(' ', '')
        retlist.append(itemobj)
      else:
        output = output.replace(line, '')
    return retlist
  except Exception as e:
    print(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)


if __name__ == '__main__':
  while True:
    blacklisted = []
    processes = getProcesses()
    blacklisted.extend(getDyKnowExes())
    for file in blacklisted:
      if file in processes and not protectedProcesses:
        name = file.replace('.exe', '')
        PID = get_PID(name)
      else:
        pass
        # If not running delete file