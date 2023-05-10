# NOTE: To properly run this file you must compile it to .exe (Due to elevation)
# NOTE: If you want to run this program please run it as admin it will 
# attempt a self elevate though this is not guaranteed to work.

import os, sys
import socket
import ctypes
import signal
import time

clear = lambda: os.system('cls')
protectedProcesses = [
  'chrome.exe', 'spotify.exe', 'code.exe', 'steam.exe', 'RuntimeBroker.exe',
  'svchost.exe', 'ntoskrnl.exe', 'winlogon.exe', 'wininit.exe', 'csrss.exe',
  'smss.exe', 'explorer.exe', 'qbittorent.exe', 'python.exe', 'WindowsTerminal.exe'
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
      print('Please wait this may take a moment...\n')

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
    base_dir = 'C:/Program Files/DyKnow'
    for r, d, f in os.walk(base_dir):
      for file in f:
        if file.endswith('.exe'):
          fileobj = f'{r}/{file}'.replace('/', '\\')
          allCrucial.append(fileobj)
    return allCrucial

  def findDyKnowExe(target_exe):
    base_dir = 'C:/Program Files/DyKnow'
    for r, d, f in os.walk(base_dir):
      for file in f:
        if target_exe in file:
          item = f'{r}/{file}'.replace(base_dir, '')
          if item.find('/') == 0:
            item = item.replace('/', '')
          return item.replace('\\', '/')

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
  def isAdmin():
    try:
      return ctypes.windll.shell32.IsUserAnAdmin()
    except:
      return False

  def checkPerms():
    admin = driver.isAdmin()
    if admin == False:
      print('ERROR: Hitman is running without admin, attempting self elevate.')
      time.sleep(2)
      ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable,' '.join(sys.argv), None, 1)
      time.sleep(1)
    if admin == True:
      pass

  def addProtected():
    file = f'{os.getcwd()}/protect.txt'.replace('\\', '/')
    if not os.path.exists(file):
      print(f'No library found at {file}, skipping.')
    else:
      with open(file, 'r') as protected_lib:
        content = protected_lib.read()
        for line in content.splitlines():
          protectedProcesses.append(line)

  def errorHandler(error_code):
    if error_code == '1':
      print('The execution operation already removed crucial files.')
      time.sleep(5)
      sys.exit(0)
    if error_code == '2':
      print('DyKnow files cannot be found, is it installed?')
      time.sleep(5)
      sys.exit(0)
    else:
      clear()
      print('Invaild input, quitting.')
      time.sleep(5)
      sys.exit(1)


# Initialization code (Cover your eyes)
if __name__ == '__main__':
  driver.checkPerms()
  if not driver.isAdmin():
    sys.exit(1)
  clear()
  print("   ----- Windows DyKnow Hitman ----- \
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
      print("Hitman cant locate DyKnow's files, This program might have already been ran if so please type 1 if not type 2.")
      q_a = input('> ')
      driver.errorHandler(q_a)
    for file in blacklisted:
      file_name = os.path.basename(file).split('\\')[-1]
      file = file.replace('\\', '/')
      if file_name in processes:
        if file not in protectedProcesses:
          del_file = sd.findDyKnowExe(file_name)
          print(f'File {file} is running as a process.')
          sd.removeRunning(del_file)
          print(f'Hitman killed/deleted running process {file}.')
      else:
        if file not in protectedProcesses:
          del_file = sd.findDyKnowExe(file_name)
          os.remove(f'C:/Program Files/DyKnow/{del_file}')
          print(f'Hitman deleted file {del_file}.')
        else:
          continue

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
    sys.exit(1)

else:
  print(f'ERROR: You cannot import {__file__}.')
  time.sleep(5)
  sys.exit(1)
