`clFun` <-
function(x, sg, nSigma, cl, type = "xbar", xbarVariability = "auto", mu=NA, sigma=NA) {

  #if not "u" or "l" stops
  if(!is.element(cl, c("u", "l"))) {stop("Error! cl must be either u or l")}


  # xbar Chart
  if(type == "xbar") {

    # first case: mu and sigma are both not given (release 0.6.3, Nicola)
    if(is.na(mu) && is.na(sigma)) {
      center = mean(x, na.rm = TRUE)
      
      sgSize = as.numeric(tapply(x, sg, countFun))
      
      # define "auto" (use R if all subgroups have the same numerosity less then 7; otherwise use S)
      if(xbarVariability == "auto") {
	if (((max(sgSize)-min(sgSize)) == 0) & (sgSize[1] < 7)) {
	  xbarVariability = "r"
	} else {
	  xbarVariability = "s"
	}
      }
      
      # first subcase: use R for variability
      if (xbarVariability == "r") {
        rbar = centerFun(x=x, sg=sg, type="r")
	A2 = (nSigma/3) * getParameterFun(sgSize[1], "A2")
	# returns limits    
        if(cl == "u") clout = center + A2*rbar                                   # upper confidence limit (Montgomery, pag. 182)
        if(cl == "l") clout = center - A2*rbar                                   # lower confidence limit (Montgomery, pag. 182)
      }

      # second subcase: use S for variability
      if (xbarVariability == "s") {
        sbar = centerFun(x=x, sg=sg, type="s")
        A3 = (nSigma/3) * getCoeffFun(sgSize, "A3")
	# returns limits
        if(cl == "u") clout = center + A3*sbar                                   # upper confidence limit (Montgomery, pag. 215)
        if(cl == "l") clout = center - A3*sbar                                   # lower confidence limit (Montgomery, pag. 215)
      }
    }

    # second case: mu and sigma are both given (release 0.6.1, Nicola)
    if(!is.na(mu) && !is.na(sigma)) {
      sgSize = as.numeric(tapply(x, sg, countFun))                               # size of each subgroups
      if(cl == "u") clout = mu + (nSigma/sqrt(sgSize))*sigma                     # upper confidence limit (Montgomery, pag. 201)
      if(cl == "l") clout = mu - (nSigma/sqrt(sgSize))*sigma                     # lower confidence limit (Montgomery, pag. 201)
    }

    # third case: mu is given, sigma not
    if(!is.na(mu) && is.na(sigma)) {
      print('TO BE IMPLEMENTED') # TO BE IMPLEMENTED
    }

    # fourth case: sigma is given, mu not
    if(is.na(mu) && !is.na(sigma)) {
      print('TO BE IMPLEMENTED') # TO BE IMPLEMENTED
    }

  }


  # r Chart
  if(type == "r") {

    # first case: sigma is not given (release 0.6.3, Nicola)
    if(is.na(sigma)) {
      center = centerFun(x, sg, type = "r", mu=mu, sigma=sigma)                  # compute center line
      sgSize = table(sg)
      d2 = getCoeffFun(sgSize, "d2")
      d3 = getCoeffFun(sgSize, "d3")
      D3 = 1 - nSigma*(d3/d2)
      D4 = 1 + nSigma*(d3/d2)
      if(cl == "u") {
          clout = D4 * center                                                    # upper confidence limit (Montgomery, page 183)
          clout[clout < 0] = 0                                                   # confidence limit cannot be less than 0
        }
      if(cl == "l") {
          clout = D3 * center                                                    # lower confidence limit (Montgomery, page 183)
          clout[clout < 0] = 0                                                   # confidence limit cannot be less than 0
        }
    }

    # second case: sigma given (release 0.6.1, Nicola)
    if(!is.na(sigma)) {
	sgSize = table(sg)
        d2 = getCoeffFun(sgSize, "d2")
	d3 = getCoeffFun(sgSize, "d3")
	D1 = d2 - nSigma*d3
	D2 = d2 + nSigma*d3
        if(cl == "u") {
          clout = D2 * sigma                                                     # upper confidence limit (Montgomery, page 201)
          clout[clout < 0] = 0                                                   # confidence limit cannot be less than 0
        }
        if(cl == "l") {
          clout = D1 * sigma                                                     # lower confidence limit (Montgomery, page 201)
          clout[clout < 0] = 0                                                   # confidence limit cannot be less than 0
        }
    }

  }


  # s chart
  if(type == "s") {
    
    # first case: sigma is not given (release 0.6.3, Nicola)
    if(is.na(sigma)) {
      center = centerFun(x, sg, type = "s", mu=mu, sigma=sigma)                  # compute center line
      sgSize = table(sg)
      c4 = getCoeffFun(sgSize, "c4")
      B3 = (1-(nSigma/c4)*(sqrt(1-c4^2)))
      B4 = (1+(nSigma/c4)*(sqrt(1-c4^2)))
      if(cl == "u") {
          clout = B4 * center                                                    # upper confidence limit (Montgomery, page 214)
          clout[clout < 0] = 0                                                   # confidence limit cannot be less than 0
        }
      if(cl == "l") {
          clout = B3 * center                                                    # lower confidence limit (Montgomery, page 214)
          clout[clout < 0] = 0                                                   # confidence limit cannot be less than 0
        }
    }
    
    # second case: sigma is given (release 0.6.3, Nicola)
    if(!is.na(sigma)) {
	sgSize = table(sg)
        c4 = getCoeffFun(sgSize, "c4")
	B5 = c4 - nSigma*(sqrt(1-c4^2))
	B6 = c4 + nSigma*(sqrt(1-c4^2))
	if(cl == "u") {
          clout = B6 * sigma                                                    # upper confidence limit (Montgomery, page 213)
          clout[clout < 0] = 0                                                  # confidence limit cannot be less than 0
        }
        if(cl == "l") {
          clout = B5 * sigma                                                    # lower confidence limit (Montgomery, page 213)
          clout[clout < 0] = 0                                                  # confidence limit cannot be less than 0
        }
    }
    
  }


  # i chart (xbar chart for individual measurements)
  if(type == "i") {

    # first case: mu and sigma are both not provided (as in release 0.6.0)
    if(is.na(mu) && is.na(sigma)) {
      center = mean(na.omit(x))
      MR = centerFun(x = x, sg = sg, type="mr", sigma = sigma)
      d2 = getCoeffFun(sg+1, "d2")                  # release 0.6.1, Nicola
      UCL = center + nSigma * MR / d2               # release 0.6.1, Nicola
      LCL = center - nSigma * MR / d2               # release 0.6.1, Nicola
    }

    # second case: mu and sigma are both provided (release 0.6.1, Nicola)
    if(!is.na(mu) && !is.na(sigma)) {
      MR = centerFun(x = x, sg = sg, type="mr", sigma = sigma)
      d2 = getCoeffFun(sg+1, "d2")                  # release 0.6.1, Nicola
      d3 = getCoeffFun(sg+1, "d3")                  # release 0.6.1, Nicola
      UCL = mu + nSigma * MR * (d3/d2)              # release 0.6.1, Nicola
      LCL = mu - nSigma * MR * (d3/d2)              # release 0.6.1, Nicola
    }
    
    # third case: mu is provided, sigma not
    if(!is.na(mu) && is.na(sigma)) {
        print('TO BE IMPLEMENTED') # TO BE IMPLEMENTED
    }

    # fourth case: sigma is provided, mu not
    if(is.na(mu) && !is.na(sigma)) {
        print('TO BE IMPLEMENTED') # TO BE IMPLEMENTED
    }

    # Return output
    if(cl == "u") clout=rep(UCL,length(x))
    if(cl == "l") clout=rep(LCL,length(x))
    
  }


  # mr chart
  if(type == "mr") {                     
    #recalculates center kline
    #see when interval is used
    MR = centerFun(x = x, sg = sg, type = "mr", sigma = sigma)
    #calcola i limiti centrali
    d2 = getCoeffFun(sg+1, "d2")
    d3 = getCoeffFun(sg+1, "d3")
    UCL = MR + nSigma * (d3/d2) * MR
    LCL = MR - nSigma * (d3/d2) * MR
    LCL = ifelse(LCL < 0, 0, LCL)
    if(cl == "u") clout=rep(UCL,length(x))
    if(cl == "l") clout=rep(LCL,length(x))
  }


  # p chart
  if(type == "p") {
    # compute center line
    pbar = centerFun(x = x, sg = sg, type = "p", mu = mu)
    # compute control limits
    UCL = pbar + nSigma*sqrt((pbar*(1-pbar))/sg)
    LCL = pbar - nSigma*sqrt((pbar*(1-pbar))/sg)
    LCL = ifelse(LCL < 0, 0, LCL)   # non negativity
    if(cl == "u") clout=UCL
    if(cl == "l") clout=LCL
  }


  # np chart
  if(type == "np")  {
    #calculates pbar
    #for npbar
    if(is.na(mu)) {
      pbar  = centerFun(x = x, sg = sg, type = "p")
      
    } else {
      pbar = mu / sg
    }
    #calculates UCL
    UCL = (sg*pbar) + nSigma*sqrt((sg*pbar)*(1-pbar))
    LCL = (sg*pbar) - nSigma*sqrt((sg*pbar)*(1-pbar))
    LCL = ifelse(LCL < 0, 0, LCL)   # non negativity
    if(cl == "u") clout=UCL
    if(cl == "l") clout=LCL
  }


  # c chart
  if(type == "c") {
    cline=centerFun(x = x, sg = sg, type = "c", mu = mu)
    UCL = cline + nSigma*sqrt(cline)
    LCL = cline - nSigma*sqrt(cline)
    LCL = ifelse(LCL < 0, 0, LCL)   # non negativity
    if(cl == "u") clout=rep(UCL,length(x))
    if(cl == "l") clout=rep(LCL,length(x))
  }


  # u chart
  if(type == "u") {
    cline=centerFun(x=x, sg=sg, type="u", mu = mu)
    UCL = cline + nSigma*sqrt(cline/sg)
    LCL = cline - nSigma*sqrt(cline/sg)
    LCL = ifelse(LCL < 0, 0, LCL)   # non negativity
    if(cl == "u") clout=UCL
    if(cl == "l") clout=LCL
  }

  # Return output
  return(clout)

}

