# A script for adding detectors with odd-ball properties.
# Author:  Nicholas W. M. Ritchie
# Date:    1-Apr-2009 - Really!

# Create a new detector
dd=epq.Detector.EDSDetector.createSiLiDetector(2048,10.0,135.0)
dd.getDetectorProperties().setName("Custom Detector")
dp=dd.getDetectorProperties().getProperties()

# Take-off -> 25 deg, sample-det distant -> 9.22 mm, optimal working distance-> 2.2 mm
dp.setDetectorPosition(25.0*3.1415926/180.0, 0.0, 0.00922, 0.0022)

# Set the detector to point anti-parallel to the x-axis.
dp.setArrayProperty(epq.SpectrumProperties.DetectorOrientation,[-1.0,0.0,0.0])

# Replace the gold layer with a nickel layer
dp.setNumericProperty(epq.SpectrumProperties.GoldLayer,0.0)
dp.setNumericProperty(epq.SpectrumProperties.NickelLayer,10.0)

# Set the owner to the same owner as an existing detector 
# Use "listDetectors()" to identify a detector on the same instrument as the new detector
dd.setOwner(d1.getOwner())

# Add the detector to the database
Database.addDetector(dd)

# You can view the new detector using File - Preference but don't edit the properties here
# or you risk mucking up your custom configuration.

# Use the script deleteDetector.py to remove erroneous detectors.