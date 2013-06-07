// Script file to Build the CM package
// 2008-05-29 J. R. Minter
// As written, expects package to built rel to %GIT_ROOT%

String strPkgName  = "CM";
string strMenuName = "CM"
String strSrcDir   = "%GIT_ROOT%\\OSImageAnalysis\\dm-plugins\\CM-plugin\\";
String strScript;

strScript = strSrcDir + "CM_Cathode_Tool.s";
AddScriptFileToPackage(strScript, strPkgName, 3, "Cathode_Tool", strMenuName, "" , 0);

strScript = strSrcDir + "CM_Compustage_Tool.s";
AddScriptFileToPackage(strScript, strPkgName, 3, "Compustage_Tool", strMenuName,  "" , 0);

strScript = strSrcDir + "CM_Stage_Tilt_Tool.s";
AddScriptFileToPackage(strScript, strPkgName, 3, "Stage_Tilt_Tool", strMenuName,  "" , 0);

strScript = strSrcDir + "CM_Coord_Tool.s";
AddScriptFileToPackage(strScript, strPkgName, 3, "Coord_Tool", strMenuName, "" , 0);

strScript = strSrcDir + "CM_Expose_Tool.s";
AddScriptFileToPackage(strScript, strPkgName, 3, "Expose_Tool", strMenuName, "" , 0);

