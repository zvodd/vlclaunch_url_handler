#
# -*- coding: utf-8 -*-
""" used to register python.exe and pythonw.exe in windows"""
import sys, os.path
try:
    import _winreg as wr
except ImportError:
    import winreg as wr

#
# To lazy for argparse, just change this line and run. 
#

PATH_TO_PYTHON = r"C:\Python27"
# PATH_TO_PYTHON = r"C:\Python34"

def register_executable_location(exename, location):
    """
    The executables must be found on windows shell ""path""
    i.e. in:
    HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\<x>
    ... not the enviroment variable "PATH".
    Putting it in path apperently doesnt cut the mustard
    for launching through a URL Protocol Handler
    """
    #
    full_exe_path =  os.path.join (location, exename)
    subkey = ("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\"
              + exename)
    success_write_count = 0
    for root_key in [wr.HKEY_LOCAL_MACHINE, wr.HKEY_CURRENT_USER]:
        try:
            with wr.CreateKeyEx(
                    wr.HKEY_LOCAL_MACHINE, subkey,
                    0, wr.KEY_WRITE) as key:
                wr.SetValueEx(
                    key, "", 0, wr.REG_SZ,
                    full_exe_path)
                wr.SetValueEx(
                    key, "Path", 0, wr.REG_SZ,
                    location)
                success_write_count += 1
        except WindowsError:
            pass
    if success_write_count < 1:
        print ("Failed to open key for writing in "
              +"HKEY_LOCAL_MACHINE and HKEY_CURRENT_USER.")
        return
    else:
        print ("successful registeration of '{}'".format(exename))
    return


def register_execatuble_class(exename, location):
    """
    Apperently registering an exe in:
        "HKEY_CLASSES_ROOT\Applications"
    It registers an application classes, for right click menus.
    It's not actually relevent for finding a execateable
     with the Win+R run command
    Did you know you can't set the type of a '(Default)' key in regedit.exe?
    i.e. Setting 'HKCR\Applications\python.exe\Shell\Open\Command\(Default)'
    to 'REG_EXPAND_SZ' from 'REG_SZ' is impossible using the regedit GUI.
    """
    subkey = "Applications\\"+ exename +r"\Shell\Open\Command"
    with wr.CreateKeyEx(wr.HKEY_CLASSES_ROOT, subkey, 0, wr.KEY_WRITE) as key:
        wr.SetValueEx(key, "", 0, wr.REG_EXPAND_SZ, '"{}" "%1"'.format(location))

if __name__ == "__main__":
    register_executable_location('pythonw.exe', PATH_TO_PYTHON)
    # register_executable_location('python.exe', PATH_TO_PYTHON)
