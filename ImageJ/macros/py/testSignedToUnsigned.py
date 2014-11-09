# testSignedToUnsigned.py
#
# Test function to convert between signed and unsigned
# From http://stackoverflow.com/questions/4111595/sneaking-unsigned-values-from-jython-through-java-to-c-and-back-again
# advantage of this version is that it converts to the right type
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-06  JRM 0.1.00  Initial prototype

import struct

def u2s(v, width=32):
    fmt = {8: "B", 16: "H", 32: "I", 64: "Q"}[width]
    return struct.unpack(fmt.lower(), struct.pack(fmt, v))[0]

def s2u(v, width=32):
    fmt = {8: "B", 16: "H", 32: "I", 64: "Q"}[width]
    return struct.unpack(fmt, struct.pack(fmt.lower(), v))[0]

a = 128

b = u2s(a, width=8)

print(a,b)
