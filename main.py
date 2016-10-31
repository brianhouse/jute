#!/usr/bin/env python3

import os, curses
from housepy import config, log


messages = []

def curses_main(args):
    try:
        w = curses.initscr()                                            # initialize
        curses.use_default_colors()                                     # use the terminal settings for color_pair 0, otherwise it's black and white
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)     # define some other color pairs
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        w.bkgd(" ", curses.color_pair(1))                               # use a custom for the default
        curses.echo()                   # show what's being typed
        while True:
            LINES, COLUMNS = w.getmaxyx()
            w.addstr(LINES - 1, 0, "> ", curses.color_pair(3))        # display something
            w.clrtoeol()                        # erase from cursor to end of line
            s = w.getstr().decode().strip()     # allow typing and return
            if len(s):
                messages.append(s)
            if s == "exit":
                break
            for i in range(LINES - 1):
                if i < len(messages):                    
                    message = messages[-1 * (i + 1)]
                    index = messages.index(message)
                    color = 1 if (index % 2) else 2
                    w.addstr(LINES - i - 2, 0, message, curses.A_BOLD | curses.color_pair(color))    # draw the line
                    w.clrtoeol()                                                                    # erase the rest of it
    except Exception as e:
        log.error(log.exc(e))

curses.wrapper(curses_main)


"""
Comment out exit in production


w.addstr(LINES - i - 2, 0, messages[-1 * (i + 1)], curses.A_REVERSE)  # draw the line
video reverse colors
curses.A_BOLD

"""