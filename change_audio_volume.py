from sys import exit, argv
from os import system
import re
import dee_logging as dl

debugging_on = True
VOL_MAX = 65535
testing_values = None # "raise the volume by 10 percent"
dl.configureLogging(logFilePath=dl.path.dirname(__file__) + '\\' + __file__.split("\\")[-1].split(".")[0] +'.log', logLevel=dl.logging.INFO)

def dbugprint(string="", end="\n", logging_level="DEBUG"):
    dl.log(string, logging_level)
    if debugging_on: print(string, end=end)

if len(argv) == 1:
    if not testing_values:
        print("Usage: python " + __file__.split("\\")[-1] + " \"raise volume\"")
        exit(1)
    dbugprint("****Using test values****", logging_level="INFO")

NUMBERS = {
    'zero'          : 0,
    'one'           : 1,
    'two'           : 2,
    'three'         : 3,
    'four'          : 4,
    'five'          : 5,
    'six'           : 6,
    'seven'         : 7,
    'eight'         : 8,
    'nine'          : 9,
    'ten'           : 10,
    'eleven'        : 11,
    'twelve'        : 12,
    'thirteen'      : 13,
    'fourteen'      : 14,
    'fifteen'       : 15,
    'sixteen'       : 16,
    'seventeen'     : 17,
    'eighteen'      : 18,
    'nineteen'      : 19,
    'twenty'        : 20,
    'twenty-one'    : 21,
    'twenty-two'    : 22,
    'twenty-three'  : 23,
    'twenty-four'   : 24,
    'twenty-five'   : 25,
    'twenty-six'    : 26,
    'twenty-seven'  : 27,
    'twenty-eight'  : 28,
    'twenty-nine'   : 29,
    'thirty'        : 30,
    'thirty-one'    : 31,
    'thirty-two'    : 32,
    'thirty-three'  : 33,
    'thirty-four'   : 34,
    'thirty-five'   : 35,
    'thirty-six'    : 36,
    'thirty-seven'  : 37,
    'thirty-eight'  : 38,
    'thirty-nine'   : 39,
    'forty'         : 40,
    'forty-one'     : 41,
    'forty-two'     : 42,
    'forty-three'   : 43,
    'forty-four'    : 44,
    'forty-five'    : 45,
    'forty-six'     : 46,
    'forty-seven'   : 47,
    'forty-eight'   : 48,
    'forty-nine'    : 49,
    'fifty'         : 50,
    'fifty-one'     : 51,
    'fifty-two'     : 52,
    'fifty-three'   : 53,
    'fifty-four'    : 54,
    'fifty-five'    : 55,
    'fifty-six'     : 56,
    'fifty-seven'   : 57,
    'fifty-eight'   : 58,
    'fifty-nine'    : 59,
    'sixty'         : 60,
    'sixty-one'     : 61,
    'sixty-two'     : 62,
    'sixty-three'   : 63,
    'sixty-four'    : 64,
    'sixty-five'    : 65,
    'sixty-six'     : 66,
    'sixty-seven'   : 67,
    'sixty-eight'   : 68,
    'sixty-nine'    : 69,
    'seventy'       : 70,
    'seventy-one'   : 71,
    'seventy-two'   : 72,
    'seventy-three' : 73,
    'seventy-four'  : 74,
    'seventy-five'  : 75,
    'seventy-six'   : 76,
    'seventy-seven' : 77,
    'seventy-eight' : 78,
    'seventy-nine'  : 79,
    'eighty'        : 80,
    'eighty-one'    : 81,
    'eighty-two'    : 82,
    'eighty-three'  : 83,
    'eighty-four'   : 84,
    'eighty-five'   : 85,
    'eighty-six'    : 86,
    'eighty-seven'  : 87,
    'eighty-eight'  : 88,
    'eighty-nine'   : 89,
    'ninety'        : 90,
    'ninety-one'    : 91,
    'ninety-two'    : 92,
    'ninety-three'  : 93,
    'ninety-four'   : 94,
    'ninety-five'   : 95,
    'ninety-six'    : 96,
    'ninety-seven'  : 97,
    'ninety-eight'  : 98,
    'ninety-nine'   : 99,
    'one-hundred'   : 100
}

increase_words = ['up', 'raise', 'increase', 'plus']
decrease_words = ['down', 'lower', 'decrease', 'reduce', 'minus', 'quieter']
mute_words     = ['mute', 'off', 'quiet', 'silent', 'silence'] # the way the algorithm checks, only single words will work. ie. "shut up" won't work.
unmute_words   = ['on']

"""Not really necessary but I thought it could be useful at some point
one_to_one_hundred_list = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 
    'twenty-one', 'twenty-two', 'twenty-three', 'twenty-four', 'twenty-five', 'twenty-six', 'twenty-seven', 'twenty-eight', 'twenty-nine', 'thirty', 
    'thirty-one', 'thirty-two', 'thirty-three', 'thirty-four', 'thirty-five', 'thirty-six', 'thirty-seven', 'thirty-eight', 'thirty-nine', 'forty', 
    'forty-one', 'forty-two', 'forty-three', 'forty-four', 'forty-five', 'forty-six', 'forty-seven', 'forty-eight', 'forty-nine', 'fifty', 
    'fifty-one', 'fifty-two', 'fifty-three', 'fifty-four', 'fifty-five', 'fifty-six', 'fifty-seven', 'fifty-eight', 'fifty-nine', 'sixty', 
    'sixty-one', 'sixty-two', 'sixty-three', 'sixty-four', 'sixty-five', 'sixty-six', 'sixty-seven', 'sixty-eight', 'sixty-nine', 'seventy', 
    'seventy-one', 'seventy-two', 'seventy-three', 'seventy-four', 'seventy-five', 'seventy-six', 'seventy-seven', 'seventy-eight', 'seventy-nine', 'eighty', 
    'eighty-one', 'eighty-two', 'eighty-three', 'eighty-four', 'eighty-five', 'eighty-six', 'eighty-seven', 'eighty-eight', 'eighty-nine', 'ninety', 
    'ninety-one', 'ninety-two', 'ninety-three', 'ninety-four', 'ninety-five', 'ninety-six', 'ninety-seven', 'ninety-eight', 'ninety-nine', 'one-hundred'
    ]"""

def changeWordToNumber(string):
    try:
        return NUMBERS[string]
    except:
        return string

def _validateVolume(x):
    if x < 0 or x > 100:
        dbugprint(f"Invalid volume value: {x}", logging_level="ERROR")
        exit(2)

def _getRawVolume(x):
    return x / 100 * VOL_MAX

def _do(func, x=None):
    if x:
        _validateVolume(x)
        func(x)
        _unMute()
    else:
        func()
    exit(0)

def _unMute():
    dbugprint("Un-muting", logging_level="INFO")
    system("nircmd.exe mutesysvolume 0")

def _mute():
    dbugprint("Muting", logging_level="INFO")
    _speak("muting")
    system("nircmd.exe mutesysvolume 1")

def _toggleMute():
    dbugprint("Toggling mute", logging_level="INFO")
    system("nircmd.exe mutesysvolume 2")

def _increaseVolume(x = 9):
    dbugprint(f"Increasing volume by {x}%", logging_level="INFO")
    system(f"nircmd.exe changesysvolume {_getRawVolume(x)}")
    _speak(f"Raising volume {x}%")

def _decreaseVolume(x = 9):
    dbugprint(f"Decreasing volume by {x}%", logging_level="INFO")
    system(f"nircmd.exe changesysvolume -{_getRawVolume(x)}")
    _speak(f"Lowering volume {x}%")

def _setVolume(x):
    dbugprint(f"Setting volume to {x}%", logging_level="INFO")
    system(f"nircmd.exe setsysvolume {_getRawVolume(x)}")
    _speak(f"Setting volume to {x}")

def _speak(string):
    system(f'nircmd.exe speak text "{string}"')

def main():
    WORDS = testing_values if testing_values else argv[1:]

    # standardizing input: concatenate args into one strings. Designed to receive command(s) either divided into arguments or a single string argument
    phrase = ' '.join(WORDS)
    dbugprint(f"*** VOLUME CHANGE *** | on {dl.getHostname()} | ***", logging_level="INFO")
    dbugprint("Received: " + phrase, logging_level="INFO")

    phrase_post_change = ' '.join(str(changeWordToNumber(word)).lower() for word in phrase.split())
    if phrase_post_change != phrase:
        phrase = phrase_post_change
        dbugprint("Swapped in numbers: " + phrase)

    will_Increase = will_Decrease = will_Mute = will_Unmute = will_Toggle_Mute = False

    for word in phrase.split():
        if word in increase_words:
            will_Increase = True
        if word in decrease_words:
            will_Decrease = True
        if any([True if re.search(x, word) else False for x in mute_words]) or phrase.count("shut up"):
            will_Mute = True
            if phrase.count("toggle"):
                will_Toggle_Mute = True
            elif re.search(r"\bun\w+", phrase):
                will_Unmute = True
        if word in unmute_words:
            will_Unmute = True

    dbugprint("Boolean flags summary:\nwill_Increase: "+ str(will_Increase)\
        + "\nwill_Decrease:" + str(will_Decrease)\
        + "\nwill_Mute: " + str(will_Mute)\
        + "\nwill_Unmute: " + str(will_Unmute)\
        + "\nwill_Toggle_Mute: " + str(will_Toggle_Mute)
        )

    number = -1
    number_found = re.search("(\d+)", phrase)
    if number_found:
        number = int(number_found.group(1))
        dbugprint(f"Number is {number}")
    
    if not any([will_Increase, will_Decrease, will_Mute, will_Unmute, will_Toggle_Mute, number != -1]):
        dbugprint(f"Nothing was understood from \"{phrase}\".  Exiting!", logging_level="WARNING")
        _speak("Sorry. I didn't understand.")
        exit(3)

    if will_Increase and will_Decrease:
        dbugprint("What you smoking?  I don't get you.", logging_level="ERROR")
        _speak("That was a load of gowble-d gook.")
        exit(4)

    if will_Toggle_Mute:
        _do(_toggleMute)

    if will_Unmute:
        _do(_unMute)
    
    if will_Mute:
        _do(_mute)
    
    byPercentage = phrase.count("percent") or phrase.count("%")

    percentage = 10
    if number != -1:
        if number > 100:
            # correct if over 100
            percentage = 100
        elif byPercentage or number >= 10:
            # if # is above 10, assume we're talking about a percentage
            percentage = number
        elif number > 0:
            # if # is in 0-10, assume range is 0-10 (so 3 means 30% like how the smart assistants do)
            percentage = number * 10
        else:
            # if # is negative... I did something wrong somewhere although this should never catch cuz currently a regex match grabs a #, no negative signs
            dbugprint(f"Unexpected number recieved: {number}", logging_level="WARNING")
            _speak("Unexpected error.  Did you give me a negative number?")
    
    if will_Increase:
        _do(_increaseVolume, percentage)
    
    if will_Decrease:
        _do(_decreaseVolume, percentage)
    
    _do(_setVolume, percentage)

if __name__ == "__main__":
    main()
    from time import sleep
    sleep(3)