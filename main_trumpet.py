#!/usr/bin/env python3

import queue, time, subprocess
import link, encoder
from PIL import Image
from housepy import config, log, animation

FILENAME = "result.png"

CHARACTERS = config['characters']

first_time = True
waiting = True
transmitting = False
label = None

incoming_message = []
coords = []

sender = link.Sender(23232)
receiver = link.Receiver(23234)

animation.show_fps = False
ctx = animation.Context(859, 556, title="OH DEAR ME", background=(1., 1., 1., 1.), screen=1, fullscreen=config['fullscreen'], chrome=not config['fullscreen'])  


def on_mouse_press(data):
    global waiting, transmitting, current_string, incoming_message

    # waiting mode, nothing happens
    if waiting:
        log.debug("MODE: waiting")
        return

    # transmitting mode, we've clicked, so go into receiving mode
    if transmitting:            
        log.debug("MODE: transmitting")
        ctx.textures = []                
        incoming_message = []
        label.text = ""
        ctx.objects = [o for o in ctx.objects if o is label]
        draw_reception()        
        transmitting = False
        return

    # receiving mode: process clicks and build message
    log.debug("MODE: receiving")    
    x, y, button, modifiers = data
    x *= ctx.width
    y *= ctx.height
    for c, coord in enumerate(coords):
        if x > coord[0][0] and x < coord[1][0] and y > coord[0][1] and y < coord[1][1]:                
            if c == len(CHARACTERS):
                sender.messages.put("".join(incoming_message).strip())
                ctx.textures = []                
                incoming_message = []
                label.text = ""
                ctx.objects = [o for o in ctx.objects if o is label]
                result = subprocess.run(["osascript", "focus.scpt", "main_terminal"], stdout=subprocess.PIPE)
                log.info(result)        
                waiting = True                
            else:
                character = CHARACTERS[c]
                incoming_message.append(character)
            label.text = "".join(incoming_message)
            break

ctx.add_callback("mouse_press", on_mouse_press)

def draw_transmission(message):
    ctx.textures = []
    ctx.load_image(FILENAME, 0, -50, ctx.width, ctx.height)        

def draw_reception():
    global coords
    ctx.textures = []
    coords = []
    for i in range(36):
        filename = "phrases/%s.png" % (i if len(str(i)) == 2 else "0%s" % i)
        image = Image.open(filename)
        w, h = image.size
        # x1 = 400 + (i % 8) * (70 + 25)
        x1 = 20 + (i % 8) * (70 + 25)
        # y1 = ctx.height - ((i // 8) * (70 + 25)) - 200
        y1 = ctx.height - ((i // 8) * (70 + 25)) - 100
        x2 = x1 + w
        y2 = y1 + h
        ctx.load_image(filename, x1, y1, w, h)
        t = CHARACTERS[i] if i < len(CHARACTERS) else ""
        ctx.label((x1 + ((x2 - x1) / 2)) / ctx.width, (y1 + 70) / ctx.height, t, font="Monaco", center=True, width=30, size=8)
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
    waiting = False
    transmitting = False
    draw_reception()    
ctx.start(draw)
