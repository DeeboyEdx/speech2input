# Speech2Input

Convert spoken commands into actions or typed text on your Windows computer by integrating smart devices, software, and services.

## Demo video

[![demo video](https://img.youtube.com/vi/2mzV1V0gVAE/0.jpg)](https://www.youtube.com/watch?v=2mzV1V0gVAE)

## Project description

This project is the last leg of a system that allows you to convert spoken commands from smart devices, like Amazon Echo and Google Assistant, into actions or typed text on your Windows computer. We achieve this by integrating these project files with a chain of services and software, as detailed below.

### Background

This project originated from a simple desire to dictate to my computer, evolving into a quest for voice command functionality akin to that on an Android phone. While there are several other solutions out there, such as [Microsoft's voice access](https://support.microsoft.com/topic/get-started-with-voice-access-bd2aa2dc-46c2-486c-93ae-3d75f7d053a4), the approach detailed here is light weight, open source, highly customizable, and enables remote control from your smart devices.

## Prerequisites

All requirements are *FREE*[^1] or [free to a certain extent](#free-really).

- Windows PC
  - [Push2Run](https://www.push2run.com/) application
  - [Python 3.x](https://www.python.org/downloads/) and [pynput](https://pypi.org/project/pynput/) module
  - [NirCmd](https://www.nirsoft.net/utils/nircmd.html) for audial responses (optional)[^2]
- [Pushbullet](https://www.Pushbullet.com/) account
- A smart home assistant device. These are two compatible options, AFAIK.
  - an Amazon Echo - **recommended**
    - with the [PC Commander](https://pccommander.net/) skill
  - a Google Assistant device
    - and an [IFTTT](https://ifttt.com/) account
      - with applicable applet(s)

## Setup

Follow these steps to build the data chain that will take your voice commands from your smart assistant, all the way to your computer and feed it to this project's Speech2Input scripts.

1. **Create Pushbullet Account**: At [pushbullet.com](https://www.pushbullet.com/)
1. **Set Up Smart Device**: Connect your smart device to the Pushbullet service.<details><summary><strong>Instructions</strong></summary>
    - **Amazon Echo**: Use the [PC Commander skill](https://pccommander.net/howto/enable/) for integration.
    - **Google Assistant**: Use [IFTTT](https://ifttt.com/) to link Google Assistant with Pushbullet using [these instructions](https://github.com/roblatour/Push2Run/blob/main/help/setup_Google_IFTTT_Pushbullet.md#:~:text=8.-,Sign%20onto%20IFTTT,-Notes%3A%0A%0Aa).
    </details>
> [!NOTE]
> Due to Google's August 2022 bull**** change, the IFTTT route no longer supports variables or "*ingredients*"[^3] in its commands so applets must be hard-coded.
3. **Install Push2Run**: Download and install the [Push2Run](https://www.push2run.com/) application on your Windows PC.
1. **Configure Push2Run**: Link Push2Run with your Pushbullet account, and import the `p2r` file or create cards in Push2Run to link voice commands to Python scripts.<details><summary><strong>Instructions</strong></summary>
    - for **Amazon Echo** route: https://pccommander.net/howto/push2run/  
    - for **Google Assistant** route: https://github.com/roblatour/Push2Run/blob/main/help/setup_Google_IFTTT_Pushbullet.md
    </details>
> [!WARNING]
> If you chose a custom project directory and wish to import the `p2r` file, update the path of each entry's *Parameter* field to the directory you chose. This can be done either before importing with a text editor, or after importing within Push2Run's GUI.
5. **Install Python and Dependencies**: Install Python 3.x, then the `pynput` module (by executing `pip install pynput` in a command line after installing Python).
  > [!IMPORTANT]
  > It's recommended to select "**Add python.exe to PATH**". Otherwise, you must use the full python executable path in your Push2Run cards.
6. **Download Project Files**: Clone or download the project files, **along with NirCmd**, into `C:\Scripts\speech2input\` or a directory of your choosing.
  > [!TIP]
  > If executed directly, Nircmd will offer you a button to copy it to your Windows directory. Alternatively, you may place NirCmd elsewhere but you'll need to add its path to PATH.

  <br>

<details><summary><strong>Click here for a list of the cards included in the p2r file.</strong></summary>

|Action|Description|
|-|-|
|**Type \***            |Bypass command interpretation (uses `-v` flag) to simply type out the supplied text|
|**Computer! Do Things**|Attempts to interpret command as Windows action(s).|
|**Open \***            |Opens a program.|
|**Close \***           |Closes a program.|
|**Voice Typing**       |Opens Microsoft's dictation solution.|
|**Voice Access**       |Opens Microsoft's voice control solution.|
|**Voice Update**       |Opens Windows update.|
|**No matching phrases**|"*No matching phrases*" is a special catch-all phrase that's triggered when no other card was triggered. Functionality is same as the "*Computer! Do Things*" card.|

The first two cards use this project's python script(s). The rest are bonus useful cards.

</details>

<details><summary>Read an additional Push2Run primer...</summary>
<p>

By this point, your digital assistant should understand a certain invocation phrase to indicate to forward commands through your Pushbullet service which is then captured by Push2Run. There are a couple points to learn about Push2Run if you want to best harness it's power. In the following example scenarios, we'll use the invocation phrase "*tell my computer to* ~", the default for the Amazon Echo route, and which most colloquially makes sense.

- `$` represents your variable input.  For example, let's say you've setup your Type card just like in the `p2r` file, with "type $" as one of the 'Listen for' entries[^4] and `main.py -v "$"` in the parameters field.

    You say: "*tell my computer to* **type** it is a lovely day period mark"

    `main.py` receives `-v "it is a lovely day period mark"` (`-v` being the verbatim flag), then formats the string nicely, and lastly simulates the key presses to type out "**It is a lovely day.**" on your computer.

- Within the 'Listen for' field, the `*` is a throw-away, catch-all character. It's purpose is for matching miscellaneous phrases, not for capturing text.

  For example, let's say that you've put created a card specifically for modifying volume with "* volume $" in the 'Listen for' field, and `change_audio_volume.py "$"` in your Parameters field.
  1. You say: "*tell my computer to* lower the gosh darn **volume to 20 percent**"
  1. Push2Run will match and throw away "lower the gosh darn".
  1. Match the "**volume**" keyword to the card.
  1. And pass long "**to 20 percent**" to the script.

</p>
</details>

## How to execute python scripts

Here's how these project files can be used. There are two primary ways. Either...

- A) Type out a string to your computer with basic formatting.

  `python main.py -v [<string>...]`

- B) Or have the scripts try to interpret your command to your computer. See[supported commands](#list-of-viable-commands).

  `python main.py [<command>...]`

> [!NOTE]
> These commands will execute immediately so if you wish to type on or control a particular application, you will need to either execute the command in a hidden window or use a delay timer.

## List of viable commands

Please note the following considerations.

- You can chain commands together with delimiters "and", and "then".[^5]  For example...

  "press windows r **then** type notepad **and** press enter **then** wait 2 seconds **then** press control n **and** type hello world exclamation mark"

- Although Google Assistant will sometimes properly insert punctuation in your speech, you must say "mark" or "sign" after punctuation.  For example...

  "typing colon **sign** open parentheses **sign** words closed parentheses **mark**" -> "Typing : ( words )"

- You can delay commands by saying a wait phrase along with your command. For example...
  - **wait 10 minutes** *then* type still working on it and hit send
  - press alt f4 **in 5 minutes**

### Typing

To type out inputs, either use the `-v` flag at the command-line or start your command with the word `type`. Punctuation marks and new lines are supported. Additionally, inputs are roughly sentence formatted. For example...

- "a phrase of your choice comma sign with punctuation exclamation mark" -> "A phrase of your choice , with punctuation !"
- "type i'll  be there at 6 pm period mark send" -> "I'll be there at 6 pm ." (Enter will be pressed afterwards)

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

- mute
- volume up / down / specific number
- play
- pause
- next
- previous
- full screen (compatible for toggling full screen on most players)

### Literal

- alt tab [five times]
- alt space n
- shift r
- etc.
- ❌ control alt delete <- is a protected key combination so it is NOT supported

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

## Caveats, acknowledgements, and known bugs to fix

- [ ] *An internet connection is required for your computer to receive commands.*
- [ ] *You must be logged into your computer for most, if not all, actions to succeed.*
- [ ] A digital assistant's attention span is short. So, commands must be swift and to the point.
  - [ ] As such, performing multiple or complex actions utilizing this project may prove difficult. To alleviates this pressure, the Alexa method introduced a follow-up mode.
- [ ] Giving literal key-press commands can be tricky to near impossible as it is wholly dependent on what the digital assistant *thinks* it heard. With their tendency to listen for natural spoken language, they can mishear. For example, it may hear "end" when you say "n". This project attempts to mitigate misheard literal key-press commands with an equivalency dictionary, but it isn't perfect.
- [ ] Log file location may differ depending on whether the script is executed from the console[^6] or by Push2Run.

## FREE? Really?

Basically yes! Unless possibly if you're a super user. The following are what's currently known about the Free capacity of each service/software in regard to the scope of this project.

  | Software / Service | Details|
  |--------------------|--------|
  |Amazon Alexa        | No known limitations |
  |PC Commander        | Free 150 pushes a month.[^7] <br>Subject to change, soon. Subscribe now to be grandfathered in!! |
  |Google Assistant    | No known limitations |
  |IFTTT               | Free account limited to two (2) static applets |
  |Pushbullet          | Free 500 API calls (ie. pushes) a month |
  |Push2Run            | Free |
  |Python              | Free |
  |Speech2Input        | Free |

## Footnotes

[^1]: Aside from a Windows PC and a device with smart home assistant, of course.  These devices are ubiquitous but I recognize accessibility to these devices is not universal.
[^2]: Currently, audial responses are only used to confirm volume adjustments and to inform the user when a command was not understood.
[^3]: Fucking stupid name for it.
[^4]: You can list multiple "Listen for" phrases.  Be sparing here as the more variability you add, the greater your chances of stepping on another card's toes, leading to unexpected results.
[^5]: By default, Push2Run also uses "and" and "then" as a delimiter to separate commands.  Given that the setting may interfere with this project's command-stringing function, you may find it useful to remove or change the delimiters in Push2Run's settings: File > Options > Separating words.
[^6]: The log file will be saved at the path of the process which executed the python script.
[^7]: Subject to Pushbullet API call limit. That is, PC Commander doesn't grant you additional pushes and must adhere to the limits specified by Pushbullet.