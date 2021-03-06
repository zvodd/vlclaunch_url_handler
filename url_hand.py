#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
from subprocess import Popen
import json
import platform


try:
    # Python 2.7
    from urlparse import urlparse
    from urllib import quote, urlencode
except ImportError:
    # Pythonn 3.4 untested
    from urllib.parse import urlparse, quote, urlencode

CURRENT_OS = platform.system().lower().strip()
OS_COMMAND_PARENTH = "'" 
OS_COMMAND_ESCAPE = '\\'

if CURRENT_OS == "windows":
    from win32api import GetSystemMetrics
    OS_COMMAND_PARENTH = '"' 
    OS_COMMAND_ESCAPE = '^'
    try:
        # Python 2.7
        import _winreg as wr
    except ImportError:
        # Pythonn 3.4
        import winreg as wr



class VLCArgumentCompile(object):

    def __init__(self, video_url, query_string, append_args = {} ):
        self.arg_dict = self.query_split_to_dict(query_string)
        self.arg_dict.update(dict(video_url = self.scrub_url( video_url)))
        if len(append_args) > 0 :
            self.arg_dict.update(append_args)

    def scrub_url(self, url):
        """ This should scrub the video_url
            TODO: Implement
        """
        return url

    def query_split_to_dict(self, query):
        args = {}
        segment = re.compile('[\?\&]')
        matches = segment.split(query)
        for arg in matches:
            kv = arg.split('=')
            if len(kv) == 2:
                k,v = kv
                args.update({k: v})
            else:
                args.update({arg: True})
        return args

    def get_args(self):
        """ Maps dictionary of parameters to vlc arguments list
        TODO
        * Scrub Everything to sane values or die.
        """
            
        argl = []
        ad = self.arg_dict
        def appendArg(fstring, a=None):
            """
            Adds strings to argl list (defined in localscope above)
            _fstring_ is a format string if _a_ is defined, other wise just 
            append _fstring_ to the list.
            In theory it should escape quote or double characters..
            but seeing as we use Popen to send arguments as a list,
            I think maybe the str.replace is usless or even error inducing.
            """
            arg = ""
            if a == None:
                arg = fstring.replace(OS_COMMAND_PARENTH, "{}{}".format(
                    OS_COMMAND_ESCAPE, OS_COMMAND_PARENTH) )
                argl.append(arg)
            else:
                arg = a.replace(OS_COMMAND_PARENTH, "{}{}".format(
                    OS_COMMAND_ESCAPE, OS_COMMAND_PARENTH))
                arg = fstring.format(a)
                argl.append(arg)

        if "fullscreen" in ad:
            appendArg("--fullscreen")
        if "ontop" in ad:
            appendArg("--video-on-top")
        if "minimal" in ad:
            appendArg("--qt-minimal-view")
        if "no_tree" in ad:
            appendArg('--no-playlist-tree')
        if 'width' in ad:
            appendArg('--width={}', ad['width'])
        if 'height' in ad:
            appendArg('--height={}', ad['height'])
        if 'video_x' in ad:
            appendArg('--video-x={}', ad['video_x'])
        if 'video_y' in ad:
            appendArg('--video-y={}', ad['video_y'])
        if "playspeed" in ad:
            appendArg("--rate={}", ad["playspeed"])
        # Maybe we should throw an exception even earlier,
        # if ad['video_url'] isn't there.
        appendArg(ad['video_url'])
        return argl


    def __dict__(self):
        return self.arg_dict

    def __repr__(self):
        return "VLCArgumentCompile: "+repr(self.__dict__())

def main():
    # "vlclaunch://video/play/?fullscreen&playspeed=2#https://www.youtube.com/watch?v=XVZrL4k1los"
    main_url = sys.argv[1]
    purl = urlparse(main_url)
    if purl.netloc == 'video':
        if purl.path == '/play/':
            vargs = VLCArgumentCompile(purl.fragment, purl.query)
            # print vargs
            launch(vargs.get_args())
        elif purl.path == '/playsmallmode/':
            screen_width = GetSystemMetrics (0)
            screen_height = GetSystemMetrics (1)
            smw =  screen_width / 4
            smh =  screen_height / 4
            smx = screen_width - smw
            smy = screen_height - smh
            small_mode_args = dict(
                width = smw,
                height = smh,
                video_x = smx,
                video_y = smy,
                minimal = None,
                ontop = None,
                no_tree = None
                )
            vargs = VLCArgumentCompile(
                            purl.fragment, purl.query, small_mode_args)
            launch(vargs.get_args())

def launch(args):
    command = [get_vlc_location()] + args
    print "command: {}".format(command)
    DETACHED_PROCESS = 0x00000008 #is this windows specific?
    Popen(command, close_fds=True, creationflags=DETACHED_PROCESS)

def get_vlc_location():
    with wr.OpenKey(
      wr.HKEY_CLASSES_ROOT,
      r"Applications\vlc.exe\shell\Open\command",
      0, wr.KEY_READ) as key:
        value, _ = wr.QueryValueEx(key,"")
    return value.split('"')[1]

if __name__ == "__main__":
    main()

