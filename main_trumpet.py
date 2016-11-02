#!/usr/bin/env python3

import queue, time, subprocess
import link, encoder
from PIL import Image
from housepy import config, log, animation

FILENAME = "result.png"
LEFT_MARGIN = 400

transmitting = not config['start']
first_time = True
label = None

incoming_message = []
partial_decoding = ""

sender = link.Sender(23232)
receiver = link.Receiver(23234)

coords = []

animation.show_fps = False
ctx = animation.Context(859, 556, title="JUTE", background=(0.9, 0.9, 0.9, 1.), screen=1, fullscreen=True, chrome=False)  

def on_mouse_press(data):
    global transmitting, current_string, incoming_message, partial_decoding

    # done transmitting, go into receiving mode
    if transmitting:            
        ctx.textures = []
        transmitting = False
        sender.messages.put("This is a fake response")
        result = subprocess.run(["osascript", "focus.scpt", "main_terminal"], stdout=subprocess.PIPE)
        log.info(result)
        draw_transmission()
        incoming_message = []
        partial_decoding = ""

    # receiving mode: process clicks and build message
    else:
        x, y, button, modifiers = data
        x *= ctx.width
        y *= ctx.height
        for c, coord in enumerate(coords):
            if x > coord[0][0] and x < coord[1][0] and y > coord[0][1] and y < coord[1][1]:                
                character = encoder.CHARACTERS[c]
                incoming_message.append(character)
                partial = encoder.decode("".join(incoming_message))
                if partial is not False:
                    partial_decoding = partial
                label.text = "%s\n%s" % ("".join(incoming_message), partial_decoding)

ctx.add_callback("mouse_press", on_mouse_press)

def draw_transmission(message):
    ctx.textures = []
    ctx.load_image(FILENAME, 0, 0, ctx.width, ctx.height)        

def draw_reception():
    global coords
    ctx.textures = []
    coords = []
    for i in range(16):
        filename = "phrases/%s.png" % (i if len(str(i)) == 2 else "0%s" % i)
        image = Image.open(filename)
        w, h = image.size
        x1 = LEFT_MARGIN + (i % 8) * (w + 25)
        y1 = ctx.height - ((i // 8) * (h + 25))
        x2 = x1 + w
        y2 = y1 + h
        ctx.load_image(filename, x1, y1, w, h)
        coords.append(((x1, y1), (x2, y2)))

def draw():
    global transmitting, first_time, label
    if first_time:
        label = ctx.label(0.5, 0.2, "hello world", font="Monaco", center=True, width=600)
        first_time = False
    if not transmitting:
        message = None
        while True:
            try:
                message = receiver.messages.get_nowait()
            except queue.Empty:
                break
        if message is not None:
            encoder.music(message)
            draw_transmission(message)
            transmitting = True
    time.sleep(0.1)

draw_reception()    

ctx.start(draw)
