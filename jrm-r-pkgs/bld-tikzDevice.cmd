R CMD build tikzDevice
R CMD check tikzDevice
pause
R CMD INSTALL "./tikzDevice*.gz"
del tikzDevice*.gz
pause
