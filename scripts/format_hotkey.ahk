; AutoHotkey script to trigger the format panel via hotkey Ctrl+Alt+F
; Place this file in the project root (next to run.bat) and run it with AutoHotkey.
; It will execute run.bat format using the script directory as working dir.

^!f::
    ; Run the project's run.bat with the "format" argument
    Run, %A_ScriptDir%\run.bat format
    Return
