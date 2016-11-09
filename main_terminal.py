#!/usr/bin/env python3

import os, curses, itertools, time, queue, atexit
import link
from housepy import config, log, util

CHARACTERS = config['characters']

receiver = link.Receiver(23232)
sender = link.Sender(23234)

try:
    messages = util.load("transcript.pkl")
except Exception:
    messages = []
spinner = itertools.cycle(['—', '\\', '|', '/'])
ready = config['start']

current = []

def curses_main(args):
    global ready, receiver, sender, current
    # try:
    w = curses.initscr()                                            # initialize
    curses.use_default_colors()                                     # use the terminal settings for color_pair 0, otherwise it's black and white
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)     # define some other color pairs
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    w.bkgd(" ", curses.color_pair(1))                               # use a custom for the default
    # curses.echo()                                                 # show what's being typed
    curses.noecho()                                                 # or dont
    while True:

        # draw chat history
        LINES, COLUMNS = w.getmaxyx()
        for i in range(LINES - 1):
            if i < len(messages):                    
                message = messages[-1 * (i + 1)]
                index = messages.index(message)
                color = 1 if message[0] == 0 else 2
                w.addstr(LINES - i - 2, 0, "  " + message[1], curses.A_BOLD | curses.color_pair(color))    # draw the line
                w.clrtoeol()      
                                                                        # erase the rest of it
        # take input
        if ready:
            curses.flushinp()
            curses.curs_set(1)
            w.addstr(LINES - 1, 0, "> %s" % "".join(current), curses.color_pair(1))          # display something
            ch = w.getch()
            log.debug(ch)
            if ch != 10:
                if ch == 127 or ch == 8:
                    if len(current):
                        current.pop()
                # elif ch < 128 and len(current) < 30:                    # restrict to ascii. make it 256 if you need latin.
                elif len(current) < 30 and chr(ch).upper() in CHARACTERS:
                    current.append(chr(ch).upper())
            else:
                message_s = "".join(current).strip()
                if message_s == "MARADONA":
                    exit()          
                elif message_s == "UNDO":
                    messages.pop()          
                elif len(message_s):
                    messages.append((0, message_s))
                    sender.messages.put(message_s)
                    flush_messages()
                    ready = False
            w.addstr(LINES - 1, 0, "> %s" % "".join(current), curses.color_pair(1))          # display something
            w.clrtoeol()                                                # erase from cursor to end of line                
            w.refresh()

        # get a response
        else:
            curses.curs_set(0)
            w.addstr(LINES - 1, 0, "> Waiting for message... " + next(spinner), curses.A_REVERSE)
            w.clrtoeol()
            w.refresh()
            time.sleep(0.1)
            message_s = get_message()
            if message_s is not None:
                messages.append((1, message_s))
                ready = True

    # except Exception as e:
    #     log.error(log.exc(e))

def get_message():
    message = None
    while True:
        try:
            message = receiver.messages.get_nowait()
        except queue.Empty:
            break    
    return message

def flush_messages():
    while True:
        try:
            receiver.messages.get_nowait()
        except queue.Empty:
            break

def exit_handler():
    util.save("transcript.pkl", messages)
    print("Exiting...")
atexit.register(exit_handler)


curses.wrapper(curses_main)



"""

disable control-c?

it should cache the whole conversation and load it on startup (via an argument)

"""