`centerFun` <-
function(x, sg, type = "xbar", mu=NA, sigma=NA) {


  dfTemp=cbind(x,sg)
    

  # xbar central line
  if(type == "xbar") {

    # first case: mu is not provided (as in release 0.6.0)	
    if (is.na(mu)) {
      center = mean(x, na.rm = TRUE)
    } 

    # second case: mu is provided (release 0.6.1, Nicola)
    else {
      center = mu
    }

  }


  # r chart
  if(type=="r") {

    # first case: sigma is not provided (as in release 0.6.0)	
    if (is.na(sigma)) {
      sgSize = tapply(x,sg,countFun)
      
      # first case: all subgroups have the same numerosity (as in release 0.6.0)
      if((max(sgSize)-min(sgSize)) == 0) {
        rangesCampionari = tapply(x,sg,rFun)
        rangesCampionari[is.nan(rangesCampionari)] = NA
        center = mean(rangesCampionari, na.rm=TRUE)
      }
      
      # second case: all subgroups don't have the same numerosity (release 0.6.2, Nicola)
      else {
        sdCampionari = tapply(x,sg,sd,na.rm=TRUE)
        sdCampionari[is.nan(sdCampionari)] = NA
        sgSize = tapply(x,sg,countFun)
        numFormula = sum(sdCampionari^2*(sgSize-1),na.rm=TRUE)
        m = length(unique(sg))
        denFormula = sum(sgSize)-m
        sigma = (numFormula/denFormula)^0.5
        center = sigma * getCoeffFun(sgSize, "d2")
      }
    } 

    # second case: sigma is provided (release 0.6.1, Nicola)
    else {
      sgSize = table(sg)                                                     # size of each subgroups
      center = sigma * getCoeffFun(sgSize, "d2")                             # compute center line
    }

  }


  # s chart
  if(type=="s") {

    # first case: sigma is not provided (as in release 0.6.0)	
    if (is.na(sigma)) {
      sdCampionari = tapply(x,sg,sd,na.rm=TRUE)
      sdCampionari[is.nan(sdCampionari)] = NA
      sgSize = tapply(x,sg,countFun)
      # montgomery pp 189
      numFormula = sum(sdCampionari^2*(sgSize-1),na.rm=TRUE)
      m = length(unique(sg))
      denFormula = sum(sgSize)-m
      center = (numFormula/denFormula)^0.5
    }

    # second case: sigma is provided (release 0.6.1, Nicola)
    else {
      sgSize = table(sg)                                                     # size of each subgroups
      center = sigma * getCoeffFun(sgSize, "c4")                             # compute center line
    }

  }


  # i chart
  if(type=="i") {

    # first case: mu is not provided (release 0.6.1, Nicola)
    if(is.na(mu)) {
      center = mean(na.omit(x))
    }

    # second case: mu is provided (release 0.6.1, Nicola)
    else {
      center = mu        
    }
  }


  # mr chart
  if(type=="mr") {

    # first case: sigma is not provided (release 0.6.1, Nicola)
    if(is.na(sigma)) {
      #sg is range length
      center = mean(na.omit(mrangeFun(x,sg=sg)))
      #### La formula sopra e' come in Montgomery (pag. 202). Lascio commentato lo script della release 0.6.0
      #d2=getCoeffFun(sg+1, "d2")
      #come vuole
      #center=center/d2
    } 

    # second case: sigma is provided (release 0.6.1, Nicola)
    else {
      d2 = getCoeffFun(sg+1, "d2")
      center = sigma * d2
    }

  }


  # p chart
  if(type=="p") {

    # first case: mu is not provided (release 0.6.1, Nicola)
    if(is.na(mu)) { # as in release (0.6.0)
      sumX=sum(na.omit(x))
      #in attributes chart sg is a vector contsaining
      #sample dimension
      sumN=sum(na.omit(sg))
      pLine=sumX/sumN
      center=pLine
    }

    # second case: mu is provided (release 0.6.1, Nicola)
    else {
      center = mu
    }
 
  } 


  # np chart
  if(type=="np") {

    # first case: mu is not provided (release 0.6.1, Nicola)
    if(is.na(mu)) { # as in release (0.6.0)
      #central line equal mean(x).
      center = mean(na.omit(x))
    }

    # second case: mu is provided (release 0.6.1, Nicola)
    else {
      center = mu
    }

  }


  # c chart
  if(type=="c") {

    # first case: mu is not provided (release 0.6.1, Nicola)
    if(is.na(mu)) { # as in release (0.6.0)
      #central line equal mean(x).
      center = mean(na.omit(x))
    }

    # second case: mu is provided (release 0.6.1, Nicola)
    else {
      center = mu
    }

  }


  # u chart
  if(type=="u") {

    # first case: mu is not provided (release 0.6.1, Nicola)
    if(is.na(mu)) { # as in release (0.6.0)
      sumX=sum(na.omit(x))
      #checks
      sumN=sum(na.omit(sg))
      uLine=sumX/sumN
      center=uLine
    }

    # second case: mu is provided (release 0.6.1, Nicola)
    else {
      center = mu
    }

  }

  # Return output
  return(center)
}

