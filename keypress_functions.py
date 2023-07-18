from pynput.keyboard import Key, Controller
import time
from os import system

kb = Controller()

#########################
###  helper functions ###
#########################

multiple_key_tap_delay = 0.2 # seconds

def tap(key):
    # Just a shortcut for this.
    kb.tap(key)

def sleep(seconds=1):
    # Just a shortcut for this.
    time.sleep(seconds)

def _tap_multiple_times(key, n=2):
    for i in range(n):
        tap(key)
        # tap() is same as...
        #kb.press(key)
        #kb.release(key)
        sleep(multiple_key_tap_delay)

def press(combination_keys_list):
    for key in combination_keys_list:
        kb.press(key)
    for key in combination_keys_list:
        kb.release(key)
    # Need this refractory timer for whatever was executed to follow through
    sleep(0.3)

def pressInSequence(combination_keys_list, subsequent_sequential_keys_list):
    if not subsequent_sequential_keys_list:
        print("Second parameter cannot be empty")
        return
    press(combination_keys_list)
    for key in subsequent_sequential_keys_list:
        sleep(0.3)
        kb.tap(key)

########################
###  WINDOWS actions ###
########################

def do_move():
    pressInSequence([Key.alt, Key.space], ['m', Key.right, Key.left])

def do_resize():
    pressInSequence([Key.alt, Key.space], ['s', Key.down, Key.right])

def do_resize_left():
    pressInSequence([Key.alt, Key.space], ['s', Key.left])

def do_resize_right():
    pressInSequence([Key.alt, Key.space], ['s', Key.right])

def do_resize_top():
    pressInSequence([Key.alt, Key.space], ['s', Key.up])

def do_resize_bottom():
    pressInSequence([Key.alt, Key.space], ['s', Key.down])

def do_minimize():
    # Replacing this method which will fail for some programs like a termianl window.
    #pressInSequence([Key.alt, Key.space], ['n'])
    # For Win + down, which works for all windows.
    with kb.pressed(Key.cmd):
        _tap_multiple_times(Key.down, 5)

def do_maximize():
    #press([Key.cmd, Key.up])
    with kb.pressed(Key.cmd):
        _tap_multiple_times(Key.up, 5)

def do_restore():
    pressInSequence([Key.alt, Key.space], ['r'])

def do_dock_left():
    pressInSequence([Key.cmd, Key.left], [Key.esc])

def do_dock_right():
    pressInSequence([Key.cmd, Key.right], [Key.esc])

def do_alt_tab(n=1):
    with kb.pressed(Key.alt):
        _tap_multiple_times(Key.tab, n)

def do_change_app():
    press([Key.ctrl, Key.alt, Key.tab])

def do_exit_app():
    press([Key.alt, Key.f4])

def do_switch_app_to(name="notepad"):
    # This doesn't work reliably.
    # I think it's failing to work when the terminal window is run in the background.
    # More testing needed.
    # _ is python's throw-away variable
    _ = system(f"powershell -command \"(New-Object -ComObject wscript.shell).AppActivate('{name}') | Out-Null\"")
    #print(f"Did we successfully switch to '{name}'?")

########################
###  BROWSER actions ###
########################

def do_new_tab():
    press([Key.ctrl, 't'])

def do_new_window():
    press([Key.ctrl, 'n'])

def do_close_tab():
    press([Key.ctrl, 'w'])

def do_change_tab(n=1):
    with kb.pressed(Key.ctrl):
        _tap_multiple_times(Key.tab, n)

def do_go_to(string):
    site = string.replace(' ','')
    press([Key.alt, 'd'])
    sleep(multiple_key_tap_delay)
    kb.type(site)
    sleep(multiple_key_tap_delay)
    tap(Key.enter)

def do_refresh():
    press([Key.f5])

def do_go_back():
    press([Key.alt, Key.left])

def do_go_forward():
    press([Key.alt, Key.right])

def do_reopen_tab():
    press([Key.ctrl, Key.shift, 't'])

#####################
###  TEXT actions ###
#####################

def do_select_all():
    press([Key.ctrl, 'a'])

def do_cut():
    press([Key.ctrl, 'x'])

def do_copy():
    press([Key.ctrl, 'c'])

def do_paste():
    press([Key.ctrl, 'v'])

def do_undo():
    press([Key.ctrl, 'z'])

def do_redo():
    press([Key.ctrl, 'y'])

def do_home():
    press([Key.home])

def do_end():
    press([Key.end])

def do_page_up(n=1):
    _tap_multiple_times(Key.page_up, n)

def do_page_down(n=1):
    _tap_multiple_times(Key.page_down, n)

def do_save():
    press([Key.ctrl, 's'])

def do_save_as():
    press([Key.ctrl, Key.shift, 's'])

def do_emoji():
    press([Key.cmd, '.'])

#######################
###  SYSTEM actions ###
#######################

def do_minimize_all():
    press([Key.cmd, 'd'])

def do_minimize_everything_else():
    press([Key.cmd, Key.home])

def do_run_prompt():
    press([Key.cmd, 'r'])

def do_task_manager():
    with kb.pressed(Key.ctrl, Key.shift):
        kb.tap(Key.esc)

def do_change_input_lang():
    press([Key.cmd, Key.space])

def do_change_input_lang_back():
    press([Key.ctrl, Key.cmd, Key.space])

def do_change_input_lang_to_EN():
    press([Key.ctrl, '1'])

def do_change_input_lang_to_JP():
    press([Key.ctrl, Key.shift, '1'])

def do_show_notification():
    press([Key.cmd, 'a'])

def do_show_time_and_calendar():
    press([Key.cmd, Key.alt, 'd'])

def do_start_dictation():
    press([Key.cmd, 'h'])

def do_show_settings():
    press([Key.cmd,'i'])

def do_take_screen_snippet():
    press([Key.cmd, Key.shift, 's'])

def do_take_screenshot():
    press([Key.print_screen])

def do_save_screenshot():
    press([Key.cmd, Key.print_screen])

def do_save_screenshot_of_active_window():
    press([Key.alt, Key.cmd, Key.print_screen])

def do_open_system_menu():
    press([Key.cmd, 'x'])

def do_open_control_panel():
    press([Key.cmd, 'r'])
    kb.type("control")
    sleep(multiple_key_tap_delay)
    press([Key.enter])

""" # Doesn't work. I believe this is special key combo that can't be simulated.
def ctrl_alt_del():
    with kb.pressed(Key.ctrl_l, Key.alt_l):
        time.sleep(0.5)
        kb.tap(Key.delete)
    print("Done.  Although this has never worked.")"""

######################
###  MEDIA actions ###
######################

def do_press_spacebar():
    tap(' ')

def do_press_F():
    tap('f')

""" Template for quickly writing new action function
def do_tempate():
    press([])
"""