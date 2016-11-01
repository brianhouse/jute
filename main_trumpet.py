#!/usr/bin/env python3

import queue, time
import link, encoder
from housepy import config, log, animation

FILENAME = "result.png"

transmitting = False

sender = link.Sender(23232)
receiver = link.Receiver(23234)

animation.show_fps = False
ctx = animation.Context(859, 556, title="JUTE", background=(0.9, 0.9, 0.9, 1.), fullscreen=False)  
# ctx.add_callback("key_press", on_key_press)

def on_mouse_press(data):
    global transmitting
    if transmitting:            
        ctx.textures = []
        transmitting = False
        sender.messages.put("This is a fake response")
ctx.add_callback("mouse_press", on_mouse_press)

def draw():
    global transmitting
    if not transmitting:
        try:
            message = receiver.messages.get_nowait()
            encoder.music(message)
            ctx.textures = []
            ctx.load_image(FILENAME, 0, 0, ctx.width, ctx.height)        
            transmitting = True
        except queue.Empty:
            pass
    time.sleep(.1)
ctx.start(draw)
