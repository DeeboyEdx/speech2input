# VOICE-TO-TYPE
#### Video Demo: url here
### Description

A desire to dictate to my computer expanded to wanting to give my computer voice commands like I do my Android phone; thus this project's inception.
I succeeded in creating something functional using python in combination with a number of free tools.  It isn't perfect and may not be competitive with Microsoft's pre-installed solution [Windows Speech Recognition](https://support.microsoft.com/en-us/windows/windows-speech-recognition-commands-9d25ef36-994d-f367-a81a-a326160128c7) but my method allows control from smart devices like a smartphone or a Google Home device which has far more widespread adoption; and which I find much more useful.  This project may also have applications for those who have impairments that hinder tactile computer input.

### Requirements
All requirements[^1] are *free*.  Paid versons of the accounts are unnecessary.  The only exception I can think of would be the PushBullet or IFTTT accounts if you've already used your free allotments.
- Windows PC
- a device w/ Google Assistant + a [Google](https://www.gmail.com) account
- [IFTTT](https://ifttt.com/) account
  -  (optional) [Tell my computer to... (Pushbullet Version)](https://ifttt.com/applets/U7MjJfV3) Applet. (recommended for simplicity)
- [Pushbullet](https://www.pushbullet.com/) account
- [Push2Run](https://www.push2run.com/) program
- [Python 3.x](https://www.python.org/downloads/)
  - [pynput](https://pypi.org/project/pynput/) module. TL:DR  `pip install pynput`
  - and perhaps other non-standard modules (TBD)
- (optional) [NirCmd](https://www.nirsoft.net/utils/nircmd.html) for audial responses

## Setup

1. Follow [these instructions](https://www.push2run.com/setup_pushbullet.html) to setup the connection from your Google Assistant to the Push2Run app you will install on your Windows computer.  Just with this alone you will already be able to do a lot as documented [with these example cards](https://push2run.com/examplecards.html); such as shutdown, reboot, google search, youtube search, open a program of your choice, etc.

2. (optional) "_Install_"[^2] **NirCmd** to enable synthesized "voice" responses from your computer.[^3]  It's a small command-line utility that allows you to do some useful tasks without displaying any user interface.  TBH, some of its functionality overlaps with this project's so if you wish, you can bypass python altogether by using Push2Run and NirCmd creatively.

   >It's recommended to copy the executable of NirCmd (nircmd.exe) to your windows directory, or to any other folder listed in your PATH environment variable, so you won't need to type the full path of nircmd in each time that you want to use it.


3. Setup Push2Run (p2r) cards.  By this step, you should be ready to create (or import) the cards that will facilitate the connection between Push2Run and these python project files.

>#### A brief Push2Run primer... 
>* You will have setup spoken keyword(s) in IFTTT to indicate which verbal commands to forward to PushBullet.  In our scenarios, we will use the keywords "_tell my comptuer to_" which colloquially make sense.[^4]
>
>* `$` represents your variable.  For example, let's say you've setup your Type card as below with "type $" as one of the entries in the 'Listen for' field...[^5]
>
>   You say: "_tell my comptuer to_ type **it is a lovely day period**"
> 
>   type.py will recieve: "**it is a lovely day period**" which it will then format the string nicely and simulate the key presses to type it out on your computer.  "It is a lovely day."

  ## __Type__ card
  We'll start with the dictation card.
  With this, you'll be able to TELL your computer to type out long sentences.
  ![image](https://user-images.githubusercontent.com/71462840/146619077-ebca46e2-0119-4d00-a05d-c976aa0ef4e0.png)
  

  ## __Command__ card
  Next is the command card.
  With this, you'll be able to TELL your computer to perform a multitude of physical inputs, either colloquially "minimize" or literally "press alt space n".  See list of examples.  **TODO**
  ![image](https://user-images.githubusercontent.com/71462840/146622849-f7a05af8-faef-4a3b-991c-d41e045781b2.png)
  
  ## __Volume__ card
  With this card, you'll be able to TELL your computer what volume to set.  You can also tell it to mute, un-mute, toggle mute, or even to "shut up".  TBH, I'm still working on the kinks for this one since the object of a spoken sentence regarding "volume" or "sound" can just as easily be either in the beginning or at the end of a sentence.
  ![image](https://user-images.githubusercontent.com/71462840/146622938-419fec15-63c8-4a9c-a6f7-5e415f2c93ab.png)

>* within the "Listen for" field, the `*` is a throw-away catch-all.  It's only purpose is for matching phrases, not for capturing text.  For example...
>   
>   You say: "_tell my computer to_ lower the dang volume **to 20 percent**"
>   
>   Push2Run will match and throw away "lower the dang"
>   
>   change_audio_volume.py will recieve: "**to 20 percent**"


#### Caveats, acknowledgements, and known bugs to fix
- [x] *An internet connection is required for your computer to recieve commands.*
- [x] *You must be logged into your computer for most actions to succeed.*
- [x] Google Assistant's attention span is short so commands must be swift and to the point.
  - [x] ...as such, as a method of performing multiple actions, utilization of this project may be ineffectual.
- [x] Giving literal key-press commands can be tricky to impossible as it is wholly dependent on what Google Assistant thinks it heard you say.  Ex. "n" or "end" >_>
- [ ] Log file location may differ depending on whether script is executed from console or by Push2Run.

# (partial) List of viable commands
Please note the following
* You can chain commands together with delimeters "and", and "then".
* You can also delay commands with "wait|sleep|hold x seconds|minutes|hours".
* Although Google Assistant will handily detect in your speech when you meant to use punctuation, to explicitely indicate to type.py to produce a punctuation mark, you must say "mark" or "sign" afterwards.  Ex. "open curly bracket mark"
## Typing
* type a phrase of your choice comma with punctuation exclamation mark
* type i'll  be there at 6 pm period send
## Colloquial
* maximize
* minimize
* restore
* minimize all
* minimize everything else
* move
* resize
* resize left
* resize right
* resize bottom
* resize top
* dock left
* dock right
* close program
* change program
# Media
* pause
* play
* full screen (comptible for toggling full screen on most players)
## Literal
* alt tab (five times)
* alt space n
* shift r
* (most other combinations you can think of)
* control alt delete (is a protected key combination thus will NOT work)
## in Browser
* go to website dot com
* refresh
* go back
* go forward
* new tab
* close tab
* reopen tab
* change tab
## Text
* select all
* cut
* copy
* paste
* undo
* redo
* home
* end
* page up
* page down
* save
* save as
* emojis (don't get excited, just pulls up the menu)
* change input language
## System
* show notifications
* show time
* show calendar
* start dictation (uses Windows Speech Recognition)
* show settings
* take screenshot
* save screenshot
* open system menu
* open control panel
## Misc
* wait 10 seconds and ...
* type I see you exclamation mark after 3 minutes

[^1]: Aside from the Windows PC and a device with Google Assistant, of course.  Both are ubiquitous but I recognize accessibility to these devices is not universal.
[^2]: Just download and extract to the appropriate PATH directory.
[^3]: Currently, audial responses are only used to confirm volume adjustments and to inform the user when a command was not understood.
[^4]: I'm not fond of the confusing way IFTTT uses the terminology "connect" to either mean _to enable_ an applet or _to get_ one from their store of sorts.  Maybe it's just me.  That aside.  Thankfully if you choose to utilize the "applet" created by loneseeker777 called "[Tell my computer to... (Pushbullet Version)](https://ifttt.com/applets/U7MjJfV3)", you won't utilize one of your 3 (of 5?) slots.  I know, it's dumb but at least it's doable for free.
[^5]: You can list multiple "Listen for" phrases.  Be sparing here as the more variability you add, the greater your chances of stepping on another card's toes causing unexpected results.  As you may experience with the Volume cards later.
