\version "2.18.2"

\paper {
  #(set-paper-size "quarto")
}

\header {
  title = "TITLE"
  tagline = ""  % removed 
}

\score {
 
    \absolute {
        \time 4/4
        \clef treble
        \key g \major
        
        MUSIC

        \bar "|."

    }

    \layout { }

    \midi {
        \tempo 4 = 120
    }

}    


