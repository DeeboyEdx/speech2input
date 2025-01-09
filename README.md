# Speech2Input

Convert spoken commands into typed text or actions on your Windows computer by integrating smart devices, software, and services.

## Demo video

[![demo video](https://img.youtube.com/vi/2mzV1V0gVAE/0.jpg)](https://www.youtube.com/watch?v=2mzV1V0gVAE)

## Project description

This project allows you to convert spoken commands from smart devices, like Amazon Echo and Google Assistant, into typed text or executable actions on your Windows computer. By integrating various software and services such as Push2Run, Pushbullet, and Python scripts, you can control your PC using voice commands.

### Background

This project originated from a simple desire to dictate to my computer, evolving into a quest for voice command functionality akin to my experience with an Android phone. While this project may not rival other solutions such as [Microsoft's voice access](https://support.microsoft.com/topic/get-started-with-voice-access-bd2aa2dc-46c2-486c-93ae-3d75f7d053a4), my approach is open source, highly customaizable, and enables remote control from your smart devices. So, it offers for some a more valuable experience.

## Prerequisites

All requirements are *FREE*[^1] or free to a certain extent.

- Windows PC
  - [Push2Run](https://www.push2run.com/) application
  - [Python 3.x](https://www.python.org/downloads/) and [pynput](https://pypi.org/project/pynput/) module
  - [NirCmd](https://www.nirsoft.net/utils/nircmd.html) for audial responses (optional)
- [Pushbullet](https://www.Pushbullet.com/) account
- A smart home assistant device. These are two compatible options, AFAIK.
  - an Amazon Echo - **recommended**
    - with the [PC Commander](https://pccommander.net/) skill
  - a Google Assistant device
    - and an [IFTTT](https://ifttt.com/) account
      - with applicable applet(s)
> [!IMPORTANT]
> Due to Google's August 2022 bull**** change, the IFTTT route no longer supports variables or "ingredients[^7]" in its commands so applets must be hard-coded.

## Setup
1. **Create Pushbullet Account**: Go to [pushbullet.com](https://www.pushbullet.com/).
1. **Install Push2Run**: Download and install the [Push2Run](https://www.push2run.com/) application on your Windows PC.
1. **Set Up Smart Device**: Connect your smart device to Pushbullet.
    - **Amazon Echo**: Use the [PC Commander skill](https://www.amazon.com/dp/B0DFRQYYC3/) for integration.
    - **Google Assistant**: Use [IFTTT](https://ifttt.com/) to link Google Assistant with Pushbullet.
1. **Install Python and Dependencies**: Install Python 3.x, the `pynput` module (`pip install pynput`), and NirCmd.
1. **Download Project Files**: Download the project files and place them into `C:\Scripts\speech2input\` or a directory of your choosing.
1. **Configure Push2Run**: Link Push2Run with your Pushbullet account, and import the `p2r` file or create cards in Push2Run to link voice commands to Python scripts.<details><summary><strong>Instructions</strong></summary>
    - for **Amazon Echo** route: https://pccommander.net/howto/push2run/  
    - for **Google Assistant** route: https://github.com/roblatour/Push2Run/blob/main/help/setup_Google_IFTTT_Pushbullet.md
    </details>

> [!WARNING]
> If you chose a custom project directory and wish to import the `p2r` file, update the path of each entry's *Parameter* field to the directory you chose. This can be done either directly in the file with a text editor before importing, or after importing within Push2Run's GUI.

  <br>

<details><summary><strong>Click here for a list of the cards included in the p2r file.</strong></summary>

|Action|Description|
|-|-|
|**Pause/Play**|Presses space bar|
|**Full Screen**|Presses f key|
|**Full Screen and Play**|Presses f then space bar key|
|**Computer! Do Things**|Attempts to interpret command as Windows action(s). Types out as a sentence if it can't interpret it.|
|**Type \***|Bypass command interpretation (uses `-v` flag) to simply type out the supplied text|
|**No matching phrases**|"*No matching phrases*" is a special catch-all phrase that's triggered when no other card was triggered. Functionality is same as the "*Computer! Do Things*" card.|

</details>

<details><summary>Read an additional Push2Run primer...</summary>
<p>

By this point, your digital assistant should understand a certain invocation phrase to indicate to forward commands through your Pushbullet service which is then captured by Push2Run. There are a couple points to learn about Push2Run if you want to best harness it's power. In the following example scenarios, we'll use the invocation phrase "*tell my computer to* ~", the default for the Amazon Echo route, and which most colloquially makes sense.

- `$` represents your variable.  For example, let's say you've setup your Type card just like in the `p2r` file, with "type $" as one of the 'Listen for' entries[^4] and `main.py -v "$"` in the parameters field.

    You say: "*tell my computer to* **type** it is a lovely day period mark"

    `main.py` receives `-v "it is a lovely day period mark"` (`-v` being the verbatim flag), then formats the string nicely, and lastly simulates the key presses to type out "**It is a lovely day.**" on your computer.

- Within the 'Listen for' field, the `*` is a throw-away, catch-all character. It's purpose is for matching miscellaneous phrases, not for capturing text.

  For example, let's say that you've put created a card named *Change Volume* with "* volume $" in the 'Listen for' field, and `change_audio_volume.py "$"` in your Parameters field.
  1. You say: "*tell my computer to* lower the gosh darn **volume to 20 percent**"
  1. Push2Run will match and throw away "lower the gosh darn".
  1. Match the "**volume**" keyword to the *Change Volume* card.
  1. And pass long "**to 20 percent**" to the script.

</p>
</details>

## How to use directly

Here's how to utilize these project files directly, without relying on Push2Run triggers.

- To type out a string to your computer with basic formatting use...

  `python main.py -v <string>`

- To give your computer a command ([for example these](#list-of-viable-commands)) use...

  `python main.py <command>`

> [!NOTE]
> These commands will execute immediately so if you wish to type on or control a particular application, you will need to either execute the command in a hidden window or use a delay timer.

## List of viable commands

Please note the following

- You can chain commands together with delimiters "and", and "then".[^6]
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

## Caveats, acknowledgements, and known bugs to fix

- [x] *An internet connection is required for your computer to recieve commands.*
- [x] *You must be logged into your computer for most, if not all, actions to succeed.*
- [x] A digital assistant's attention span is short. So, commands must be swift and to the point.
  - [x] As such, performing multiple or complex actions utilizing this project may prove difficult.  Thankfully the Alexa method has a follow-up mode which alleviates this pressure.
- [x] Giving literal key-press commands can be tricky to near impossible as it is wholly dependent on what the digital assistant *thinks* it heard with their tendency to listen for natural spoken language.  For example, it may hear "end" when you say "n".  I try to work with this by providing an equivalency dictionary but it isn't perfect.
- [ ] Log file location may differ depending on whether the script is executed from the console[^5] or by Push2Run.

## Footnotes

[^1]: Aside from the Windows PC and a device with smart home assistant, of course.  These devices are ubiquitous but I recognize accessibility to these devices is not universal.
[^2]: Download and extract to a location in your PATH environmental variable OR this project's root folder.
[^3]: Currently, audial responses are only used to confirm volume adjustments and to inform the user when a command was not understood.
[^4]: You can list multiple "Listen for" phrases.  Be sparing here as the more variability you add, the greater your chances of stepping on another card's toes, leading to unexpected results.  As you may experience with the Volume cards later.
[^5]: To execute from console do `python main.py DESIRED COMMAND HERE`.  Use the `-v` argument to avoid interpretation and simply dictate.  `python main.py -v DESIRED SENTENCE HERE`  You may choose to use quotations around your command (`"DESIRED COMMAND"`) if you wish.
[^6]: Actually by default, Push2Run also uses "and" as a delimiter to separate commands.  Given that setting, I acknowledge that the "Full Screen and Play" card is redundant when you have separate "Full Screen" and "Pause/Play (press Space bar)" cards.
[^7]: Fucking stupid name for it.
