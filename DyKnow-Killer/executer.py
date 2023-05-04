# Add more user prints to the code before compiling due to long tasks

import os, sys
import signal

protectedProcesses = ['chrome', 'spotify', 'code', 'steam', 'RuntimeBroker.exe', 'svchost.exe'] # Processes that will be ignored by kill

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
  output = os.popen(f'tasklist /svc /FI "PID eq {PID}"').read()
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
    print('Please wait this may take a moment...')
    for line in output.splitlines():
      if '.exe' in line:
        index = line.find('.exe')
        itemobj = line[index + 5:].replace(' ', '')
        retlist.append(nameFinder(itemobj))
      else:
        output = output.replace(line, '')
    return retlist
  except Exception as e:
    print(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)

if __name__ == '__main__':
  blacklisted = []
  processes = getProcesses()
  blacklisted.extend(getDyKnowExes())
  for file in blacklisted:
    if file in processes and not protectedProcesses:
      name = file.replace('.exe', '')
      PID = get_PID(name)
      # Then kill the process and delete the file!
    else:
      os.remove(f'C:/Program Files/DyKnow/{file}') # If file is not found delete its assumed location