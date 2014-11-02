#!/bin/bash -e
#
# (C) 2014 John Minter. Freely use/modify under CCA License.
#
# A wrapper script to be run with Git bash under Windows. Note the
# use of environment variables GIT_HOME and IMG_ROOT
#   Date      Who   Ver
# ----------  ---  ----- ---------------------------------------------
# 2014-11-01  JRM  0.1.0 Initial prototype for Fiji x64 on Win 7
# 

# The standard jvm with Fiji 
JAVA_HOME="/C/Apps/Fiji.app.win64/java/win64/jdk1.6.0_24/jre"
# -Dpython.cachedir.skip=false
FIJI_APP="/C/Apps/Fiji.app.win64/ImageJ-win64.exe  --console --"
IJ_MACRO="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/ijm/HelloWorldMacro.ijm"
# IJ_SCRIPT="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/py/HelloWorld.py"
IJ_SCRIPT="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessCrop.py"
# IJ_SCRIPT="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessVertProf.py"
BASE_DIR="${IMG_ROOT}/test/ij"
LOG_DIR="${BASE_DIR}/fiji-log"

rm -f "/C/Users/jrminter/AppData/Local/Temp/org.scijava.jython.shaded.jline_2_5_3.dll"

echo ${IMG_ROOT}

cd ${BASE_DIR}
rm -rf ${LOG_DIR}
[ -d fiji-log ] || mkdir fiji-log

echo \"Fiji started:\"

# --java-home ${JAVA_HOME}
# --console -macro ${IJ_MACRO}
rm -rf ${LOG_DIR}/log.txt

# java -version

$FIJI_APP --headless  --mem=1000m ${IJ_SCRIPT}   > ${LOG_DIR}/log.txt

# cat ${LOG_DIR}/log.txt

read -p "Press [Enter] key to finish..."



