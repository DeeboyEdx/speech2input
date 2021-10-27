I wanted to be able to give my computer voice commands like I do my Android phone thus this project's inception.
I succeeded in creating something functional using python in combination with a number of free tools.  It isn't perfect and may not be competitive with Microsoft's pre-installed solution [Windows Speech Recognition](https://support.microsoft.com/en-us/windows/windows-speech-recognition-commands-9d25ef36-994d-f367-a81a-a326160128c7) but my method allows control from smart devices like a smartphone or a Google Home device which has far more widespread adoption; and I find much more useful.  This project may also have applications for those who have impairments that hinder regular computer use as well.

# Requirements
All requirements are *free*.[^1]  Paid versons of the accounts are unnecessary.  The only exception I can think of would be the PushBullet account if you've already used your free allotment.
- [Google](https://www.gmail.com) account, and device w/ Google Assistant
- [IFTTT](https://ifttt.com/) account
- [Pushbullet](https://www.pushbullet.com/) account
- Windows PC
- [Push2Run](https://www.push2run.com/) program
- [Python](https://www.python.org/downloads/)
  - [pynput](https://pypi.org/project/pynput/) module. TL:DR  `pip install pynput`
  - and perhaps other non-standard modules (TBD)
- (optional) [NirCmd](https://www.nirsoft.net/utils/nircmd.html) for audial error responses

# Setup

1. Follow these steps to setup the connection from your Google Assistant to the Push2Run program on your computer.  https://www.push2run.com/setup_pushbullet.html

2. (optional) **NirCmd** is a small command-line utility that allows you to do some useful tasks without displaying any user interface.  It is used by this project to produce speach responses from your computer.

   More specifically, its text-to-speach function is used to produce an audial response when a users's input is not understood, thus ignored.  The effect is that when you tell your computer to do something it doesn't understand, it'll respond back saying it didn't understand your command.

   This project was designed with the expectation that the utility would be accessible without needing to specify a path.  I believe you can simply put the executable into the same directory as the python files but I suggest following their recommendation.
   
   >It's recommended to copy the executable of NirCmd (nircmd.exe) to your windows directory, or to any other folder listed in your PATH environment variable, so you won't need to type the full path of nircmd in each time that you want to use it.


3. Once you have the connection from your Google Assistant to Push2Run functioning, you can create the following Push2Run card(s) to facilitate the voice commands on your PC.

   **TODO**  More details to come...


*Caveat: You must be logged into your computer for most actions to succeed.*

# Known Bugs to fix
- [ ] Log file location differs depending on whether script is executed from console or by Push2Run.

[^1]: Aside from the Windows machine and a device with Google Assistant, of course.
