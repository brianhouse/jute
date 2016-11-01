from housepy import log

phrases = [ "d'4 e'4",
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
            "d'2"
            ]

def purge_dups(phrases):
    dups = []
    for phrase in phrases:
        matches = []
        for p, phrase_ in enumerate(phrases):
            if phrase == phrase_:
                matches.append(p)
                dups.extend(matches[1:])
    phrases = [phrase for (p, phrase) in enumerate(phrases) if (p not in dups)]
    if len(phrases) < 32:
        log.warning("WARNING: insufficient encoder length (%s)" % len(phrases))   
    return phrases        

phrases = purge_dups(phrases)
