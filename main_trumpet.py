#!/usr/bin/env python3

import queue, time, subprocess
import link, encoder
from housepy import config, log, animation

FILENAME = "result.png"

transmitting = not config['start']

sender = link.Sender(23232)
receiver = link.Receiver(23234)

animation.show_fps = False
ctx = animation.Context(859, 556, title="JUTE", background=(0.9, 0.9, 0.9, 1.), screen=1, fullscreen=True, chrome=False)  

def on_mouse_press(data):
    global transmitting
    if transmitting:            
        ctx.textures = []
        transmitting = False
        sender.messages.put("This is a fake response")
        result = subprocess.run(["osascript", "focus.scpt", "main_terminal"], stdout=subprocess.PIPE)
        log.info(result)
ctx.add_callback("mouse_press", on_mouse_press)

def draw():
    global transmitting
    if not transmitting:
        message = None
        while True:
            try:
                message = receiver.messages.get_nowait()
            except queue.Empty:
                break
        if message is not None:
            encoder.music(message)
            ctx.textures = []
            ctx.load_image(FILENAME, 0, 0, ctx.width, ctx.height)        
            transmitting = True
    time.sleep(.1)
ctx.start(draw)
