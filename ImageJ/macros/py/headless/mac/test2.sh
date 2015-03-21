#!/bin/bash -e
#
# 2015-03-20 JRM  Testing...
# Oracle's Java 7 Home
JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_75.jdk/Contents/Home"
# try a plain console
FIJI_APP="/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx -Dpython.console=org.python.core.PlainConsole  --"
IJ_SCRIPT="/Users/jrminter/git/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessVertProf.py"
BASE_DIR="/Users/jrminter/dat/images/test/ij"

echo \"Fiji run 1 started:\"
$FIJI_APP --java-home ${JAVA_HOME} --headless  --mem=1000m  ${IJ_SCRIPT} 
