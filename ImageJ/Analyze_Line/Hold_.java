		// 6. Compute the threshold for low delta fraction

		double dThr = dGrayMuLine + m_dLoThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		tIp.setThreshold(0, dThr,  ImageProcessor.NO_LUT_UPDATE);
		tImp.updateImage();
		// pa = setupAnalyzer();
		pa.analyze(tImp, tIp);
		// get the centroids in microns and convert to px
		float fX = (float) m_rt.getValue("XM", 0);
		fX /= ps;
		float fY = (float) m_rt.getValue("YM", 0);
		fY /= ps;
		int iX = (int) fX;
		int iY = (int) fY;
		tImp.show();
		IJ.doWand(iX, iY);
		m_rt.deleteRow(0);

		Roi lineRoi = tImp.getRoi();
		int nPts = lineRoi.getConvexHull().npoints;
		int iXpts[] = lineRoi.getConvexHull().xpoints;
		int iYpts[] = lineRoi.getConvexHull().ypoints;
		float xPts[] = new float[nPts];
		float yPts[] = new float[nPts];
		for (int k=0; k < nPts; k++) {
			xPts[k] = (float) iXpts[k];
			yPts[k] = (float) iYpts[k];		
		}
				
	  FloatPolygon linePolyHull = new FloatPolygon(xPts, yPts, nPts);
	  PolygonRoi hullRoi = new PolygonRoi(linePolyHull, Roi.POLYGON);
		hullRoi.setStrokeColor(Color.yellow);

		linePolyHull = hullRoi.getInterpolatedPolygon(1.0, true); // 1--- pixel spacing
		PolygonRoi interpolatedHullRoi= new PolygonRoi(linePolyHull.duplicate(), Roi.POLYGON);
		interpolatedHullRoi.setStrokeColor(Color.blue);
		
		int nHullPolyPts=linePolyHull.npoints;
		double xh[] = new double[nHullPolyPts];
		double yh[] = new double[nHullPolyPts];
		double loxr[] = new double[nHullPolyPts];
		double loyr[] = new double[nHullPolyPts];
		double loxl[] = new double[nHullPolyPts];
		double loyl[] = new double[nHullPolyPts];
		for (int i=0; i<nHullPolyPts; i++){
			loxr[i]=-9999999.0;
			loyr[i]=-9999999.0;
			loxl[i]=-9999999.0;
			loyl[i]=-9999999.0;
		}
		
		int nLoPtsL = 0;
		int nLoPtsR = 0;
		double dXt, dYt;
		
		for (int i=0; i<nHullPolyPts; i++){
			xh[i] = linePolyHull.xpoints[i];
			yh[i] = linePolyHull.ypoints[i];
			if (yh[i] > m_dGapPx){
				// keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- m_dGapPx)){
        	//keep - sep from bottom
        	dXt = (xh[i] - fX)*ps;
        	dYt = (yh[i] - fY)*ps;
        	if(dXt > 0){
        		// it is a right side
        		loxr[nLoPtsR]=dXt;
        		loyr[nLoPtsR]=dYt;
        		nLoPtsR += 1;		
        	}
        	else{
        		// it is a left side
        		loxl[nLoPtsL]=dXt;
        		loyl[nLoPtsL]=dYt;
        		nLoPtsL += 1;		
        	}
        }
			}
		}
		tImp.close();
		
		// 7. Compute the threshold for hi delta fraction

	  dThr = dGrayMuLine + m_dHiThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		tIp.setThreshold(0, dThr,  ImageProcessor.NO_LUT_UPDATE);
		tImp.updateImage();
		// pa = setupAnalyzer();
		pa.analyze(tImp, tIp);
		// get the centroids in microns and convert to px
		fX = (float) m_rt.getValue("XM", 0);
		fX /= ps;
		fY = (float) m_rt.getValue("YM", 0);
		fY /= ps;
		iX = (int) fX;
		iY = (int) fY;
		tImp.show();
		IJ.doWand(iX, iY);
		m_rt.deleteRow(0);

		lineRoi = tImp.getRoi();
		nPts = lineRoi.getConvexHull().npoints;
		iXpts = lineRoi.getConvexHull().xpoints;
		iYpts = lineRoi.getConvexHull().ypoints;
		xPts = new float[nPts];
		yPts = new float[nPts];
		for (int k=0; k < nPts; k++) {
			xPts[k] = (float) iXpts[k];
			yPts[k] = (float) iYpts[k];		
		}
				
	  linePolyHull = new FloatPolygon(xPts, yPts, nPts);
	  hullRoi = new PolygonRoi(linePolyHull, Roi.POLYGON);
		hullRoi.setStrokeColor(Color.yellow);

		linePolyHull = hullRoi.getInterpolatedPolygon(1.0, true); // 1--- pixel spacing
		interpolatedHullRoi= new PolygonRoi(linePolyHull.duplicate(), Roi.POLYGON);
		interpolatedHullRoi.setStrokeColor(Color.blue);
		
		nHullPolyPts=linePolyHull.npoints;
		xh = new double[nHullPolyPts];
	  yh = new double[nHullPolyPts];
		double hixr[] = new double[nHullPolyPts];
		double hiyr[] = new double[nHullPolyPts];
		double hixl[] = new double[nHullPolyPts];
		double hiyl[] = new double[nHullPolyPts];
		for (int i=0; i<nHullPolyPts; i++){
			hixr[i]=-9999999.0;
			hiyr[i]=-9999999.0;
			hixl[i]=-9999999.0;
			hiyl[i]=-9999999.0;
		}
		
		int nHiPtsR = 0;
		int nHiPtsL = 0;
		
		for (int i=0; i<nHullPolyPts; i++){
			xh[i] = linePolyHull.xpoints[i];
			yh[i] = linePolyHull.ypoints[i];
			if (yh[i] > m_dGapPx){
				// keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- m_dGapPx)){
        	//keep - sep from bottom
        	dXt = (xh[i] - fX)*ps;
        	dYt = (yh[i] - fY)*ps;
        	if(dXt > 0){
        		// it is a right side
        		hixr[nHiPtsR]=dXt;
        		hiyr[nHiPtsR]=dYt;
        		nHiPtsR += 1;		
        	}
        	else{
        		// it is a left side
        		hixl[nHiPtsL]=dXt;
        		hiyl[nHiPtsL]=dYt;
        		nHiPtsL += 1;		
        	}
        }
			}
		}
		tImp.close();



////

	String strLoXl, strLoYl, strLoXr, strLoYr, strMedXl, strMedYl, strMedXr, strMedYr, strHiXl, strHiYl, strHiXr, strHiYr, strLineOut;
		int nGoodPts = Math.max(nLoPtsL, nLoPtsR);
		nGoodPts = Math.max(nGoodPts, nMedPtsL);
		nGoodPts = Math.max(nGoodPts, nMedPtsR);
		nGoodPts = Math.max(nGoodPts, nHiPtsL);
		nGoodPts = Math.max(nGoodPts, nHiPtsR);
		
    try{
    	File file = new File(m_strReportPath);
    	if(!file.exists()){
		  	file.createNewFile();
    	}
			boolean bAppend = false;
   
			FileWriter fw = new FileWriter(m_strReportPath, bAppend);
			fw.write("x.lo.l, y.lo.l, x.lo.r, y.lo.r, x.med.l, y.med.l, x.med.r, y.med.r, x.hi.l, y.hi.l, x.hi.r, y.hi.r\n");
			for(int i=0; i<nGoodPts; i++){
				if(loxl[i] > -99999.0){
					strLoXl = String.format("%.5f, ", loxl[i] );
					strLoYl = String.format("%.5f, ", loyl[i] );		
				} else{
					strLoXl = "  ,";
					strLoYl = "  ,";
				}
				if(loxr[i] > -99999.0){
					strLoXr = String.format("%.5f, ", loxr[i] );
					strLoYr = String.format("%.5f, ", loyr[i] );		
				} else{
					strLoXr = "  , ";
					strLoYr = "  , ";
				}
				if(medxl[i] > -99999.0){
					strMedXl = String.format("%.5f, ", medxl[i] );
					strMedYl = String.format("%.5f, ", medyl[i] );		
				} else{
					strMedXl = "  , ";
					strMedYl = "  , ";
				}
				if(medxr[i] > -99999.0){
					strMedXr = String.format("%.5f, ", medxr[i] );
					strMedYr = String.format("%.5f, ", medyr[i] );		
				} else{
					strMedXr = "  , ";
					strMedYr = "  , ";
				}
				if(hixl[i] > -99999.0){
					strHiXl = String.format("%.5f, ", hixl[i] );
					strHiYl = String.format("%.5f, ", hiyl[i] );		
				} else{
					strHiXl = "  , ";
					strHiYl = "  , ";
				}
				if(hixr[i] > -99999.0){
					strHiXr = String.format("%.5f, ", hixr[i] );
					strHiYr = String.format("%.5f\n", hiyr[i] );		
				} else{
					strHiXr = "  , ";
					strHiYr = "  \n";
				}
				strLineOut = strLoXl + strLoYl + strLoXr + strLoYr + strMedXl + strMedYl + strMedXr + strMedYr + strHiXl + strHiYl + strHiXr + strHiYr;
				fw.write(strLineOut);
			}
			fw.close();
		}
		catch (IOException e){
			e.printStackTrace();
		}
			
		
