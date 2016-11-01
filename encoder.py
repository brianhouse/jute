#!/usr/bin/env python3

import sys, smaz, base64

def encode(s):
    result = base64.b32encode(smaz.compress(s).encode()).decode()
    result = result.strip("=")
    print(s, len(s), result, len(result))
    return result

def decode(s):
    padding = (((len(s) // 8) + 1) * 8) - len(s) if len(s) % 8 != 0 else 0
    padding = "=" * padding
    result = smaz.decompress(base64.b32decode((s + padding)).decode())
    print(s, len(s), result, len(result))
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[string]")
        exit()
    s = sys.argv[1]
    decode(encode(s))


"""
Are there still strings that break this?

"""