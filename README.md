## What is this?

Currently a collection of scripts designed to register and make use of a URL Protocal Handler for launching VLC.

## Example urls:

```
    To launch a video:
        vlclaunch://video/play/?#https://www.youtube.com/watch?v=XVZrL4k1los

    Additional parameters:
        vlclaunch://video/play/?fullscreen&playspeed=1.5#https://www.youtube.com/watch?v=XVZrL4k1los

    Smallmode launchs the video in minumal-ui and always-on-top modes on bottom right corner of screen 
        vlclaunch://video/play/?fullscreen&playspeed=1.5#https://www.youtube.com/watch?v=XVZrL4k1los

```

## Disclaimer

Works under windows only at the moment, because lazy.
Probably only works under Python 2.7 because I havent actually tested in 3 and surly did somthing wrong.
You need to do things to make it work.

## How do I do things?

Get a command line in to this folder, making sure your PATH and PYTHON_PATH enviroment variables are set for python.

##### Step 1:
```    
$> python url_reg.py
```
You should now be able to click on "vlclaunch://" urls and things happen.

##### Step 2:
Write something to make use of the vlclaunch url proto handler.
Maybe a browser extention.... probably for youtube or something.

##### Step 3:
Profit


## TODO

#### URL Handler Registerer / Installer:

* Setup.py and possibly a userfriendly installer.

* Linux URL Proto Registration (Gnome, Unity, KDE).

* Mac OSX URL Proto Registration.

* Possibly combine URL Handler Registration into a crossplatform library.

#### URL Handler:

* Use a configuration file.

* Improve VLC path finding, instead of reading unrealiable registry keys.

* Investigate poential security issues.

* Valid all data to sane values before throwing it at OS shell.

* Userscript for video site intergration and video urls. (Seperate Project)

## Potential Security Problems

URL protocal handlers are risky business.

##### Python command injection
Probably on windows.
Because we are using python? We can maybe pass a python command?
```
    vlclaunch://video/play/?#" -c "f = open('wtfbbq.exe','w'); f.write('wtfbbw'); f.close(); from subprocess import Popen; Popen(['wtfbbw.exe'])"
```
e.g.
Because the registered protocal handler is actually:
```
    python.exe "C:\[scriptlocation]\url_handler.py" "%1"
```
In theory the windows shell would execute:
```
    python url_hand.py "vlclaunch://video/play/?#" -c "f = open('wtfbbq.exe','w'); f.write('wtfbbw'); f.close(); from subprocess import Popen; Popen(['wtfbbw.exe'])"
```

Maybe py2exe or nuikta can be used to compile an executable to remove the possible python -c exploit.
If it can be proven.

##### File url and additional parameters

VLC allows file:// urls as well as a number of complex arguments for transcoding that shouldn't be exposed.

*Be stricter about what passes for a video url.

*URL encode / validate before putting on the commandline.

##### Shell injection

Lack of value scrubbing, leaves a nasty exploit vector.
On posix systems;
Imagine you have this url handler installed and you go to a page with:

    vlclaunch://video/play/?#;echo This is bad;

Could end up coming out like this:
```
    "vlc "; echo This is bad"
```
Although I think the way we use subproccess.Popen will prevent it?
On windows I fairly sure the shell won't run more than one executable.
