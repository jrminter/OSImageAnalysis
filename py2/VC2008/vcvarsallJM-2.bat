@echo off

if "%1" == "" goto x86
if not "%2" == "" goto usage

if /i %1 == x86       goto x86
if /i %1 == amd64     goto amd64
if /i %1 == x64       goto amd64
if /i %1 == x86_amd64 goto x86_amd64
goto usage

:x86
echo Setting environment for using Microsoft Visual Studio 2008 x86 tools.
set VCINSTALLDIR=%~dp0VC\
set WindowsSdkDir=%~dp0WinSDK\
if not exist "%VCINSTALLDIR%bin\cl.exe" goto missing
set PATH=%VCINSTALLDIR%Bin;%WindowsSdkDir%Bin;%PATH%
set INCLUDE=%VCINSTALLDIR%Include;%WindowsSdkDir%Include;%INCLUDE%
set LIB=%VCINSTALLDIR%Lib;%WindowsSdkDir%Lib;%LIB%
set LIBPATH=%VCINSTALLDIR%Lib;%WindowsSdkDir%Lib;%LIBPATH%
goto :eof

:amd64
@rem
@rem JRM - let's set our desired directory at the end of this block
@rem Use this for systems with VCForPython27 installed
@rem This goes in C:\Users\l837410\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0
@rem
echo Setting environment for using Microsoft Visual Studio 2008 x64 tools and Anaconda Py 2.7.
set VCINSTALLDIR=%~dp0VC\
set WindowsSdkDir=%~dp0WinSDK\
if not exist "%VCINSTALLDIR%Bin\amd64\cl.exe" goto missing
set PATH=%VCINSTALLDIR%Bin\amd64;%WindowsSdkDir%Bin\x64;%WindowsSdkDir%Bin;%PATH%
set INCLUDE=%VCINSTALLDIR%Include;%WindowsSdkDir%Include;%INCLUDE%
set LIB=%VCINSTALLDIR%Lib\amd64;%WindowsSdkDir%Lib\x64;%LIB%
set LIBPATH=%VCINSTALLDIR%Lib\amd64;%WindowsSdkDir%Lib\x64;%LIBPATH%

cd C:\Users\l837410\Documents\work\py2
activate py27
echo VS2008 X64 CMD environment for Anaconda Python 2.7 set


goto :eof

:x86_amd64
echo Setting environment for using Microsoft Visual Studio 2008 x64 cross tools.
set VCINSTALLDIR=%~dp0VC\
set WindowsSdkDir=%~dp0WinSDK\
if not exist "%VCINSTALLDIR%Bin\x86_amd64\cl.exe" goto missing
set PATH=%VCINSTALLDIR%Bin\x86_amd64;%WindowsSdkDir%Bin;%PATH%
set INCLUDE=%VCINSTALLDIR%Include;%WindowsSdkDir%Include;%INCLUDE%
set LIB=%VCINSTALLDIR%Lib\amd64;%WindowsSdkDir%Lib\x64;%LIB%
set LIBPATH=%VCINSTALLDIR%Lib\amd64;%WindowsSdkDir%Lib\x64;%LIBPATH%
goto :eof

:usage
echo Error in script usage. The correct usage is:
echo     %0 [option]
echo where [option] is: x86 ^| amd64 ^| x86_amd64
echo:
echo For example:
echo     %0 x86_ia64
goto :eof

:missing
echo The specified configuration type is missing.  The tools for the
echo configuration might not be installed.
goto :eof
