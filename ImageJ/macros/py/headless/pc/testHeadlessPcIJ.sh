#!/bin/bash
# Try a git bash script to run
# 2014-12-01 J. R. Minter

# The app
IJ="/C/Apps/ImageJ.app.win64/ImageJ.exe"
echo $GIT_HOME
echo $USERNAME
SCRIPT=$GIT_HOME"/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessVertProf.py"
# the offending DLL from jython
BAD_DLL="/C/Users/"$USERNAME"/AppData/Local/Temp/org.scijava.jython.shaded.jline_2_5_3.dll"
# The standard jvm with ImageJ
JAVA_HOME="C:/Program Files/Java/jdk1.6.0_45/jre"
# Current Java 1.8
# JAVA_HOME="/C/PROGRA~1/Java/jdk1.8.0_25/jre"
echo $JAVA_HOME


rm -rf $BAD_DLL


java -version

$IJ --java-home $JAVA_HOME --console $SCRIPT

rm -rf $BAD_DLL


read -p "Press [Enter] key to finish..."
