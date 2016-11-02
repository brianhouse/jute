on run argv
    -- log item 1 of argv
    tell application "Terminal"
        activate
        set theWindow to the first item of (get the windows whose name contains (item 1 of argv))
        -- log theWindow
        set index of theWindow to 1
        set visible of theWindow to false
        set visible of theWindow to true
    end tell
end run