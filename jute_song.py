import json, shutil
from housepy import log

phrases = [
    "d'2",

    "d''2",

    "g'4 g'4",
    "b'4 b'4",    

    "d'4 e'4",
    "d'4 e'8. g'16",

    "d'4. b'8",   
    "g'4~ g'8. b'16",
    "g'8 b'4.",    
    "c''4. d''8",    
    "d''4. e''8",

    "d'4. b8",
    "d'4. c'8",


    "e'4 d'4",
    "a'8 g'4.",

    "c''4 b'4",
    "d''8 b'4.",
    "d''4 c''4",
    "d''8 c''4.",


    "d'4 d'16 g'8.",

    "g'8 a'4 b'8",

    "e'4 a'8 g'8",
    "a'8 b'8 g'4",

    "b'4 a'8 g'8",


    "e'8 d'4 d''8",

    "e'16 e'8. a'8 g'8",
    "c''16 c''8. b'8 a'8",


    "d''8 d''8 d''8 e''8",
    "d''8 d''8 d''8 a'8",

    "c''8 b'8 a'8 g'8",
    "c''8 b'8 g'8 e'8",
    "b'8 a'8 g'8 e'8",
    "b'8 a'8 g'8 d'8",
    "b'8 a'8 g'8 a'8",
    "c''8 c''8 b'8 a'8",

]


if __name__ == "__main__":

    material = [ "d'4 e'4",
                "d'4. c'8",
                "d'4 d'16 g'8.",
                "g'4~ g'8. b'16",
                "c''4 b'4",
                "a'8 g'4.",
                "b'8 a'8 g'8 e'8",
                "d'2",
                "d''4. e''8",
                "d''4 c''4",            
                "b'8 a'8 g'8 e'8",            
                "c''4. d''8",            
                "b'8 a'8 g'8 d'8",
                "e'4 a'8 g'8",            
                "e'4 d'4",            
                "d'2",            
                "d'4 e'4",
                "d'4. b'8",
                "c''8 b'8 g'8 e'8",
                "d'2",
                "c''16 c''8. b'8 a'8",
                "b'8 a'8 g'8 a'8",
                "b'8 a'8 g'8 e'8",
                "d'2",
                "d''8 d''8 d''8 e''8",
                "d''8 c''4.",
                "b'4 a'8 g'8",
                "c''4. d''8",
                "b'8 a'8 g'8 d'8",
                "e'16 e'8. a'8 g'8",
                "e'4 d'4",
                "d'2",
                "d'4 e'4",
                "d'4. b8",
                "d'4 e'8. g'16",
                "g'8 b'4.",
                "c''8 c''8 b'8 a'8",
                "g'8 a'4 b'8",
                "c''8 b'8 a'8 g'8",
                "e'8 d'4 d''8",
                "d''8 d''8 d''8 e''8",
                "d''8 b'4.",
                "b'4 a'8 g'8",
                "c''4. d''8",
                "b'8 a'8 g'8 d'8",
                "e'16 e'8. a'8 g'8",
                "e'4 d'4",
                "d'2",
                "a'8 b'8 g'4",
                "d''8 d''8 d''8 a'8",  
                "g'4 g'4",
                "b'4 b'4",
                "d''2",                
                ]

    def purge_dups(material):
        dups = []
        for phrase in material:
            matches = []
            for p, phrase_ in enumerate(material):
                if phrase == phrase_:
                    matches.append(p)
                    dups.extend(matches[1:])
        material = [phrase for (p, phrase) in enumerate(material) if (p not in dups)]
        if len(material) < 32:
            log.warning("WARNING: insufficient encoder length (%s)" % len(material))   
        return material        

    material = purge_dups(material)


    print(json.dumps(material, indent=4))

    for p, phrase in enumerate(material):
        print("%s -> %s" % (p, phrases.index(phrase)))
        p1 = str(p)
        if len(p1) < 2:
            p1 = "0%s" % p1
        p2 = str(phrases.index(phrase))
        if len(p2) < 2:
            p2 = "0%s" % p2
        shutil.copy("phrases/original/%s.png" % p1, "phrases/%s.png" % p2)


