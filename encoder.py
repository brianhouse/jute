#!/usr/bin/env python3

import sys, smaz, base64, subprocess
from jute_song import phrases
from housepy import config, log

CHARACTERS = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '2', '3', '4', '5', '6', '7'

def encode(s):
    remove = [c for c in s if ord(c) > 127]
    for c in remove:
        s = s.replace(c, '')
    result = base64.b32encode(smaz.compress(s).encode()).decode()
    result = result.strip("=")
    log.info("%s %s %s %s" % (s, len(s), result, len(result)))
    return result

def decode(s):
    try:
        padding = (((len(s) // 8) + 1) * 8) - len(s) if len(s) % 8 != 0 else 0
        padding = "=" * padding
        result = smaz.decompress(base64.b32decode((s + padding)).decode())
        log.info("%s %s %s %s" % (s, len(s), result, len(result)))
        return result
    except Exception as e:
        log.error(e)
        return False

def encode(s):
    return s

def decode(s):
    return s

def music(message):
    song = []
    for c in encode(message):
        index = CHARACTERS.index(c)
        phrase = phrases[index % len(phrases)]
        if len(song) % 4 == 3:
            phrase += ' \\bar "||"'
        song.append(phrase)
    song = ' '.join(song)
    with open("template.ly") as f:
        template = f.read()
    template = template.replace("MUSIC", song).replace("TITLE", message)
    with open("result.ly", "w") as f:
        f.write(template)
    result = subprocess.run(["lilypond", "-fpng", "result.ly"], stdout=subprocess.PIPE)
    log.info(result.stdout)
    result = subprocess.run(["convert", "-rotate", "90", "result.png", "result.png"], stdout=subprocess.PIPE) # annoying
    log.info(result.stdout)
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[string]")
        exit()
    message = sys.argv[1]
    decode(encode(message))
    # music(message)
    # subprocess.run(["open", "result.png"])
    # subprocess.run(["open", "result.midi"])
