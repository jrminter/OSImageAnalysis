#!/bin/bash -e
# Mac's standard Java Home
# JAVA_HOME="/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home"
# Oracle's Java 7 Home
JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_71.jdk/Contents/Home"
FIJI_APP="/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx -Dpython.cachedir.skip=false --"
IJ_MACRO="/Users/jrminter/git/OSImageAnalysis/ImageJ/macros/ijm/HelloWorldMacro.ijm"
# IJ_SCRIPT="/Users/jrminter/git/OSImageAnalysis/ImageJ/macros/py/HelloWorld.py"
# IJ_SCRIPT="/Users/jrminter/git/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessCrop.py"
IJ_SCRIPT="/Users/jrminter/git/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessVertProf.py"
BASE_DIR="/Users/jrminter/dat/images/test/ij"
LOG_DIR="${BASE_DIR}/fiji-log"

rm -rf $HOME/.jlin*

cd ${BASE_DIR}
rm -rf ${LOG_DIR}
[ -d fiji-log ] || mkdir fiji-log

java -version

echo \"Fiji started:\"

# --java-home ${JAVA_HOME}
# --console -macro ${IJ_MACRO}
rm -rf ${LOG_DIR}/log.txt

$FIJI_APP --java-home ${JAVA_HOME} --headless  --mem=1000m  ${IJ_SCRIPT}  #  > ${LOG_DIR}/log.txt

# cat ${LOG_DIR}/log.txt

# rm -rf $HOME/.jlin*

read -p "Press [Enter] key to finish..."



