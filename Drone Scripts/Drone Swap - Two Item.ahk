#Requires AutoHotkey v2.0
#SingleInstance Force

; Global variables to store coordinates
global pickupX := 0
global pickupY := 0
global pickup2X := 0
global pickup2Y := 0
global dropX := 0
global dropY := 0
global locationsSet := false
global locations2Set := false
global setupMode := false

; Create a GUI to display status
StatusGui := Gui(, "DayZ Item Swap")
StatusGui.SetFont("s12")
StatusText := StatusGui.Add("Text", "w350 h50", "Press F1 to set up first item swap")
StatusGui.Add("Text", "w350 h30 y+10", "Script only works when DayZ is active")
StatusGui.Show("NoActivate")

; Only activate hotkeys when DayZ is the active window
#HotIf WinActive("ahk_class DayZ")

; F1 key - Set locations on first press, swap on subsequent presses
F1::HandleF1()

; F2 key - Set second item location on first press, swap on subsequent presses
F2::HandleF2()

; Add a reset hotkey (F5)
F5::ResetLocations()

#HotIf ; End context sensitivity

; Function to handle F1 key
HandleF1() {
    global pickupX, pickupY, dropX, dropY, locationsSet, StatusText, setupMode

    ; Check if DayZ is active
    if (!WinActive("ahk_class DayZ")) {
        StatusText.Value := "DayZ is not active! Activate the game first."
        StatusGui.Show("NoActivate")
        return
    }

    ; If locations aren't set, enter setup mode
    if (!locationsSet) {
        setupMode := true

        ; Step 1: Set pickup location
        StatusText.Value := "Click on the PICKUP location (item in inventory)"
        StatusGui.Show("NoActivate")

        KeyWait "LButton", "D"
        MouseGetPos &pickupX, &pickupY
        Sleep 500

        ; Step 2: Set drop location
        StatusText.Value := "Click on the DROP location (equipped slot)"
        StatusGui.Show("NoActivate")

        KeyWait "LButton", "D"
        MouseGetPos &dropX, &dropY

        ; Mark as configured
        locationsSet := true
        setupMode := false

        StatusText.Value := "Item 1 locations set! Press F1 again to swap"
        StatusGui.Show("NoActivate")
    }
    ; If locations are already set, perform the swap
    else {
        ; Save current mouse position
        MouseGetPos &currentX, &currentY

        ; Perform the swap
        try {
            ; Move to the item to pick up
            MouseMove pickupX, pickupY
            Sleep 50

            ; Press and hold left mouse button
            Send "{LButton Down}"
            Sleep 100

            ; Move to the destination while holding button
            MouseMove dropX, dropY, 5
            Sleep 100

            ; Release left mouse button
            Send "{LButton Up}"
            Sleep 50

            ; Return mouse to original position
            MouseMove currentX, currentY

            StatusText.Value := "Item 1 swapped successfully!"
        } catch as e {
            ; Make sure button is released if an error occurs
            Send "{LButton Up}"
            StatusText.Value := "Error: " e.Message
        }

        StatusGui.Show("NoActivate")
    }

    return
}

; Function to handle F2 key
HandleF2() {
    global pickup2X, pickup2Y, dropX, dropY, locationsSet, locations2Set, StatusText, setupMode

    ; Check if DayZ is active
    if (!WinActive("ahk_class DayZ")) {
        StatusText.Value := "DayZ is not active! Activate the game first."
        StatusGui.Show("NoActivate")
        return
    }

    ; Check if primary locations are set first
    if (!locationsSet) {
        StatusText.Value := "Set up item 1 with F1 first!"
        StatusGui.Show("NoActivate")
        return
    }

    ; If second location isn't set, enter setup mode
    if (!locations2Set) {
        setupMode := true

        ; Set pickup location for second item
        StatusText.Value := "Click on the SECOND item pickup location"
        StatusGui.Show("NoActivate")

        KeyWait "LButton", "D"
        MouseGetPos &pickup2X, &pickup2Y

        ; Mark as configured
        locations2Set := true
        setupMode := false

        StatusText.Value := "Item 2 location set! Press F2 again to swap"
        StatusGui.Show("NoActivate")
    }
    ; If location is already set, perform the swap
    else {
        ; Save current mouse position
        MouseGetPos &currentX, &currentY

        ; Perform the swap
        try {
            ; Move to the second item to pick up
            MouseMove pickup2X, pickup2Y
            Sleep 50

            ; Press and hold left mouse button
            Send "{LButton Down}"
            Sleep 100

            ; Move to the destination while holding button
            MouseMove dropX, dropY, 5
            Sleep 100

            ; Release left mouse button
            Send "{LButton Up}"
            Sleep 50

            ; Return mouse to original position
            MouseMove currentX, currentY

            StatusText.Value := "Item 2 swapped successfully!"
        } catch as e {
            ; Make sure button is released if an error occurs
            Send "{LButton Up}"
            StatusText.Value := "Error: " e.Message
        }

        StatusGui.Show("NoActivate")
    }

    return
}

; Function to reset all locations
ResetLocations() {
    global locationsSet, locations2Set

    ; Check if DayZ is active
    if (!WinActive("ahk_class DayZ")) {
        StatusText.Value := "DayZ is not active! Activate the game first."
        StatusGui.Show("NoActivate")
        return
    }

    locationsSet := false
    locations2Set := false

    StatusText.Value := "Locations reset! Press F1 to set up again"
    StatusGui.Show("NoActivate")
    return
}

; Add a tray menu item to show/hide the status window
A_TrayMenu.Add("Show/Hide Status", ShowHideStatus)

ShowHideStatus(*) {
    if WinExist("ahk_id " StatusGui.Hwnd) {
        if WinActive("ahk_id " StatusGui.Hwnd)
            StatusGui.Hide()
        else
            StatusGui.Show("NoActivate")
    } else {
        StatusGui.Show("NoActivate")
    }
}

; Right-click on the tray icon to exit
ExitFunc(ExitReason, ExitCode) {
    StatusGui.Destroy()
}

OnExit ExitFunc

