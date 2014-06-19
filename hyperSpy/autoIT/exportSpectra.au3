#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.0.0
 Author:         John Minter based on export_sum_spectrum by Pierre Burdet

 Script Function:
 Export 25 spectra Spectrum from INCA
 
 To do: figure out how to change directories

#ce ----------------------------------------------------------------------------


#include <Constants.au3>
#include <MsgBoxConstants.au3>

; Activate window
WinActivate("INCA")
WinWaitActive("INCA")

; $x0 = 214 ; spec 2
; $y0 = 297
$ysp  = 16 ; spacing for y for spectra
$dx1 = 123
$dy1 = 33
$dx2 = 180
$dy2 = 129
$dx3 = 795 ; dist from save window position to save button
$dy3 = 560
$pause = 10*1000; s
$hover = 250 ; ms


;Find window position
$a = WinGetPos("INCA")
; get the first spectrum position
MsgBox($MB_SYSTEMMODAL, "To do","Hover 2nd letter spc 1")
Sleep($pause)
$s0 = MouseGetPos()
$x0 = $s0[0]
$y0 = $s0[1]



For $i = 0 To 24 Step 1
   ;MsgBox($MB_SYSTEMMODAL, "Inca Pos x, y:", $a[0] & ", " & $a[1]) ;
   MouseClick("right", $x0, $y0+$i*$ysp)
   Sleep(50)
   MouseMove($x0+$dx1, $y0+$dy1+$i*$ysp)
   Sleep($hover)
   MouseMove($x0+$dx2, $y0+$dy1+$i*$ysp)
   Sleep($hover)
   MouseMove($x0+$dx2, $y0+$dy2+$i*$ysp)
   Sleep($hover)
   MouseClick("left", $x0+$dx2, $y0+$dy2+$i*$ysp)
   WinWaitActive("Save")
   $b = WinGetPos("Save")
   MouseMove($b[0]+$dx3, $b[1]+$dy3)
   Sleep($hover)
   MouseClick("left", $b[0]+$dx3, $b[1]+$dy3)
   WinWaitActive("INCA")
   ; Sleep($pause)
Next

; MsgBox($MB_SYSTEMMODAL, "To do","Hover for EMSA")

; 1st spectrum (2)
; 195,264
; 30th spectrum (32)
; 181/745
; delta = (745-264)/29  = 16.58`

