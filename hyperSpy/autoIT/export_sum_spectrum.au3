	#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.0.0
 Author:         Pierre Burdet

 Script Function:
	Export SumSpectrum from INCA

#ce ----------------------------------------------------------------------------


	$filename = "EDX_map"
	$beginmap = 0
	$nbmap = 10
	
	; Activate window
	WinActivate("INCA")
	WinWaitActive("INCA")

	;Find window position
	$a = WinGetPos("INCA")

	;Mapping
	MouseClick("",$a[0]+134,$a[1]+671)
	WinWaitActive("INCA","SmartMap")

	;Smartmap
	MouseClick("",$a[0]+145,$a[1]+347)
	WinWaitActive("INCA","&SaveList")

	
	;Export map 1
	MouseClick("right",$a[0]+727,$a[1]+610)
	MouseClick("",$a[0]+727+83,$a[1]+610+68)
	MouseClick("",$a[0]+727+ 200,$a[1]+610+154)
	
	;Create new folder
	WinWaitActive("Export Spectrum in EMSA format","File &name:")
	$b = WinGetPos("Export Spectrum in EMSA format","File &name:")
	MouseClick("",$b[0]+273,$b[1]+44)
	Sleep(500)
	MouseClick("",$b[0]+122,$b[1]+81)
	WinWaitActive("Export Spectrum in EMSA format","My Documents")
	MouseClick("",$b[0]+81,$b[1]+126,2)
	WinWaitActive("Export Spectrum in EMSA format","INCA Projects")
	MouseClick("",$b[0]+337,$b[1]+46)
	WinWaitActive("Export Spectrum in EMSA format","New Folder")
	Send(""& $filename1 )
	Send("{ENTER}")
	Sleep(200)
	Send("{ENTER}")
	;Save
	ControlSend("Export Spectrum in EMSA format","File &name:", "[CLASS:Edit; INSTANCE:1]", ""& $filename1 &"_"& $beginmap)
	MouseClick("",$b[0]+395,$b[1]+225)
	WinWaitActive("INCA","&SaveList")
	
	For $i = $beginmap + 1 to $nbmap Step 1
		
		; Activate window
	WinActivate("INCA")
	WinWaitActive("INCA")

	;Find window position
	$a = WinGetPos("INCA")
		
	;Change area of interest for the next one
	MouseClick("",$a[0]+155,$a[1]+270)
	WinWaitActive("INCA","Column")
	MouseClick("",$a[0]+176+385,$a[1]+11+93)
	MouseClick("",$a[0]+118+385,$a[1]+50+93)

	;Smartmap
	MouseClick("",$a[0]+145,$a[1]+347)
	WinWaitActive("INCA","&SaveList")

	
	;Export loop
	MouseClick("right",$a[0]+727,$a[1]+610)
	Sleep(500)
	MouseClick("",$a[0]+727+83,$a[1]+610+68)
	MouseClick("",$a[0]+727+ 200,$a[1]+610+154)	
	WinWaitActive("Export Spectrum in EMSA format","File &name:")

	If $i > 9 AND $i < 100 Then
		Send(""& $filename1 &"_0"& $i)
		Send("{ENTER}")
	ElseIf $i > 99 Then
		Send(""& $filename1 &"_"& $i)
		Send("{ENTER}")
	Else    
		Send(""& $filename1 &"_00"& $i)
		Send("{ENTER}")
	EndIf
	WinWaitActive("INCA","&SaveList")
		
	Next
	
	MsgBox(0,"Export TSV","Exportation is finished")

	Exit