#!/usr/bin/env python3

import queue, time, subprocess
import link, encoder
from PIL import Image
from housepy import config, log, animation

FILENAME = "result.png"

first_time = True
waiting = True
transmitting = False
label = None

incoming_message = []
partial_decoding = ""
coords = []

sender = link.Sender(23232)
receiver = link.Receiver(23234)

animation.show_fps = False
ctx = animation.Context(859, 556, title="JUTE", background=(1., 1., 1., 1.), screen=1, fullscreen=True, chrome=False)  


def on_mouse_press(data):
    global waiting, transmitting, current_string, incoming_message, partial_decoding

    # waiting mode, nothing happens
    if waiting:
        return

    # transmitting mode, we've clicked, so go into receiving mode
    if transmitting:            
        ctx.textures = []                
        incoming_message = []
        partial_decoding = ""
        label.text = ""
        draw_reception()        
        transmitting = False
        return

    # receiving mode: process clicks and build message
    x, y, button, modifiers = data
    x *= ctx.width
    y *= ctx.height
    for c, coord in enumerate(coords):
        if x > coord[0][0] and x < coord[1][0] and y > coord[0][1] and y < coord[1][1]:                
            if c == 33:
                sender.messages.put(partial_decoding.strip())
                ctx.textures = []                
                incoming_message = []
                partial_decoding = ""
                label.text = ""
                result = subprocess.run(["osascript", "focus.scpt", "main_terminal"], stdout=subprocess.PIPE)
                log.info(result)        
                waiting = True                
            elif c == 32:
                incoming_message = incoming_message[:-1]
            else:
                character = encoder.CHARACTERS[c]
                incoming_message.append(character)
            partial = encoder.decode("".join(incoming_message))
            if partial is not False:
                partial_decoding = partial
            # label.text = "%s\n%s" % ("".join(incoming_message), partial_decoding)
            label.text = "%s\n%s" % (("•" * len(incoming_message)), partial_decoding)
            break

ctx.add_callback("mouse_press", on_mouse_press)

def draw_transmission(message):
    ctx.textures = []
    ctx.load_image(FILENAME, 0, -50, ctx.width, ctx.height)        

def draw_reception():
    global coords
    ctx.textures = []
    coords = []
    for i in range(34):
        filename = "phrases/%s.png" % (i if len(str(i)) == 2 else "0%s" % i)
        image = Image.open(filename)
        w, h = image.size
        x1 = 400 + (i % 8) * (70 + 25)
        y1 = ctx.height - ((i // 8) * (70 + 25)) - 200
        x2 = x1 + w
        y2 = y1 + h
        ctx.load_image(filename, x1, y1, w, h)
        coords.append(((x1, y1), (x2, y2)))    

def draw():
    global first_time, waiting, transmitting, label
    if first_time:
        label = ctx.label(0.5, 0.2, "", font="Monaco", center=True, width=600)
        first_time = False
    if waiting:
        message = None
        while True:
            try:
                message = receiver.messages.get_nowait()
            except queue.Empty:
                break
        if message is not None:
            encoder.music(message)
            draw_transmission(message)
            waiting = False
            transmitting = True
    time.sleep(0.05)

if not config['start']:
    draw_reception()    
ctx.start(draw)
