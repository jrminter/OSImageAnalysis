from ij.plugin.filter import ParticleAnalyzer as PA
import ij.measure as MEA

print(PA.ADD_TO_MANAGER)
print(PA.EXCLUDE_EDGE_PARTICLES)
print(PA.CLEAR_WORKSHEET)
print(PA.INCLUDE_HOLES)
print(PA.SHOW_OVERLAY_MASKS)
print(PA.SHOW_RESULTS)
print(PA.RECORD_STARTS)

print(PA.AREA)
print(PA.PERIMETER)
print(PA.CENTER_OF_MASS)
print(PA.CIRCULARITY)
print(PA.ELLIPSE)
print(PA.FERET)
print(PA.LABELS)
print(PA.MIN_MAX)
print(PA.MEAN)
print(PA.MODE)
print(PA.RECT)
print(PA.SHAPE_DESCRIPTORS)

mOptions = PA.AREA | PA.MEAN | PA.MODE | PA.MIN_MAX | PA.CENTER_OF_MASS | PA.PERIMETER | PA.RECT | PA.ELLIPSE | PA.SHAPE_DESCRIPTORS | PA.FERET | PA.LABELS 
# | PA.CIRCULARITY      
print(mOptions)

pOptions = PA.ADD_TO_MANAGER | PA.EXCLUDE_EDGE_PARTICLES | PA.CLEAR_WORKSHEET | PA.INCLUDE_HOLES | PA.SHOW_OVERLAY_MASKS | PA.SHOW_RESULTS

print(pOptions)
