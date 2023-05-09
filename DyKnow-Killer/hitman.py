# TODO: Test driver.addProtected() then print protectedProcesses.
# TODO: Review initlization code and reformat

import os, sys
import socket
import signal
import time

clear = lambda: os.system('cls')
protectedProcesses = [
  'chrome.exe', 'spotify.exe', 'code.exe', 'steam.exe', 'RuntimeBroker.exe',
  'svchost.exe', 'ntoskrnl.exe', 'winlogon.exe', 'wininit.exe', 'csrss.exe',
  'smss.exe', 'explorer.exe', 'qbittorent.exe', 'cmd.exe', 'Terminal.exe'
]


class utility:

  def processPath(process):
    if process.endswith('.exe'):
      process = process[:-4]
    try:
      out = os.popen(f'powershell (Get-Process {process}).Path').read()
      for line in out.splitlines():
        if os.path.exists(line):
          return line
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

  def getProcesses():
    try:
      iterated = set()
      retlist = []
      output = os.popen('wmic process get description, processid').read()
      print('Please wait this may take a moment...')

      for line in output.splitlines():
        if '.exe' in line:
          index = line.find('.exe')
          item = line[index + 5:].replace(' ', '')
          itemobj = utility.nameFinder(item)
          if itemobj and itemobj not in iterated:
            retlist.append(itemobj)
            iterated.add(itemobj)

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

  def getPID(process):
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


class sd:

  def killProcess(name):
    if name.endswith('.exe'):
      name = name.replace('.exe', '')
    PIDlist = utility.getPID(name)
    for PID in PIDlist:
      try:
        os.kill(int(PID), signal.SIGTERM)
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)

  def getDyKnowProcesses():
    allCrucial = []
    for r, d, f in os.walk('C:/Program Files/DyKnow'):
      for file in f:
        if file.endswith('.exe'):
          allCrucial.append(file)
    return allCrucial

  def findDyKnowExe(target_exe):
    base_dir = 'C:/Program Files/DyKnow/'
    for r, d, f in os.walk(base_dir):
      for file in f:
        if target_exe in file:
          item = f'{r}/{file}'.replace(base_dir, '')
          if item.find('/') == 0:
            item = item.replace('/', '')
            return item

  def removeRunning(process):
    proc_path = utility.processPath(process)
    if not process.endswith('.exe'):
      process = f'{process}.exe'
    else:
      try:
        try:
          sd.killProcess(process)
        except:
          pass
        time.sleep(0.5)
        os.remove(proc_path)
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)


class driver:

  def addProtected():
    file = f'{os.getcwd()}/protect.txt'
    if not os.path.exists(file):
      print(f'No {file} library found, skipping.')
    else:
      with open(file, 'r') as protected_lib:
        content = protected_lib.read()
        for line in content.splitlines():
          protectedProcesses.append(line).replace('\n', '')

  def errorHandler(error_code):
    if error_code == '1':
      print('The execution operation already removed crucial files.')
      time.sleep(5)
      sys.exit(0)
    if error_code == '2':
      print('DyKnow files cannot be found, is it installed?')
      time.sleep(5)
      sys.exit(1)
    else:
      clear()
      print('Invaild input, quitting.')
      time.sleep(5)
      sys.exit(1)


# Initialization code (Cover your eyes)
if __name__ == '__main__':
  clear()
  print("   ----- Windows DyKnow Executor ----- \
    \nThis program will delete crucial DyKnow files to \
    \nrender DyKnow unable to run properly. Once ran \
    \nyou will be unable to reinstall DyKnow unless you \
    \npull some crafty shit like recovering the files. \n")
  input("Press 'Enter' to start \n")
  clear()

  try:
    driver.addProtected()
    processes = utility.getProcesses()
    blacklisted = []
    blacklisted.extend(sd.getDyKnowProcesses())
    if len(blacklisted) == 0:
      clear()
      print("The process cant locate DyKnow's files, This program might have already been ran if so please type 1 if not type 2.")
      q_a = input('> ')
      driver.errorHandler(q_a)
    for file in blacklisted:
      if file in processes:
        if file not in protectedProcesses:
          print(f'File {file} is running as process')
          sd.removeRunning(file)
          print(f'Killed/deleted running process {file}.')
          del_file = sd.findDyKnowExe(file)
          os.remove(f'C:/Program Files/DyKnow/{del_file}')
          print(f'Executor deleted file {del_file}.')
      else:
        del_file = sd.findDyKnowExe(file)
        os.remove(f'C:/Program Files/DyKnow/{del_file}')
        print(f'Executor deleted file {del_file}.')

    print(f'\nDetected files have been removed from {socket.gethostname()}.')
    input("Press 'Enter' to quit.")
    sys.exit(0)

  except PermissionError:
    print('ERROR: Action executed without required permissions, try \
      \nclosing DyKnow or running the program as an administrator.')
    time.sleep(5)
    sys.exit(1)
  except Exception as e:
    print(f'ERROR: An unknown error was encountered. \n{e}\n')
    time.sleep(5)
    sys.exit(1)

else:
  print(f'ERROR: You cannot import {__file__}.')
  sys.exit(1)
