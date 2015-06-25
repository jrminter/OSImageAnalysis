number FixSampleID(String szImagePath, String szNewID)
{
   String szOldID
   String szBaseName = PathExtractBaseName( szImagePath, 0 );
   String szBasePath = PathExtractDirectory( szImagePath, 0 );
 
   // set to "1" to turn on debugging
   number nDebug = 0;
   Image TheImage := OpenImage(szImagePath);
   TheImage.ShowImage();
   TagGroup tgParams = TheImage.ImageGetTagGroup();
   tgParams.TagGroupGetTagAsText("Microscope Info:Specimen", szOldID)
   tgParams.TagGroupSetTagAsText("Microscope Info:Specimen", szNewID )
   Result("Reassingned from: " + szOldID + " to: " + szNewID + "\n")
   TheImage.SaveAsGatan3(szImagePath)
   DeleteImage( TheImage);
   return 1;
}

void BatchFixSampleID(void)
{
  String szLastPath = GetPersistentStringNote("Kodak:LastPath");
  String szNewSamp = GetPersistentStringNote("Kodak:LastSample");
  number bRet = GetString("Enter path To process", szLastPath, szLastPath );
  if (bRet)
  {
    SetPersistentStringNote("Kodak:LastPath", szLastPath);
    bRet = GetString("Enter new SampleID", szNewSamp, szNewSamp);
    if (bRet)
    {
      SetPersistentStringNote("Kodak:LastSample", szNewSamp);
      TagGroup tg = GetFilesInDirectory( szLastPath, 1 );
      DocumentWindow RWindow = GetDocumentWindowByTitle( "Results" );
      if (RWindow)
         WindowClose( RWindow, 0 ); 
      OpenResultsWindow( );
      number i, count = tg.TagGroupCountTags( );
      for( i = 0; i < count; ++i )  
      {
        String szLabel = tg.TagGroupGetTagLabel( i )  
        number type    = tg.TagGroupGetTagType( i, 0 )  
        if( type == 0 )
        {  
          // tag is a TagGroup
          TagGroup tgInner;
          TagGroupGetIndexedTagAsTagGroup(tg, i, tgInner );
          String szFileName;
          TagGroupGetTagAsString(tgInner, "Name", szFileName );
          String szExt = PathExtractExtension(szFileName, 0);
          if(szExt == "dm3")
          {
            String szFilePath = szLastPath + "\\" + szFileName;
            FixSampleID(szFilePath, szNewSamp)
            // Result(szFilePath + "\n" )

          }
        }
      }
    }
  }
}
BatchFixSampleID()