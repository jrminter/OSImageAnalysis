import subprocess
import os

ij_exe = 'C:\\Apps\\ImageJ\\ImageJ.exe'
ij_scr = 'C:\\Users\\jrminter\\Documents\\git\\OSImageAnalysis\\ImageJ\\macros\\ijm\\crunch\\RandomOvals.ijm'
png_fi = 'C:\\Users\\jrminter\\Documents\\git\\OSImageAnalysis\\ImageJ\\output\\random_ovals.png'
# remover the old image file
os.remove(png_fi)
subprocess.call([ij_exe, ij_scr])
