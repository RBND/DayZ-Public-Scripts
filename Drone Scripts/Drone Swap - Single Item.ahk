#Requires AutoHotkey v2.0
#SingleInstance Force

; Global variables to store coordinates
global pickupX := 0
global pickupY := 0
global dropX := 0
global dropY := 0
global locationsSet := false

; Create a GUI to display status
StatusGui := Gui(, "DayZ Item Swap")
StatusGui.SetFont("s12")
StatusText := StatusGui.Add("Text", "w300 h50", "Press F2 to set pickup/drop locations")
StatusGui.Show("NoActivate")

; F2 key to set locations
F2::SetLocations()

; F1 key to perform the swap
F1::SwapItem()

; Function to set pickup and drop locations
SetLocations() {
    global pickupX, pickupY, dropX, dropY, locationsSet, StatusText

    ; Update GUI
    StatusText.Value := "Click on the PICKUP location (item in inventory)"
    StatusGui.Show("NoActivate")

    ; Wait for left click to set pickup location
    KeyWait "LButton", "D"
    MouseGetPos &pickupX, &pickupY
    Sleep 500

    ; Update GUI
    StatusText.Value := "Click on the DROP location (equipped slot)"
    StatusGui.Show("NoActivate")

    ; Wait for left click to set drop location
    KeyWait "LButton", "D"
    MouseGetPos &dropX, &dropY

    ; Set flag that locations are configured
    locationsSet := true

    ; Update GUI
    StatusText.Value := "Locations set! Press F1 to swap items"
    StatusGui.Show("NoActivate")

    return
}

; Function to perform the item swap
SwapItem() {
    global pickupX, pickupY, dropX, dropY, locationsSet, StatusText

    ; Check if locations are set
    if (!locationsSet) {
        StatusText.Value := "Locations not set! Press F2 first"
        StatusGui.Show("NoActivate")
        return
    }

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
        MouseMove dropX, dropY, 5  ; Added speed parameter (5) for smoother movement
        Sleep 100

        ; Release left mouse button
        Send "{LButton Up}"
        Sleep 50

        ; Return mouse to original position
        MouseMove currentX, currentY

        StatusText.Value := "Item swapped successfully!"
    } catch as e {
        ; Make sure button is released if an error occurs
        Send "{LButton Up}"
        StatusText.Value := "Error: " e.Message
    }

    StatusGui.Show("NoActivate")
    return
}

; Right-click on the tray icon to exit
ExitFunc(ExitReason, ExitCode) {
    StatusGui.Destroy()
}

OnExit ExitFunc

