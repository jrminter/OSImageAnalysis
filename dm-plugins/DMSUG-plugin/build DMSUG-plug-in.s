/***********************************************************************
  3456789012345678901234567890123456789012345678901234567890123456789012
  
  Build an DMSUG plug in
  
  Created JRM 2012-12-15

  Modifcation History:

    Date        Who   What...
  -----------   ---   --------------------------------------------------
  2012-12-15    JRM   Initial release
  2013-08-10    JRM   Format changes & add D. Mitchell Scale Bar
 
  This script is released under the Gnu Public License v.2
  http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
  
  
***********************************************************************/

void InstallationLog( String Package, String ScriptFile )
{
  Result( "\n" + "Package [" + package + "], script file [" + scriptfile + "] installed" )
  return
}

String scriptFile, pkgName, cmd, menu, submenu
Number level, IsLibrary
Number key

pkgName  = "DMSUG"

//  Get the directory of scripts to be installed

String ParentPath, Path
If( !SaveAsDialog("", "Go in the directory and click save", ParentPath) )
{; ParentPath = ParentPath.PathExtractDirectory(0); }
else
{; ParentPath = GetSpecialDirectory(2); }


/******************************************************************************

Path    = ParentPath               // sub-directory-name + chr(92)

level     = 3
IsLibrary   = 1

menu     = ""
submenu   = ""

scriptFile   = "Distortion_Analysis_Lib.s"  
cmd     = "Distortion_Analysis_Lib"

AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
InstallationLog( pkgName, scriptFile )

***********************************************************************************/


// Install scripts

Path     = ParentPath               // sub-directory-name + chr(92)
level      = 3
IsLibrary  = 0
menu       = "DMSUG"
submenu    = ""

scriptFile   = "mitchell-scale-bar.s"  
cmd          = "Scale Bar Control "
AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
InstallationLog( pkgName, scriptFile )

scriptFile   = "Close_All_ImagesNow.s"  
cmd          = "Close all images now "
AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
InstallationLog( pkgName, scriptFile )

scriptFile   = "Copy_All_Tags_Between_Images.s"  
cmd          = "Copy all tags between images "
AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
InstallationLog( pkgName, scriptFile )

scriptFile   = "Copy_All_Tags_to_Multiple_Images.s"  
cmd          = "Copy all tags between multiple images"
AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
InstallationLog( pkgName, scriptFile )

AddScriptToPackage("Beep()",pkgName,level, "-", menu, submenu, IsLibrary)    // --------- divider

scriptFile   = "Create-Image-from-ROI.s"  
cmd          = "Create an image from ROI "
AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
InstallationLog( pkgName, scriptFile )

AddScriptToPackage("Beep()",pkgName,level, "-", menu, submenu, IsLibrary)    // --------- divider
