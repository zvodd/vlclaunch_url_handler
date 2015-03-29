#/usr/bin/env python
# -*- coding: utf-8 -*-
""" Used to register the URL Protocol Handler in Windows
    TODO:
    support other platforms...

"""

import sys, os.path
try:
    import _winreg as wr
except ImportError:
    import winreg as wr

PROTOCOL_NAME = "vlclaunch"

ACCESS_RIGHTS = (wr.KEY_WRITE | wr.KEY_READ
                | wr.KEY_QUERY_VALUE | wr.KEY_SET_VALUE
                | wr.KEY_CREATE_SUB_KEY | wr.KEY_ENUMERATE_SUB_KEYS)

def set_reg_keys():
    r"""
    HKEY_CLASSES_ROOT
        foo
            (Default) = "URL: Foo Protocol"
            URL Protocol = ""
            DefaultIcon
                (Default) = "foo.exe,1"
            shell
                open
                    command
                        (Default) = "C:\Program Files\example\foo.exe" "%1"
    """
    fpath, fname = os.path.split(os.path.abspath(sys.modules[__name__].__file__))
    url_hand_path =  '"{}"'.format(os.path.join(fpath, 'url_hand.py'))
    program_launch = ' '.join(['python', url_hand_path, '"%1"'])

    # print ("ACCESS_RIGHTS: {}".format(repr(ACCESS_RIGHTS)))
    with wr.CreateKeyEx(wr.HKEY_CLASSES_ROOT, PROTOCOL_NAME, 0, ACCESS_RIGHTS) as key:
        # print ("Opened Key: {}".format(repr(key)))
        wr.SetValueEx(key, "", 0, wr.REG_SZ, "URL: VLC Launch Protocol")
        wr.SetValueEx(key, "URL Protocol", 0, wr.REG_SZ, "")
        # with wr.CreateKeyEx(key, "DefaultIcon", 0, ACCESS_RIGHTS) as def_icon_key:
        #   wr.SetValue(def_icon_key, "", wr.REG_SZ, icon_path)
        shell_key = wr.CreateKeyEx(key, "shell", 0, ACCESS_RIGHTS)
        open_key = wr.CreateKeyEx(shell_key, "open", 0, ACCESS_RIGHTS)
        command_key = wr.CreateKeyEx(open_key, "command", 0, ACCESS_RIGHTS)
        wr.SetValueEx(command_key, "", 0, wr.REG_SZ, program_launch)
    print 'Installed URL Protocol Handler "{}"'.format(PROTOCOL_NAME)
    print "With shell command '{}'".format(program_launch)
    return

if __name__ == "__main__":
    set_reg_keys()