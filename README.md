# VOICE-TO-TYPE

Use your smart home device to command or dictate to your Windows computer.

## Demo Video

[![Voice-to-type demo video](https://img.youtube.com/vi/2mzV1V0gVAE/0.jpg)](https://www.youtube.com/watch?v=2mzV1V0gVAE)

## Description

A desire to dictate to my computer expanded to wanting to use voice commands with my computer like I do my Android phone; thus this project's inception. I created something functional using python in combination with a number of free tools.  It may not be competitive with Microsoft's [Windows Speech Recognition](https://support.microsoft.com/windows/windows-speech-recognition-commands-9d25ef36-994d-f367-a81a-a326160128c7) solution, but my method allows control from smart devices which have widespread adoption, and I find it more useful.  This project may also have applications for those who have impairments that hinder tactile computer input.

## Prerequisites

All requirements are *FREE*[^1].  The only exceptions are if you've already used your free allotments, would be the Pushbullet and/or IFTTT accounts.

- Windows PC
  - [Push2Run](https://www.push2run.com/) application
  - [Python 3.x](https://www.python.org/downloads/)
    - [pynput](https://pypi.org/project/pynput/) module. TL:DR  `pip install pynput`
  - (optional) [NirCmd](https://www.nirsoft.net/utils/nircmd.html) for audial responses
- [Pushbullet](https://www.Pushbullet.com/) account
- A smart device from which to send Pushbullet messages. (These are two options I've used)
  - a device with Amazon Alexa smart home assistant [**recommended FREE option**]
    - with the [PC Pusher skill](http://pcpusher.s3-website.us-east-2.amazonaws.com/) (currently in beta)
  - a device with Google Assistant [Potentially Free option]
    - and an [IFTTT](https://ifttt.com/) account
      - with an applet that links your Google and Pushbullet services such as [Tell my computer to... (Pushbullet Version)](https://ifttt.com/applets/U7MjJfV3)

## Setup

1. Install the [Push2Run](https://www.push2run.com/) application.

1. Setup one or both of these smart home device connections to your Pushbullet service.

   - **Alexa Route**: Refer to the [PC Pusher website](http://pcpusher.s3-website.us-east-2.amazonaws.com/) for instructions.

   - **Google Route**: Follow [these instructions](https://www.push2run.com/setup_Pushbullet.html).  

   With the completion of these steps, you will be able to do a lot such as shutdown, reboot, google search, youtube search, open a program of your choice, etc.  See more [with these example cards](https://push2run.com/examplecards.html).

1. Download this project's files to a directory of your choosing.  Take note of it as you will need it later.
   - change_audio_volume.py
   - dee_logging.py
   - keypress_functions.py
   - type.py
   - Push2Run_type_cards.p2r (optional)

   *The other files are unnecessary.*

1. (optional) "*Install*"[^2] **NirCmd** to enable synthesized "voice" responses from your computer.[^3]  This is a small command-line utility that allows you to do some useful tasks such as voice synthesis.

1. Setup Push2Run (p2r) cards.  By this step, you should be ready to import (or create) cards that will facilitate the connection between Push2Run and these python project files.  To import, simply drag the included [Push2Run_type_cards.p2r](Push2Run_type_cards.p2r) file (a JSON file) into your Push2Run client.  Feel free to discard the file once imported.

   ### What cards will be imported

    - **Pause/Play**<br>Presses space bar
    - **Full Screen**<br>Presses f key
    - **Full Screen and Play**<br>Presses f and space bar
    - **Type \***<br>Bypass command interpretation to simply type out the supplied text
    - **Computer! Do Things**<br>A catch-all card. Attempts to interpret any messages which didn't trigger a Push2Run card as a command.
    - **No matching phrases**<br>Same catch-all function as above

1. Change the path in the *Parameter* field to the directory of your choosing from step 3, where you've placed this project's files.  In the provided cards, the path is `C:\Scripts\python\type\`.  This can be done either in the p2r file before importing, or after importing within the Push2Run GUI.
    <br><br>

    <details><summary><strong>Click here to see how to build your own cards.</strong></summary>

    Note that all these cards are set to the "Hidden" window state which is important to prevent a terminal window from being shown.

    <p>

    ## **Type** card

    We'll start with the dictation card.
    With this, you'll be able to tell your computer to **type out** long sentences.

    ![Type card example](https://user-images.githubusercontent.com/71462840/146619077-ebca46e2-0119-4d00-a05d-c976aa0ef4e0.png)
    <br><br>

    ## **Command** card

    Next is the command card.
    With this, you'll be able to tell your computer to **perform** a multitude of physical inputs, either colloquially (ex. "minimize") or literally (ex. "press alt space n").  See [more](#literal).

    ![Command card example](https://user-images.githubusercontent.com/71462840/146622849-f7a05af8-faef-4a3b-991c-d41e045781b2.png)
    <br><br>

    ## **Volume** card

    With these cards, you'll be able to tell your computer to change the volume.  You can also tell it to mute, un-mute, toggle mute, or even to "shut up".  I'm still working out the kinks for this one so I did not include a card for volume adjustments in the included p2r file.

    Note that there are two cards as I found it more successful to separate them like so.

    ![Volume card example](https://user-images.githubusercontent.com/71462840/146622938-419fec15-63c8-4a9c-a6f7-5e415f2c93ab.png)

    </p>
    </details>

    <details><summary>Read an additional brief Push2Run primer...</summary>
    <p>

    By this point, you will have an invocation keyword set up to indicate to your digital assistant to forward commands through your Pushbullet service which will be captured by Push2Run.  In this readme's example scenarios, we will use the "tell my computer to ~" keywords (the default for both proposed routes) which colloquially just makes sense.

    - `$` represents your variable.  For example, let's say you've setup your Type card as below with "type $" as one of the entries in the 'Listen for' field...[^4]

       You say: "*tell my computer to* type **it is a lovely day period mark**"

       type.py will recieve: "-v **it is a lovely day period mark**" (-v being the verbose flag) which it will then format the string nicely and simulate the key presses to type it out on your computer.  "**It is a lovely day.**"

    - within the "Listen for" field, the `*` is a throw-away catch-all.  It's only purpose is for matching phrases, not for capturing text.  For example...
      1. You say: "*tell my computer to* lower the gosh darn **volume to 20 percent**"
      1. Push2Run will match and throw away "lower the gosh darn".
      1. And pass long "**volume to 20 percent**" to the script.

    </p>
    </details><br>

    <details><summary>Caveats, acknowledgements, and known bugs to fix</summary>
    <p>

    - [x] *An internet connection is required for your computer to recieve commands.*
    - [x] *You must be logged into your computer for most (if not all) actions to succeed.*
    - [x] Digital assistants' attention span is short so commands must be swift and to the point.
      - [x] As such, performing multiple or complex actions utilization of this project may prove difficult.  Thankfully the Alexa method has a follow-up mode which alleviates this pressure.
    - [x] Giving literal key-press commands can be tricky to near impossible as it is wholly dependent on what the digital assistant *thinks* it heard and their tendency to listen for colloquial language.  For example, it may hear "end" when you say "n".  I try to work with this by providing an equivalency dictionary but it isn't perfect.
    - [ ] Log file location may differ depending on whether script is executed from console[^5] or by Push2Run.

    </p>
    </details>

## How to use directly

Here's how to utilize these project files directly, without relying on Push2Run triggers.

- To type out a string to your computer with basic formatting use...

  `python type.py -v <string>`

- To give your computer a command (see them listed below) use...

  `python type.py <command>`

  Note that these commands will execute immediately so if you wish to type on or control a particular application, you will need to either execute the command in a hidden window or use a delay timer.

## List of viable commands

Please note the following

- You can chain commands together with delimeters "and", and "then".[^6]
<!-- Actually this isn't working now.  Gotta debug.
* You can also delay commands with "wait|sleep|hold x seconds|minutes|hours".
  * Ex. `tell my computer to wait 30 seconds then press start button`-->

- Although Google Assistant will handily detect in your speech when you meant to use punctuation, and I acknowledge it's a mouth-full but to explicitely indicate to the script to produce a punctuation mark, you must say "mark" or "sign" afterwards.  For example: "open curly bracket mark x closed curly bracket sign" -> "{ x }"

### Typing

- type a phrase of your choice comma with punctuation exclamation mark
- type i'll  be there at 6 pm period mark send

### Colloquial

- maximize
- minimize
- restore
- minimize all
- minimize everything else
- move
- resize
- resize left
- resize right
- resize bottom
- resize top
- dock left
- dock right
- close program
- change program

### Media

- pause
- play
- full screen (comptible for toggling full screen on most players)

### Literal

- alt tab [five times]
- alt space n
- shift r
- etc.
- control alt delete <- is a protected key combination thus will NOT work

### in Browser

- go to website dot com
- refresh
- go back
- go forward
- new tab
- close tab
- reopen tab
- change tab

### Text

- select all
- cut
- copy
- paste
- undo
- redo
- home
- end
- page up
- page down
- save
- save as
- emojis (don't get excited, just pulls up the menu)
- change input language

### System

- show notifications
- show time
- show calendar
- start dictation (uses Windows Speech Recognition)
- show settings
- take screenshot
- save screenshot
- open system menu
- open control panel

### Misc

- wait 10 seconds and ...
- type I see you exclamation mark after 3 minutes

[^1]: Aside from the Windows PC and a device with smart home assistant, of course.  These devices are ubiquitous but I recognize accessibility to these devices is not universal.
[^2]: Download and extract to a location in your PATH environmental variable OR this project's root folder.
[^3]: Currently, audial responses are only used to confirm volume adjustments and to inform the user when a command was not understood.
[^4]: You can list multiple "Listen for" phrases.  Be sparing here as the more variability you add, the greater your chances of stepping on another card's toes causing unexpected results.  As you may experience with the Volume cards later.
[^5]: To execute from console do `python type.py DESIRED COMMAND HERE`.  Use the `-v` argument to avoid interpretation and simply dictate.  `python type.py -v DESIRED SENTENCE HERE`  You may choose to use quotations around your command (`"DESIRED COMMAND"`) if you wish.
[^6]: Actually by default, Push2Run also uses "and" as a delimeter to separate commands.  Given that setting, I acknowledge that the "Full Screen and Play" card is redundant when you have separate "Full Screen" and "Pause/Play (press Spacebar)" cards.
