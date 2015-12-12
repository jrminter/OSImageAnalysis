import os
from ij.io import FileSaver, DirectoryChooser

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()

imagePath = basePath + os.sep + "image.tif"


print(imagePath)

