# This "script" will interpret a string into windows keyboard input; hotkey commands and/or verbatim text typing.
# It was designed with Google assistant output as the string provider in mind.
# Data chain:
# User's voice > Google Assistant > IFTTT (Tell my computer to... Pushbullet Version) > PushBullet > Push2Run > this script
# Direct key dictation (ex. "windows r") via google assistant is unreliable as it often misinterprests ("ex. windows are")
# Thus althought it's somwhat capable, this is designed more to interpret colloquial english commands rather than execute spoken key commands (Ex. "minimize" rather than "alt space n")

from sys import exit, argv
import random, re
from difflib import get_close_matches
from keypress_functions import sleep
import keypress_functions as kf
import dee_logging as dl # logging functions
from os import system # for the _speak function
import subprocess # replacing os.system for the _speak function

# Set this "dbug" variable to 1 to see console output (when run from a CLI).  Set it to 0 to silence superfluous output.
dbug = 1 #(True) or 0 (False)
# This variable sets the minimum logging level. Options: NOTSET, DEBUG, INFO, WARNING, ERROR, or CRITICAL.  NOTSET being the most verbose.
# All log levels "above" the set level will also show.  Ex. If set to INFO, WARNING logs will also show.
logging_level = dl.logging.INFO
# This variable is just for testing purposing, skipping the data hand-off chain.  Set to None for the script to ignore it.
testing_values = None # "change programs then type ABC and change programs and minimize" # <-- Test input
# This variable adjusts the acceptable threshold within the mechanism I use to make my best interpretation guess as a last resort.
# Any guess below this value won't be executed.
# 0.54 seems to be the sweet spot
guess_confidence_threshold = 0.54 # range:0 ~ 1.
# Variable is here to prevent from spamming the console for each dbugprint() call in case of logging failure.
logging_failed = False

def dbugprint(string="", logging_level="DEBUG", end="\n"):
    """ Prints to console as well as logs to logfile. """
    try: dl.log(string, logging_level)
    except:
        # Apparently when I change the variable to True a few lines down, it changes the scope of the variable from global to just this function
        # So I need this "global" here to explicitely tell python to not do that.  Why?  I dunno (yet).
        # Thanks to this site for the exlanation.
        # https://pythoncircle.com/post/680/solving-python-error-unboundlocalerror-local-variable-x-referenced-before-assignment/
        global logging_failed
        if not logging_failed:
            print("ERROR: Logging function failure.")
            logging_failed = True # This "re-assignment" was giving me trouble and making the if statement at the top of this block fail.
        None # logging is not strictly necessary so I've elected to do nothing if it fails
    if dbug: print(string, end=end)

##########################
### Setting up Logging ###
##########################
try:
    dl.configureLogging(logFilePath=dl.path.dirname(__file__) + '\\' + __file__.split("\\")[-1].split(".")[0] +'.log', logLevel=logging_level)
except:
    try:
        dbugprint("Failed creating localized log.  Attempting to create one in user's temp folder.")
        import tempfile
        dl.configureLogging(logFilePath=tempfile.gettempdir() + '\\' + __file__.split("\\")[-1].split(".")[0] +'.log', logLevel=logging_level)
    except:
        print("Unable to create/write log file.  Logging will be disabled.")

WORDS = []
commandKeys = {
    "alt"    : kf.Key.alt,
    "all"    : kf.Key.alt,
    "out"    : kf.Key.alt,
    "ctrl"   : kf.Key.ctrl,
    "control": kf.Key.ctrl,
    "shift"  : kf.Key.shift,
    "start"     : kf.Key.cmd,
    "startmenu" : kf.Key.cmd,
    "start menu": kf.Key.cmd,
    "windows"   : kf.Key.cmd,
    "caps"      : kf.Key.caps_lock,
    "caps lock" : kf.Key.caps_lock,
}
SpecialKeys = {
    "escape"      : kf.Key.esc,
    "space"       : kf.Key.space,
    "spacebar"    : kf.Key.space,
    "space bar"   : kf.Key.space,
    "del"         : kf.Key.delete,
    "delete"      : kf.Key.delete,
    "enter"       : kf.Key.enter,
    "return"      : kf.Key.enter,
    "new line"    : kf.Key.enter,
    "next line"   : kf.Key.enter,
    "mute"        : kf.Key.media_volume_mute,
    "number lock" : kf.Key.num_lock,
    "home"        : kf.Key.home,
    "end"         : kf.Key.end,
    "page down"   : kf.Key.page_down,
    "page up"     : kf.Key.page_up,
    "print screen": kf.Key.print_screen,
    "scroll lock" : kf.Key.scroll_lock,
    "mute"        : kf.Key.media_volume_mute,
    "right click" : kf.Key.menu, # doesn't quite fit in this dict but it hahs to go somewhere
}
# joining both dicts and sorting first by number of words, then by word length if previous condition is same
sortedSpecialKeys = sorted({**commandKeys, **SpecialKeys}, key=lambda x: (len(x.split()), len(x)), reverse=True)
possibleSingleLetterMisinterpretations = {
    "be"  : 'b',
    "bee" : 'b',
    "sea" : 'c',
    "see" : 'c',
    "de"  : 'd',
    "dee" : 'd',
    "ghee": 'g',
    "jay" : 'j',
    "jeep": 'j',
    "kay" : 'k',
    "kae" : 'k',
    "oh"  : 'o',
    "pee" : 'p',
    "are" : 'r',
    "run" : 'r',
    "tee" : 't',
    "yu"  : 'u',
    "you" : 'u',
    "why" : 'y',
    "zero" : "0",
    "one"  : "1",
    "two"  : "2",
    "three": "3",
    "four" : "4",
    "five" : "5",
    "six"  : "6",
    "seven": "7",
    "eight": "8",
    "nine" : "9",
}
mark_signs = {
    "tilda"   : '~',
    "at"      : '@',
    "hashtag" : '#',
    "dollar"  : '$',
    "percent" : '%',
    "hat"     : '^',
    "and"     : '&',
    "star"    : '*',
    "asterisk": '*',
    "open parentheses" : "(",
    "close parentheses": ")",
    "dash"         : '-',
    "minus"        : '-',
    "underscore"   : '_',
    "plus"         : '+',
    "equal"        : '=',
    "equals"       : '=',
    "open bracket" : '[',
    "close bracket": ']',
    "open curly bracket" : '{',
    "close curly bracket": '}',
    "slash"        : '/',
    "pipe"         : '|',
    "colon"        : ':',
    "semicolon"    : ';',
    "quote"        : '"',
    "single quote" : '\'',
    "less than"    : '<',
    "greater than" : '>',
    "forward slash": '/',
    "back slash"   : '\\',
    "backslash"    : '\\',
    "period"       : '.',
    "exclamation"  : '!',
    "comma"  : ','
}
sorted_mark_signs = sorted(mark_signs, key=lambda x: (len(x.split()), len(x)), reverse=True)
execute = {
    "move"         : kf.do_move,
    "resize"       : kf.do_resize,
    "resize left"  : kf.do_resize_left,
    "resize right" : kf.do_resize_right,
    "resize top"   : kf.do_resize_top,
    "resize bottom": kf.do_resize_bottom,
    "minimize"     : kf.do_minimize,
    "maximize"     : kf.do_maximize,
    "restore"      : kf.do_restore,
    "dock left"    : kf.do_dock_left,
    "dock right"   : kf.do_dock_right,
    "change application n": kf.do_alt_tab,
    "select application"  : kf.do_change_app,
    "exit application"    : kf.do_exit_app,
    "switch application to x" : kf.do_switch_app_to,
    "new tab"       : kf.do_new_tab,
    "new window"    : kf.do_new_window,
    "close tab"     : kf.do_close_tab,
    "change tab n"  : kf.do_change_tab,
    "go to website" : kf.do_go_to,
    "refresh"       : kf.do_refresh,
    "go back"       : kf.do_go_back,
    "go forward"    : kf.do_go_forward,
    "reopen tab"    : kf.do_reopen_tab,
    "select all"  : kf.do_select_all,
    "cut"         : kf.do_cut,
    "copy"        : kf.do_copy,
    "paste"       : kf.do_paste,
    "undo"        : kf.do_undo,
    "redo"        : kf.do_redo,
    "home"        : kf.do_home,
    "end"         : kf.do_end,
    "page up n"   : kf.do_page_up,
    "page down n" : kf.do_page_down,
    "save"        : kf.do_save,
    "save as"     : kf.do_save_as,
    "emoji"       : kf.do_emoji,
    "minimize all"                    : kf.do_minimize_all,
    "minimize everything else"        : kf.do_minimize_everything_else,
    "run prompt"                      : kf.do_run_prompt,
    "task manager"                    : kf.do_task_manager,
    "change language"                 : kf.do_change_input_lang,
    "change language back"            : kf.do_change_input_lang_back,
    "change language to English"      : kf.do_change_intput_lang_to_EN,
    "change language to Japanese"     : kf.do_change_intput_lang_to_JP,
    "show notification"               : kf.do_show_notification,
    "show time and calendar"          : kf.do_show_time_and_calendar,
    "dictation"                       : kf.do_start_dictation,
    "show settings"                   : kf.do_show_settings,
    "take screen snippet"             : kf.do_take_screen_snippet,
    "take screenshot"                 : kf.do_take_screenshot,
    "save screenshot"                 : kf.do_save_screenshot,
    "save screenshot of active window": kf.do_save_screenshot_of_active_window,
    "open system menu"                : kf.do_open_system_menu,
    "control panel"                   : kf.do_open_control_panel,
    "play"       : kf.do_press_spacebar,
    "pause"      : kf.do_press_spacebar,
    "fullscreen" : kf.do_press_F,
}
synonyms = {
    # exact equivalents
    #"alt tab": "change application", # gonna try to leave this for the isLiteralKeyCommands() method
    "scroll down": "page down",
    "scroll"     : "page down",
    "scroll up"  : "page up",
    #"windows run": "run prompt", # gonna try to leave this for the isLiteralKeyCommands() method
    "full screen": "maximize",
    "fullscreen" : "maximize",
    "fill screen": "maximize",
    "box if i": "restore",
    "box 5"   : "restore",
    "boxify"  : "restore",
    "close program": "exit application",
    # just starting to guess now
    "switch" : "change",
    "quit"   : "exit",
    "desktop": "minimize all",
    "run"    : "run prompt",
    "window" : "application",
    "program": "application",
    "put it on the": "dock",
    "tile"         : "dock",
}

# Exit if no arguments.  Unless testing_value exists...
if len(argv) == 1:
    if not testing_values:
        dbugprint("Didn't recieve anything to type.", logging_level="ERROR")
        exit(1)
    dbugprint("****Using test values****", logging_level="INFO")

class Command:
    #data members of class
    name = ""         #attribute 1
    confidence = 0.0  #attribute 2
    #class default constructor
    def __init__(self,name,confidence):
        self.name = name
        self.confidence = confidence
    #user defined example function of class
    def func(self):
        print(f"Command is ['{self.name}']")
        print(f"Confidence is {self.getConfidence()}")
    def isGoodEnough(self):
        return self.confidence > guess_confidence_threshold
    def getConfidence(self):
        return f"{self.confidence *100}%"
    def __str__(self):
        return f"('{self.name}', {self.confidence})"
    def __repr__(self):
        # This is what prints when printing a list of these. Ex. print(str(commands[]))
        return f"('{self.name}', {self.confidence})"
    # How to instantiate.
    #cmd1 = Command('alt tab', 0)

def canBeSingleChar(x):
    # intended to indicate whether x can either be a single character (ex. 'r') or a mis-recognized word which may have been intended to be a letter (ex. "are")
    singleChar = len(x) == 1 and isinstance(x, str)
    potentialSingleLetter = x in possibleSingleLetterMisinterpretations
    punctuation_mark = x in mark_signs
    return singleChar or potentialSingleLetter or punctuation_mark

def getSingleChar(x):
    if len(x) == 1 and isinstance(x, str):
        return x
    if x in possibleSingleLetterMisinterpretations:
        return possibleSingleLetterMisinterpretations[x]
    if x in mark_signs:
        return mark_signs[x]
    raise ValueError(f"\"{x}\" is not a single letter or a known homophone.")

def isCommandKey(input):
    # for indicating whether a word represents a key which can be pressed with others (ex. "shift")
    try:
        if isinstance(input, kf.Key):
            return input in commandKeys.values()
        commandKeys[input]
        return True
    except:
        None
    return False

def isSpecialKey(input):
    # intended to indicate whether a word represents a Key object (ex. 'windows', 'control', 'a')
    # So I realize this used a bunch of repeated code so I'll just refer to the already existing (and updated) code
    try:
        if getSpecialKey(input):
            return True
    except:
        None
    return False

def getSpecialKey(input):
    if isinstance(input, kf.Key):
        return input
    # else... Converts a text key representation to a Key object for pressing.  Yes, single characters count, too.
    try:
        return commandKeys[input]
    except:
        None
    
    try:
        return SpecialKeys[input]
    except:
        None
    
    try:
        return kf.Key[input]
    except:
        None
    
    try:
        if canBeSingleChar(input):
            return getSingleChar(input)
    except:
        None
    
    raise ValueError("No such special key '" + input + "' found")

def getLiteralKeyCommands(string):
    # checks if a string of words represent a combination of single key inputs *starting with a command key (ex. "control shift escape")
    dbugprint(f"Attempting to understand as literal key(s): {string}", logging_level="INFO")
    string = string.lower()
    if string.startswith("press ") or string.startswith("hit "):
        string = ' '.join(string.split()[1:])
    def extractFirstSpecialKeyPhrase(words):
        # I don't know what I'm doing here.  Trying to make something recursive but I can't imagine how this will work.  Good luck following the logic.  lol
        if not words:
            return False
        for key_word in sortedSpecialKeys + sorted_mark_signs:
            if words.startswith(key_word):
                return key_word
        # for single letter case
        first_word_or_letter = words.split(" ", 1)[0]
        if canBeSingleChar(first_word_or_letter) or isSpecialKey(first_word_or_letter):
            return first_word_or_letter
        return False
    literal_keys = []
    i = 0
    while string:
        key = extractFirstSpecialKeyPhrase(string)
        if not key:
            dbugprint("Failed literal check.")
            return False
        string = string.replace(key, "", 1).lstrip()
        if i == 0 and string and not isCommandKey(key):
            dbugprint(f"'{key}' fails command key check.")
            return False
        key = getSpecialKey(key)
        literal_keys.append(key)
        dbugprint(f"Added ", end="")
        if isCommandKey(key): dbugprint(f"command ", end="")
        else:                 dbugprint(f"regular ", end="")
        dbugprint(f"key: [{key}]", end="")
        i += 1
        if string:
            dbugprint(f"  |  Remaining string: '{string}'")
        else:
            dbugprint()
    #dbugprint("Keys collected: " + str(literal_keys))
    return literal_keys

def swap_in_symbols(string):
    # a jumble of logic that ultimately swaps in symbols for text representing them.  Ex "here's a percent sign sign" -> "here's a % sign"
    for signifier in ["mark", "sign"]:
        for symbol in mark_signs:
            symbol_phrase = f"{symbol} {signifier}"
            if re.search(symbol_phrase, string, flags=re.IGNORECASE):
                insensitive_hippo = re.compile(re.escape(symbol_phrase), re.IGNORECASE)
                string = insensitive_hippo.sub(mark_signs[symbol], string)
            # Taking into account that user might've said "open" or "close" in past-tense, checking for symbol phrases in past-tense
            # if symbol starts with 'open' or 'close' AND (ingoring case) the string also contains 'open' or 'close', and the next word in the symbol (ex. 'bracket'):
            # forehead slap on g-assistant mishearing "closed" as "clothes"
            if re.search("^open|^close", symbol) and re.search(r"\bopened|\bclosed|\bclothes", string, flags=re.IGNORECASE) and string.count(symbol.split()[1]):
                # make past-tense version
                pt_symbol_phrase = symbol_phrase.replace("open", "opened").replace("close", "closed")
                # gotta make a stupid "clothes" case since it can sound like "close"
                if symbol.startswith("close") and string.count("clothes"):
                    dumb_clothes_possibility = f"clothes {' '.join(symbol_phrase.split()[1:])}"
                    #dbugprint("dumb_clothes_possibility is: " + dumb_clothes_possibility) # done debugging
                    if string.count(dumb_clothes_possibility):
                        #dbugprint(f"swapping dumb clothes possibilty with {mark_signs[symbol]}") # done debugging
                        insensitive_hippo = re.compile(re.escape(dumb_clothes_possibility), re.IGNORECASE)
                        string = insensitive_hippo.sub(mark_signs[symbol], string)
                if re.search(pt_symbol_phrase, string, flags=re.IGNORECASE):
                    #dbugprint('found pt_symbol_phrase "' + pt_symbol_phrase + '"  Swapping in ' + mark_signs[symbol]) # done debugging
                    insensitive_hippo = re.compile(re.escape(pt_symbol_phrase), re.IGNORECASE)
                    string = insensitive_hippo.sub(mark_signs[symbol], string)
    return string

def toSentence(string):
    # This is to correct the format of the string google assistant will send.
    # Ex. "he said don ' t do a girl ' s job !" --toSentence()--> "He said don't do a girl's job!"
    def upper_initial(string):
        # as far as I can tell, the if/else at the end is in case string is '' to avoid trying to process empty strings
        return string[0].upper() + string[1:] if string else string
    # removing spaces before punctuation (ex. "hello , you ." -> "hello, you."), and capitalizes first letter in each sentence
    for p in ['!', '?', '.']:
        string = f"{p} ".join(upper_initial(s.strip()) for s in string.split(f" {p}") )
    # removing spaces between appropriate apostrophe
    # Swapping this FOR loop with re.sub() one-line
    #for p in ['s','S','t','T','d','D','ll','LL']:
    #    string = string.replace(f" ' {p} ", f"'{p} ")
    # a little side note. the main difference is this will remove the spaces around a ' for a single "l", where-as the FOR loop will do it only for a double "ll"
    string = re.sub(r"\s'\s+([sStTdDlLmM])", r"'\1", string)
    # Swapping this .replace() with re.sub() one-line
    #return string.replace(' ,',',')
    # removes spaces before any punctuation.  This works better than above (one-liner) but has added benefit or also removing spaces between repeated punctuation
    # Ex. "hi . . ." -> "hi..." Whereas above FOR loop would do "hi. . ." 
    string = re.sub(r'\s+([,?.!"])', r'\1', string)
    # self-explanatory. Ex "here's a percent sign sign" -> "here's a % sign"
    string = swap_in_symbols(string)
    # capitalizing all instances of i'm, i'll, etc.
    string = string.replace("i'", "I'")
    return string

def typeSentences(string):
    # Types out inputted string, taking care to not include any known return language at the end.  Ex. "The brown fox. Enter"
    single_word_return_keywords = ['enter','return','send']
    dual_word_return_keywords   = ['new line', 'next line', 'hit return', 'hit enter']
    last_word_means_Enter      =            string.split()[-1].lower() in single_word_return_keywords
    last_two_words_means_Enter = ' '.join(string.split()[-2:]).lower() in dual_word_return_keywords
    hit_Enter_after_typing = last_word_means_Enter or last_two_words_means_Enter
    if hit_Enter_after_typing:
        if last_two_words_means_Enter:
            dbugprint("removing last two words and hitting ENTER")
            string = '' if string.lower() in dual_word_return_keywords else string.rsplit(' ',2)[0]
        else:
            dbugprint("removing last word and hitting ENTER")
            string = '' if string.lower() in single_word_return_keywords else string.rsplit(' ',1)[0]
    for char in string:
        kf.tap(char)
        random_sleep_time_in_s = random.uniform(0.0, 0.01)
        sleep(random_sleep_time_in_s)
    if hit_Enter_after_typing:
        kf.tap(kf.Key.enter)

def pressLiteralKeys(keys, n=0):
    dbugprint(f"Pressing ", end="")
    pressed_keys = []
    for key in keys:
        if isCommandKey(key):
            dbugprint(f"[{key}]", end=" ")
            kf.kb.press(key)
            pressed_keys.append(key)
        else:
            # press and release all keys
            if pressed_keys:
                dbugprint(f"and tapping", end=" ")
            else:
                dbugprint(f"Tapping", end=" ")
            k_times = f"[{key}]"
            if n > 1:
                k_times = k_times + f" {n} times"
            dbugprint(k_times)
            for x in range(n):
                sleep(2 * kf.multiple_key_tap_delay)
                kf.tap(key)
    if pressed_keys:
        dbugprint(f"Releasing ", end="")
    while pressed_keys:
        key = pressed_keys.pop(0)
        dbugprint(f"[{key}]", end=" ")
        kf.kb.release(key)
        if not pressed_keys:
            dbugprint()
    sleep(2 * kf.multiple_key_tap_delay)

def swap_in_synonyms(string):
    # exception to synonym swapping
    # I honestly don't remember why I put in this exception.  Likely to prevent annoying behavior.
    if string.count("window") and (string.count("new") or string.count("screenshot")):
        dbugprint('Exception!  NOT swapping "window" or other words in command. Moving onto next command.')
        return string
    # substituting synonyms
    for item in synonyms:
        if string.count(item):
            dbugprint('Swapping "' + item + '" with synonym "' + synonyms[item] + '"')
            string = string.replace(item, synonyms[item])
    return string

def remove_symbols(command):
    return re.sub('\s?[!-/]|\s?[\[-`]', '', command).lstrip()

def get_best_guess_and_confidence(command):
    dbugprint(f"Figuring best guess for \"{command}\"", logging_level="INFO")
    confidence = 0
    best_guess = command
    tuple = (best_guess, confidence)
    output = Command(command, confidence)
    samples = 50
    while best_guess:
        for x in range(1, samples + 1):
            confidence = x / samples
            confidence_percentage = f"{int(confidence * 100)}%"
            best_guess = get_close_matches(command, execute.keys(), cutoff=confidence)
            if not best_guess:
                #dbugprint(f"No good guess at confidence {confidence_percentage}")
                break
            #dbugprint(f"Best guess(es) at {confidence_percentage} = " + str(best_guess))
            tuple = (best_guess[0], confidence)
            output = Command(best_guess[0], confidence)
        best_guess = None
    dbugprint(f"{int(output.confidence * 100)}% confident \"{command}\" means ['{output.name}']")
    return output

def split_phrase_into_command_list(phrase):
    commands = []
    for command in re.split(" and | ?then | ?than ", phrase): # the spaces I added here are important, including the ' ?' which is necessary when someone says "and then"
        commands.append(command.strip())
    # checking for and splitting (ie. forming and inserting a new command) on keywords indicating keyboard input is desired
    for i in range(len(commands)):
        for delimeter in ['type ', 'input ', 'hit enter']:
            parts = commands[i].partition(delimeter)
            if not all([parts[0], parts[1]]):
                continue
            del commands[i]
            commands.insert(i, ''.join(parts[1:]))
            commands.insert(i,parts[0].rstrip())
    return commands

numbers_dict = {
    'zero' : 0,
    'one'  : 1,
    'two'  : 2,
    'to'   : 2,
    'too'  : 2,
    'three': 3,
    'four' : 4,
    'five' : 5,
    'six'  : 6,
    'sex'  : 6,
    'seven': 7,
    'eight': 8,
    'nine' : 9,
    'ten'  : 10
}

frequency_phrases = {
    "twice" : "2 times",
    "thrice": "3 times",
}

def inferNumber(string):
    # converts a string representation of a number to an int (ex. "five" -> 5)
    try:
        return int(string)
    except:
        None
    try:
        return numbers_dict.get(string, False)
    except:
        return False

def findMultiplierString(string):
    # returns tuple (multiplier_string, n) or False
    # need to account for times user may say "twice" or maybe even "thrice"
    multiplier_string = None # This needs to be initiated here or Python will complain at "if not multiplier_string".  PowerShell wouldn't...
    for phrase in frequency_phrases:
        if string.count(phrase):
            string = string.replace(phrase, frequency_phrases[phrase])
            # storing the unique phrase for later when returning tuple so next function can properly remove it from the command
            # (ex. ie. it'll properly removes "twice" from "page down twice", instead of trying to remove "2 times")
            multiplier_string = phrase
            # no need to continue the FOR loop if it already found one.
            # Yes, if someone said "twice" and "thrice" it'll only catch one but that's more a user error case than something I should account for.
            break
    # Looking for the keyword that indicates a multiplier phrase
    # Edit: Instead of adding 'X' to the list, I added the IGNORECASE flag.  I'm not expecting bugs but I'm taking note of this change here in case it does cause bugs.
    for times in ['\*', 'x', 'times']:
        found = re.search(f"(\w+) +{times}", string, flags=re.IGNORECASE)
        if found:
            n = inferNumber(found.group(1))
            if n:
                if not multiplier_string:
                    multiplier_string = found.group()
                return (multiplier_string, n)
    return False

def getMultiplierFactor(string):
    # returns tuple (command_wOut_multiplier_string, n) or False
    multiplier_tuple = findMultiplierString(string) # returns (multiplier_string, n) or False
    if not multiplier_tuple:
        return False
    multiplier_string = multiplier_tuple[0]
    n = multiplier_tuple[1]
    command_wOut_multiplier_string = string.replace(multiplier_string, "").strip()
    # Removing double white space in case the multiplier string was not at the far left or right of the string
    while command_wOut_multiplier_string.count("  "): #2 spaces
        command_wOut_multiplier_string = command_wOut_multiplier_string.replace("  ", " ")
    return (command_wOut_multiplier_string, n)

def _speak(string):
    # Cannot try/except with os.system() to detect whether app exists or not
    # Swapping for subprocess method for which that kind of check works
    #system(f'nircmd.exe speak text "{string}"')
    try:
        subprocess.run(f'nircmd.exe speak text "{string}"', check=True)
    except (OSError, subprocess.SubprocessError, subprocess.CalledProcessError):
        dbugprint("Speak application (nircmd) may not exist.  Is it installed?", logging_level="ERROR")
    except:
        dbugprint("Speak application (nircmd) failed.", logging_level="ERROR")

def lastDitchAttemptToInterpret(command, n=1):
    command_possibilities = [Command(command, 0)]
    # see if I can make sense of command as is, without synonym swapping for improved comprehension
    command_possibilities.insert(0, get_best_guess_and_confidence(command))

    if command_possibilities[0].confidence == 1:
        dbugprint("Can't get any better than that 100% confidence!!!")
    else:
        # re-format command language for hopefully better guess using get_close_matches()
        # substituting common synonyms to improve comprehension of alternative command expressions
        command_w_synonyms = swap_in_synonyms(command)

        if command == command_w_synonyms:
            dbugprint("No difference after synonym swap.")
        else:
            dbugprint("After synonym swap... ", end="")
            command_possibilities.append(get_best_guess_and_confidence(command_w_synonyms))
    
        # sort the possibilites by confidence and pick out the most confident interpretation
        command_possibilities = sorted(command_possibilities, key=lambda x: x.confidence, reverse=True)
        dbugprint("command possibilities sorted by confidence  : " + str(command_possibilities))

    best_command_candidate = command_possibilities[0]
    
    if best_command_candidate.name == 'exit application' and best_command_candidate.confidence < 0.78:
        safe_alternative = "minimize"
        dbugprint(f"!!! Replacing ['{best_command_candidate.name}'] command with [{safe_alternative}] until I can be more than 78% confident")
        best_command_candidate = Command(safe_alternative, 100)
    if not best_command_candidate.isGoodEnough():
        dbugprint(f"Canceling at ['{best_command_candidate.name}'] command until I can be more confident than {best_command_candidate.getConfidence()}")
        _speak(f"Sorry.  I didn't understand your command, {command_possibilities[-1].name}.")
        return
    dbugprint(f"Executing: ['{best_command_candidate.name}']", logging_level="INFO")
    if best_command_candidate.name.endswith(" n"):
        execute[best_command_candidate.name](n)
    else:
        for _ in range(n):
            execute[best_command_candidate.name]()
    return best_command_candidate

time_conversions_to_s_from = {
    "microseconds" : lambda x: x / 1_000_000,
    "milliseconds" : lambda x: x / 1_000,
    "seconds"      : lambda x: x,
    "minutes"      : lambda x: x * 60,
    'hours'        : lambda x: x * 60 * 60,
    "days"         : lambda x: x * 60 * 60 * 24
}

def convertToSeconds(t=1, unit="seconds"):
    if not unit.endswith('s'):
        unit = unit + 's'
    try:
        return time_conversions_to_s_from[unit](t)
    except:
        dbugprint("convertToSeconds FAILED. Returning 1 second.", logging_level="ERROR")
        return 1

def main():
    WORDS = argv[1:]
    if testing_values:
        WORDS = testing_values
    # standardizing input: concatenate args into one strings. Designed to receive command(s) either divided into arguments or a single string argument
    phrase = ' '.join(WORDS)
    dbugprint(f"*** | on {dl.getHostname()} | *********************************************************", logging_level="INFO")
    dbugprint("Received: " + phrase)

    #######################
    ### TYPING VERBATIM ###
    #######################
    if WORDS[0] in ['-v','-verbatim']:
        # Will format string in sentence format and type it out one char at a time.
        phrase = ' '.join(WORDS[1:])
        dbugprint("Typing verbatim.  No command interpretation.\n", logging_level="INFO")
        typeSentences( toSentence(toSentence(phrase)) ) # meh.  Better than tinkering wondering why punctuation wasn't being treated nice
        return

    ########################################
    ### INTERPRETTING TEXT INTO COMMANDS ###
    ########################################
    # splitting on conjunction words to seperate commands
    commands = split_phrase_into_command_list(phrase)
    action_multiplier = [1] * len(commands)

    dbugprint("Raw commands: " + str(commands), logging_level="INFO")
    
    for i in range(len(commands)):
        command = commands[i]
        if not command:
            continue

        dbugprint("==============================")

        # FIRST, check for a sleep command
        t = unit = None
        sleep_command = re.search(r'^(?:wait|sleep|hold)(?: for)? (\w+) ?(microsecond|millisecond|second|minute|hour|day)?s?$', command)
        if sleep_command:
            t = inferNumber(sleep_command.group(1))
            unit  = sleep_command.group(2)
        
        delay_command = re.search(r'^(.*) in (\d+) ?(microsecond|millisecond|second|minute|hour|day)?s?$', command)
        if delay_command:
            command = delay_command.group(1)
            t   = int(delay_command.group(2))
            unit    = delay_command.group(3)
        
        if all([t, unit]):
            dbugprint(f'Waiting for {t} {unit}(s)...', logging_level="INFO")
            sleep(convertToSeconds(t, unit))
            if sleep_command:
                continue

        # SECOND, type out text if command begins with any of these key words
        if re.search("^type|^input|^hit enter", command):
            dbugprint(f'Text input keyword detected! Typing out text within command "{command}"', logging_level="INFO")
            typeSentences( toSentence(command.split(' ', 1)[1]) )
            continue
        
        # THIRD, check for Go To command
        go_to_command = re.search(r'(navigate|go) to (.*)', command) # captures a url or some path
        if go_to_command:
            site = go_to_command.group(2).replace(' ', '')
            dbugprint(f"Going to... {site}")
            commands[i] = f"{go_to_command.group(1)} to {site}"
            execute["go to website"](site)
            continue

        multiplier_tuple = getMultiplierFactor(command) # returns tuple (command_wOut_multiplier_string, n) or False
        if multiplier_tuple:
            command = multiplier_tuple[0] 
            action_multiplier[i] = multiplier_tuple[1]
            commands[i] = multiplier_tuple # Maybe don't?

        # FIXME: Currently doesn't work I'm supposing if the calling window is not active (like how I currently have it implemented in Push2Run)
        switch_to_app = re.search(r'^(?:swap|switch|change) (?:app|application|program)?(?:s | )?(?:to )?(.*)', command)
        if switch_to_app:
            _app = switch_to_app.group(1)
            if _app:
                dbugprint(f"Attempting to make '{_app}' the active window.", logging_level="INFO")
                execute["switch application to x"](_app)
                continue
        
        # removes these chars [! " # $ % & ' ( ) * + , - . / Z [ \ ] ^ _ `] and any white space on the left if present as they're unnecessary for commands
        # Ex. 'alt - tab' -> 'alt tab'
        # This may remove intended characters, losing information but that will have to be seen
        command = remove_symbols(command)


        # FOURTH, see if I can make sense of the command as a literal key invocations (Ex. "windows run")
        literal_keys = getLiteralKeyCommands(command)
        if literal_keys:
            commands[i] = ', '.join(x if isinstance(x, str) else x.name for x in literal_keys)
            dbugprint(f"Executing: {literal_keys}", logging_level="INFO")
            pressLiteralKeys(literal_keys, action_multiplier[i])
            continue
        
        # FIFTH and lastly, if command failed literal translation, try best guess interpretation
        # also re-inserting newly formatted best guess command back into commands[] array for final debugging output
        commands[i] = lastDitchAttemptToInterpret(command, action_multiplier[i])
    
    dbugprint("==============================")
    # Post-execution command interpretation summarization
    dbugprint("Commands interpreted as:  " + str(commands) + "\n")

    return

if __name__ == "__main__":
    main()