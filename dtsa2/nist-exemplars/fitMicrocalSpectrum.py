def fitMicrocalSpectrum(spec):
   while isinstance(spec,ScriptableSpectrum):
       spec=spec.wrapped
   mfd=dtsa2.MicrocalFitDialog(MainFrame,spec)
   mfd.setLocationRelativeTo(MainFrame)
   mfd.setVisible(1)
   fitter=mfd.getFitter()
   report(fitter.toHTML())
   display(fitter.toEstLinearizedSpectrum())
   fitSpec=fitter.toFitSpectrum()
   display(fitSpec)
   display(fitter.toResidualSpectrum())
   display(fitter.linearizeSpectrum(spec))
   display(fitter.linearizeSpectrum(fitSpec))
   return fitter