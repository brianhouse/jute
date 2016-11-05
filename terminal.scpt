tell application "Terminal"
    activate
    set theWindow to the first item of (get the windows whose name contains "main_terminal")
    set index of theWindow to 1
    set visible of theWindow to false
    set visible of theWindow to true
    set isfullscreen to 1 of attribute "AXFullScreen" of theWindow
end tell
