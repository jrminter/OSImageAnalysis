# A method for deleting detectors from the detector database.
# Use with care.  Any spectra associated with this detector
# will become lost souls.
# Author:  Nicholas W. M. Ritchie
# Date:    1-Apr-2009 - Really!

# Use listDetectors() to identify the detector ie. d1, d2, ... dn


def deleteDetector(det):
   Database.deleteDetector(Database.findDetector(det.getDetectorProperties()))