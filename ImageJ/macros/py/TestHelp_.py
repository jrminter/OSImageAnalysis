from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import java.lang as jl
import java.io as jio
import java.util as ju
import jarray
import sys as sys

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager


def helpStr(arg, recurse=True):
  """javaArgs(javaMethod)
  Outputs the various different call syntaxes available for the specified java method."""
  res=""
  da=dir(arg)
  # Has a doc string, return a doc string....
  if ('__doc__' in da) and (arg.__doc__ != None):
    return str(arg.__doc__)
  if ('__class__' in da):
    cn=str(arg.__class__)
    if (cn=="<type 'instancemethod'>"):
      # Java instance method, return an arglist
      res = "Java Method:"
      if "argslist" in da:
        i = 1
        for arg in arg.argslist:
          if arg != None:
            res = "%s\n Style %d\n  %s" % (res, i, arg.data)
            i = i + 1
      else:
        res = "%s\n No arguments: %s()" % (res, arg.__name__)
    elif(cn=="<type 'java.lang.Class'>"):
      res = "Java class: %s" % (str(arg)[7,-2])
      for m in da:
        if (not str(m).startswith("_")) and recurse:
          tmp.append(helpStr(eval("%s.%s" % (arg, m)),False))
      if len(tmp)>0:
        res = "%s\nMethods:\n\t%s" % (res,"\n\t".join(tmp))
    elif cn.startswith("<type '"):
      res = "%sInstance of Java class %s" % (res,cn[7:-2])
      tmp=[]
      for m in da:
        if (not str(m).startswith("_")) and recurse:
          tmp.append(helpStr(eval("%s.%s" % (arg, m)),False))
      if len(tmp)>0:
        res = "%s\nMethods:\n\t%s" % (res,"\n\t".join(tmp))
    elif cn.startswith("<class '"):
      res = "%sInstance of Python class %s" % (res,cn[8:-2])
      tmp=[]
      for m in da:
        if (not str(m).startswith("_")) and recurse:
          tmp.append(helpStr(eval("%s.%s" % (arg,m)),False))
      res = "%s\nMethods:\n\t%s" % (res,"\n\t ".join(tmp))
    else:
      if len(res)==0:
        res = "No help available"#  for %s" % str(arg)
  return res

def help(arg=None):
  """help(arg)
  Displays ?useful? information about 'arg'"""
  if arg:
    print helpStr(arg,True)
  else:
    print __doc__

print(dir(IJ))

# print(help(IJ.runMacro))
print(help(IJ.showTime))