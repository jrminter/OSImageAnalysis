#!/bin/bash
# Try a git bash script to run
# 2014-11-28 J. R. Minter

# The app
FIJI="/C/Apps/Fiji.app.win64/ImageJ-win64.exe"
echo $GIT_HOME
SCRIPT=$GIT_HOME"/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessVertProf.py"
# the offending DLL from jython
BAD_DLL="/C/Users/jrminter/AppData/Local/Temp/org.scijava.jython.shaded.jline_2_5_3.dll"
# The standard jvm with Fiji 
# JAVA_HOME="/C/Apps/Fiji.app.win64/java/win64/jdk1.6.0_24/jre"
# Current Java 1.8
JAVA_HOME="/C/PROGRA~1/Java/jdk1.8.0_25/jre"


rm -rf $BAD_DLL

java -version

$FIJI --java-home $JAVA_HOME --console --headless $SCRIPT

rm -rf $BAD_DLL


read -p "Press [Enter] key to finish..."
