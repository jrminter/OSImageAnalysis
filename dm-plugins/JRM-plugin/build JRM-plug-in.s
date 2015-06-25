/***********************************************************************
  3456789012345678901234567890123456789012345678901234567890123456789012

  Build an ATD plug-in with menu name 'JRM'

  Created JRM 2012-12-15

  Modifcation History:

    Date        Who   What...
  -----------   ---   --------------------------------------------------
  2012-12-15    JRM   Initial release
  2013-02-01    JRM   Updated clip to 16bit to change to UINT16 and
                      copy all tags and the description
  2013-05-29    JRM   Changed names to use - instead of _
                      added invertFrontimage
  2015-06-23    RRM   Added function to change the sample IDs of all
                      images in a folder.

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

   pkgName   = "ATD"

//   Get the directory of scripts to be installed

   String ParentPath, Path
   If( !SaveAsDialog("", "Go in the directory and click save", ParentPath) )
   {
      ParentPath = ParentPath.PathExtractDirectory(0)
   }
   else
   {
      ParentPath = GetSpecialDirectory(2)
   }


/******************************************************************************

   Path = ParentPath // sub-directory-name + chr(92)

   level     = 3
   IsLibrary = 1

   menu      = ""
   submenu   = ""

   scriptFile = "mylib.s"
   cmd = "My_Lib"

   AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
   InstallationLog( pkgName, scriptFile )

***********************************************************************************/


// Install scripts

   Path       = ParentPath  // sub-directory-name + chr(92)

   level      = 3
   IsLibrary  = 0

   menu       = "JRM"
   submenu    = ""

      scriptFile  = "ClipTo16bits.s"
      cmd         = "Clip to 16bits/px"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )

      scriptFile    = "LoadGlobalTagEditor.s"
      cmd           = "Edit global tags"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )

      scriptFile    = "LoadImageTagEditior.s"
      cmd           = "Edit image tags"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )

      AddScriptToPackage("Beep()",pkgName,level, "-", menu, submenu, IsLibrary) // --------- divider

      scriptFile    = "CropFrontImage.s"
      cmd           = "Crop front image"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )
      
      scriptFile    = "BatchFixSampleID.s"
      cmd           = "Fix sample IDs in folder"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )

      scriptFile    = "CropFrontImageToSquare.s"
      cmd           = "Crop front image to square"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )

      AddScriptToPackage("Beep()",pkgName,level, "-", menu, submenu, IsLibrary)

      scriptFile    = "InvertFrontImage.s"
      cmd           = "Invert Front Image"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile ) // --------- divider

      scriptFile    = "Diffractogram.s"
      cmd           = "Compute diffractogram"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )

      scriptFile    = "PeriodogramTool.s"
      cmd           = "Compute periodograms"
      AddScriptFileToPackage( path+ScriptFile, pkgName, level, cmd, menu, submenu, IsLibrary)
      InstallationLog( pkgName, scriptFile )


      AddScriptToPackage("Beep()",pkgName,level, "-", menu, submenu, IsLibrary) // --------- divider
