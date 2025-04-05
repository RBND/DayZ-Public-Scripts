#Requires AutoHotkey v2.0
#SingleInstance Force
^!x::ExitApp
^x::Suspend

F2::
{
	Drag(1703, 1116, 20)
	InvCycle()
	OpenMRE()
	InvCycle()
	ExtractMRE()
	Discard()
}

;	Functions
;--------------------
Click()
{
	Send "{LButton down}"
	Sleep 50
	Send "{LButton up}"
	Sleep 50
}

	DoubleClick()
	{
		Send "{LButton down}"
		Sleep 50
		Send "{LButton up}"
		Sleep 50
		Send "{LButton down}"
		Sleep 50
		Send "{LButton up}"
		Sleep 50
	}

	OpenMRE()
	{
		Send "{LButton Down}"
		Sleep 100
		Send "{LButton up}"
		Sleep 2200
	}

	InvCycle()
	{
		Send "{Tab down}"
		Sleep 100
		Send "{Tab up}"
		Sleep 500
	}

	DblInvCycle()
	{
		Send "{Tab down}"
		Sleep 100
		Send "{Tab up}"
		Sleep 500
		Send "{Tab down}"
		Sleep 100
		Send "{Tab up}"
		Sleep 500
	}

	Drag(a,b,c)
	{
		Send "{LButton Down}"
		Sleep 100
		MouseMove a, b, c
		Sleep 50
		Send "{LButton Up}"
		Sleep 50
	}

DragDrop(a,b,c,x,y,z)
{
	MouseMove a, b, c
	Send "{LButton Down}"
	Sleep 100
	MouseMove x, y, z
	Sleep 50
	Send "{LButton Up}"
	Sleep 50
}

Discard()
{
	MouseMove 1705, 1010, 40
	Sleep 100
	Send "{LButton down}"
	Sleep 100
	MouseMove 88, 63, 40
	Sleep 100
	Send "{LButton up}"
	Sleep 50
}

ExtractMRE()
{
	MouseMove 1920, 1070, 20
	DoubleClick()
	MouseMove 1844, 1070, 20
	DoubleClick()
	MouseMove 1755, 1070, 20
	DoubleClick()
	MouseMove 1669, 1070, 20
	DoubleClick()
	MouseMove 1580, 1070, 20
	DoubleClick()
	MouseMove 1499, 1070, 20
	DoubleClick()
	Sleep 50
}
