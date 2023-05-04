# TODO: Test on mock folder and create a .exe to put in there

import os, sys
import signal

clear = lambda: os.system('clear')
protectedProcesses = [
  'chrome.exe', 'spotify.exe', 'code.exe', 'steam.exe', 'RuntimeBroker.exe',
  'svchost.exe', 'ntoskrnl.exe', 'winlogon.exe', 'wininit.exe', 'csrss.exe',
  'smss.exe', 'explorer.exe'
]


class sd:

  def getDyKnowProcesses():
    allCrucial = []
    for folderName, folders, files in os.walk('C:/Program Files/DyKnow'):
      for item in files:
        if item.endswith('.exe'):
          allCrucial.append(item)
    return allCrucial

  def findDyKnowExe(target_exe):
    allCrucial = []
    base_dir = 'C:/Program Files/DyKnow/'
    for r, d, f in os.walk(base_dir):
      for file in f:
        if target_exe in file:
          item = f'{r}/{file}'.replace(base_dir, '')
          if item.find('/') == 0:
            item = item.replace('/', '')
          allCrucial.append(item)
    return allCrucial

  def killProcess(PID):
    try:
      os.kill(PID, signal.SIGTERM)
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
          index = line.find('  1 ')
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
          retlist.append(sd.nameFinder(itemobj))
        else:
          output = output.replace(line, '')
      return retlist
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)


class driver:

  def addProtected():
    file = 'protect.txt'
    if not os.path.exists(file):
      print(f'No {file} library found, skipping.')
    else:
      with open(file, 'r') as protected_lib:
        content = protected_lib.read()
        for line in content.splitlines():
          protectedProcesses.append(line)

  def errorHandler(error_code):
    if error_code == '1':
      print('The execution operation already removed crucial files.')
      sys.exit(0)
    if error_code == '2':
      print('DyKnow files cannot be found, is it installed?')
      sys.exit(1)
    else:
      clear()
      print('Invaild input, quitting.')
      sys.exit(1)


# Initialization code
if __name__ == '__main__':
  clear()
  print("      ----- Windows DyKnow Executor ----- \
    \nThis program will delete crucial DyKnow files to \
    \nrender DyKnow unable to run properly. Once ran \
    \nyou will be unable to reinstall DyKnow unless you \
    \npull some crafty shit like recovering the files. \n")
  input("Press 'Enter' to start \n")
  clear()

  try:
    driver.addProtected()
    processes = sd.getProcesses()
    blacklisted = []
    blacklisted.extend(sd.getDyKnowProcesses())
    if len(blacklisted) == 0:
      clear()
      print("The process cant locate DyKnow's files, This program might have already been ran if so please type 1 if not type 2.")
      q_a = input('> ')
      driver.errorHandler(q_a)

    for file in blacklisted:
      if file in processes and not protectedProcesses:
        print(f'File {file} is running as process')
        name = file.replace('.exe', '')
        PID = sd.get_PID(name)
        sd.killProcess(PID)
        print(f'Killed running process {name}.')
        for item in sd.findDyKnowExe(file):
          os.remove(f'C:/Program Files/DyKnow/{item}')
          print(f'Executor deleted file {item}.')

      else:
        for item in sd.findDyKnowExe(file):
          os.remove(f'C:/Program Files/DyKnow/{item}')
          print(f'Executor deleted file {item}.')

    print(f'\nDetected files have been removed from {os.uname()[1]}.')
    input("Press 'Enter' to quit.")
    sys.exit(1)

  except Exception as e:
    print(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)

else:
  print(f'ERROR: You cannot import {__file__}.')
  sys.exit(1)
