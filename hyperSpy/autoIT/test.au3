#include <Constants.au3>
#include <MsgBoxConstants.au3>

HotKeySet("{ESC}", "_Terminate")

SaveSpectra()

Func _Terminate()
  Exit
EndFunc   ;==>_Terminate


Func SaveSpectra()
  ; initialize a local variable
  Local $aPos = 0
  MsgBox($MB_SYSTEMMODAL, "Start", "Click on a spectrum in the AZtec Data View to save, ESC to stop loop")
  
  ; create an endless loop
  While 1
    WinWaitActive("AZtec")
    Sleep(5000)
    ; Local $aPos = MouseGetPos()
    ; MsgBox($MB_SYSTEMMODAL, "Mouse x, y:", $aPos[0] & ", " & $aPos[1])
     MouseMove(480, 703)
     MouseClick("right")
     Sleep(25)
     MouseMove(520, 739)
     Sleep(20)
     MouseClick("left")
     MouseMove(685, 765)
     MouseClick("left")
     WinWaitActive("Export")
     Sleep(50)
     MouseMove(899, 597)
     MouseClick("left")
  WEnd
EndFunc ;==> SaveSpectra