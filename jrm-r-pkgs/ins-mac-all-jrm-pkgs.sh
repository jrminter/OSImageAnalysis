echo 
echo __install-all-jrm-r-pkgs.cmd
echo 
echo J. R. Minter Version of 2013-07-24
echo 
echo Build and install the current version of all jrm R packages
echo NOTE the environment variable %GITHOME% needs window style pathname
echo 

cd $GIT_HOME
cd "edp/R"
R CMD build Peaks
R CMD INSTALL ./Peaks_*.tar.gz
R CMD build edp
R CMD INSTALL ./edp*.tar.gz
rm -rf *.gz

cd $GIT_HOME

cd "OSImageAnalysis/jrm-r-pkgs"
R CMD build analab
R CMD INSTALL ./analab_*.tar.gz
R CMD build jrmmisc
R CMD INSTALL ./jrmmisc_*.tar.gz
R CMD build measureLines
R CMD INSTALL ./measureLines_*.tar.gz
R CMD build qAnalyst
R CMD INSTALL ./qAnalyst_*.tar.gz
R CMD build tikzDevice
R CMD INSTALL ./tikzDevice_*.tar.gz

rm -rf *.gz

echo 
echo 
read -p "Press [Enter] key to finish..."
