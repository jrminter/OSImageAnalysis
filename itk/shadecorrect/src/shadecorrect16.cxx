/*=========================================================================
 *
 * shadecorrect16.cxx
 * 
 * Example:
 * shadecorrect16 soft.tif soft_shade.tif
 * 
 * Correct a 16 bit TIFF image for shading produced either by non-uniform
 * illumination or thickness fluctuations in cryoTEM images of colloids
 * in vitreous ice. This version uses a DiscreteGaussianImageFilter to
 * compute the slowly varying component. We set Gaussian variance to
 * 0.25*input image size. We then normalize by dividing
 * the shade image by its maximum value. We divide each pixel in the
 * original image by the shading factor. We limit the gain boost to 10X.
 * 
 * Adapted from the ITK example MeanImageFilter by John Minter
 * 
 * Input parameters
 * 1. Input image name - assumes a 16 bit TIF
 * 2. Output image name - also a 16 bit TIF
 *
 *=========================================================================*/

#include <itkImage.h>
#include <itkImageFileReader.h>
#include <itkImageFileWriter.h>
#include <itkDiscreteGaussianImageFilter.h>
#include <itkMinimumMaximumImageCalculator.h>
#include <itkImageRegionIterator.h>

int main(int argc, char *argv[])
{
  if( argc < 3 )
  {
    std::cerr << "Usage: " << std::endl;
    std::cerr << argv[0] << 
      "  inputImageFile   outputImageFile" << std::endl;
    return EXIT_FAILURE;
  }
  const unsigned int Dimensions = 2;
  double variance;

  // do the typeDefs
  typedef itk::Image<unsigned short, Dimensions> UshortImageType;
  typedef itk::ImageFileReader< UshortImageType  >  ReaderType;
  typedef itk::ImageFileWriter< UshortImageType >  WriterType;
  typedef itk::DiscreteGaussianImageFilter<
     UshortImageType, UshortImageType >  filterType;
  typedef itk::MinimumMaximumImageCalculator<
     UshortImageType > MinMaxCalculatorType;
  typedef itk::ImageRegionConstIterator< UshortImageType > ConstIteratorType;
  typedef itk::ImageRegionIterator< UshortImageType> IteratorType;

  
  // Read input image
  ReaderType::Pointer reader = ReaderType::New();
  reader->SetFileName(argv[1]);
  reader->Update();

  UshortImageType::SizeType inputSize = 
    reader->GetOutput()->GetLargestPossibleRegion().GetSize();

  variance = (double) inputSize[0];
  variance *= 0.25;

  // Create and setup a Gaussian filter
  filterType::Pointer gaussianFilter = filterType::New();
  gaussianFilter->SetInput( reader->GetOutput() );
  gaussianFilter->SetVariance(variance);
  gaussianFilter->SetMaximumError(0.07);
  UshortImageType::Pointer output = gaussianFilter->GetOutput();
  gaussianFilter->Update();

  // Calculate the stats of the shade image
  MinMaxCalculatorType::Pointer imageCalculatorFilter
          = MinMaxCalculatorType::New ();
  imageCalculatorFilter->SetImage(output);
  imageCalculatorFilter->Compute();
  UshortImageType::PixelType minIntensity = imageCalculatorFilter -> GetMinimum( );
  UshortImageType::PixelType maxIntensity = imageCalculatorFilter -> GetMaximum( );
  
  char szLine[40];
  sprintf(szLine,"blurred: min - %d, max %d", minIntensity, maxIntensity);
  std::cerr << szLine << std::endl;

  // Create a working output image
  UshortImageType::Pointer  corrImage = UshortImageType::New();
  UshortImageType::RegionType region;
  UshortImageType::SizeType size;
  size=reader->GetOutput()->GetLargestPossibleRegion().GetSize();
  region=reader->GetOutput()->GetLargestPossibleRegion();
  corrImage->SetRegions(region);
  corrImage->Allocate();
  corrImage->FillBuffer(itk::NumericTraits<UshortImageType::PixelType>::Zero);

  // Create some iterators to use to compute the corrected image
  ConstIteratorType shadeIt( output,
    output->GetLargestPossibleRegion());
  ConstIteratorType origIt( reader->GetOutput(),
    reader->GetOutput()->GetLargestPossibleRegion());
  IteratorType  corrIt( corrImage,
    corrImage->GetLargestPossibleRegion());
  
  unsigned int uiDat;
  double dMax, dVal, dCorr, dFactor, dOrig;

  dMax = (double) maxIntensity;
  shadeIt.GoToBegin();
  origIt.GoToBegin();
  corrIt.GoToBegin();

  // we do the correction in one pass...
  while( !shadeIt.IsAtEnd() )
  {
    uiDat = shadeIt.Get();
    dVal = (double) uiDat;
    dVal /= dMax;
    if(dVal < 0.1) dVal = 0.1;
    dVal = 1.0/ dVal;
    uiDat = origIt.Get();
    dOrig = (double) uiDat;
    // calculate the shading corrected value
    dOrig *= dVal;
    dOrig = floor(dOrig + 0.5);
    if(dOrig > 65535.) dOrig=65535.;
    if(dOrig < 0.) dOrig = 0.;
    uiDat = (unsigned int) dOrig;
    corrIt.Set(uiDat);
    
    ++shadeIt;
    ++origIt;
    ++corrIt;
  }

  WriterType::Pointer writer = WriterType::New();  
  writer->SetFileName(argv[2]);
  std::cout << "Writing output... " << std::endl;
  writer->SetInput(corrImage);
  writer->Update();
 
  return EXIT_SUCCESS;
}
 
