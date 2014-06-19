#include <Constants.au3>
#include <MsgBoxConstants.au3>

; Activate window
WinActivate("INCA")
WinWaitActive("INCA")

$x0 = 214 ; spec 2
$y0 = 297
$dx1 = 123
$dy1 = 33
$dx2 = 180
$dy2 = 129
$dx3 = 795 ; dist from save window position to save button
$dy3 = 560
$pause = 5*1000; s
$hover = 250 ; ms


;Find window position
$a = WinGetPos("INCA")


MouseClick("right", $x0, $y0)
Sleep(50)
MouseMove($x0+$dx1, $y0+$dy1)
Sleep($hover)
MouseMove($x0+$dx2, $y0+$dy1)
Sleep($hover)
MouseMove($x0+$dx2, $y0+$dy2)
Sleep($hover)
MouseClick("left", $x0+$dx2, $y0+$dy2)
Sleep($pause)
WinWaitActive("Save")
$b = WinGetPos("Save")
MouseMove($b[0]+$dx3, $b[1]+$dy3)
Sleep($hover)
MouseClick("left", $b[0]+$dx3, $b[1]+$dy3)

; MsgBox($MB_SYSTEMMODAL, "Save Pos x, y:", $b[0] & ", " & $b[1]) ;
; MsgBox($MB_SYSTEMMODAL, "To do","Hover for save button")
;Sleep($pause)
; 1st spectrum (2)
; 195,264
; 30th spectrum (32)
; 181/745
; delta = (745-264)/29  = 16.58`
; $aPos = MouseGetPos()
; MsgBox($MB_SYSTEMMODAL, "Save x, y:", $aPos[0] & ", " & $aPos[1])
