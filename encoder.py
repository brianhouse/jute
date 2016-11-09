#!/usr/bin/env python3

import sys, smaz, base64, subprocess
from jute_song import phrases
from housepy import config, log


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
    music(message)
    subprocess.run(["open", "result.png"])