#!/bin/sh
# Kota Miura  2013-12-02
# https://gist.github.com/cmci/7751712
JAVA_HOME=/g/almf/software/bin/java/jdk1.6.0_22

PATH=${PATH}:${JAVA_HOME}/bin

FIJI=/g/almf/software/fiji/ImageJ-linux64

FIJI_SCRIPT=/g/almf/software/scripts2/getIntensityRange.py

IMG=/g/data/bio-it_centres_course/data/VSVG/0076-14--2006-01-23/data/--W00100--P00001--Z00000--T00000--nucleus-dapi.tif
java -version
${FIJI} --mem=1000m  ${FIJI_SCRIPT} ${IMG}
