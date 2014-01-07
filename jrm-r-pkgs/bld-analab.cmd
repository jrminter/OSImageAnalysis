R CMD build analab
R CMD check analab
R CMD INSTALL "./analab*.tar.gz"

pause

del analab*.gz
RD /S /Q analab.Rcheck

pause
