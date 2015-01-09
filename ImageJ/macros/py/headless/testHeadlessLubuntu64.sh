#!/bin/bash -e
#
# (C) 2014 John Minter. Freely use/modify under CCA License.
#
# A wrapper script to be run with bash under Ubuntu Linux x64
#  Note the use of environment variables GIT_HOME and IMG_ROOT
#   Date      Who   Ver
# ----------  ---  ----- ---------------------------------------------
# 2014-11-10  JRM  0.1.0 Initial prototype for Fiji on Lubuntu64
# 
source /etc/environment

# The standard jvm with Fiji 
JAVA_HOME="/home/shared/Fiji.app/java/linux-amd64/jdk1.6.0_24/jre"
# -Dpython.cachedir.skip=false
FIJI_APP="/home/shared/Fiji.app/ImageJ-linux64  -Dpython.cachedir.skip=false --"
IJ_MACRO="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/ijm/HelloWorldMacro.ijm"
# IJ_SCRIPT="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/py/HelloWorld.py"
IJ_SCRIPT="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessCrop.py"
# IJ_SCRIPT="${GIT_HOME}/OSImageAnalysis/ImageJ/macros/py/headless/testHeadlessVertProf.py"
BASE_DIR="${IMG_ROOT}/test/ij"
LOG_DIR="${BASE_DIR}/fiji-log"

echo  $IMG_ROOT

cd ${BASE_DIR}
rm -rf ${LOG_DIR}
[ -d fiji-log ] || mkdir fiji-log

echo \"Fiji started:\"

# --java-home ${JAVA_HOME}
# --console -macro ${IJ_MACRO}
rm -rf ${LOG_DIR}/log.txt


$FIJI_APP --java-home "/home/shared/Fiji.app/java/linux-amd64/jdk1.6.0_24/jre" --headless  --mem=1000m ${IJ_SCRIPT}   >  ${LOG_DIR}/log.txt

# cat ${LOG_DIR}/log.txt

read -p "Press [Enter] key to finish..."



