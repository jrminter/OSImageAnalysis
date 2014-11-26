## CheapEasy DIY BARCODE GENERATOR ##
## By Rob Colautti - UBC Botany (Loren Rieseberg Lab)
## Uses Code128 Barcodes
## Useful info about this on Wikipedia: http://en.wikipedia.org/wiki/Code_128

## INSTRUCTIONS: ##
## Upload a list of labels (labels.csv)
## Technically there is no limit to the length of the label
## BUT you can only squeeze so many pixels in a small area
## Double-check settings, below
## WHEN YOU PRINT: Check that you are printing 'actual size' and not 'fit' or 'shrink to fit page'


## What you get: ##
## Output pdf of barcodes for printing on:
## 0.5"x1.75" Worth Poly Label WP0517 (Polyester Label Stock); For other formats you can change the pdf and par settings below

## USER SETTINGS ##
setwd("C:/Users/Alliaria/Documents/Barcode Generator") # Set your working directory here
blankgraphs=0 # Change if you want to add blank labels to the beginning (e.g. use a sheet that already has a few labels printed)
MaxLength<-15 # This is the maximum barcode length; max=15 for the WORTHData Tricoder scanners in the Rieseberg lab

Barcodes<-read.csv("barcodes128.csv") ## This maps each ASCII character to its barcode; download from the Rieseberg lab blog
Labels<-read.csv("labels.csv",header=F) ## This is a file you created that contains your labels
AddLegend<-T ## Adds name of label to bottom of barcode.
StartCode<-209 # 208-Start Code A, 209-Start Code B, 210-Start Code C ; see Wikipedia for details

Labels$Barcode<-0 # This will add a column to store binary codes for each label, i.e. a binary representation of the barcode
for (i in 1:nrow(Labels)){  # Create binary representation of barcode for each label in Labels:
  Bincode<-0 # This will be the binary code for the label
  CheckCalc<-0 # Need this to keep track of characters to calculate check code
  LabChars<-unlist(strsplit(as.character(Labels[i,1]),split=""))
  for (j in 1:length(LabChars)){ # For each character in Labels[i]
    CheckCalc<-CheckCalc+(grep(utf8ToInt(LabChars[j]),Barcodes[,1])-1)*j
    # Convert Character to UTF-8 ASCII code and find corresponding binary in Barcodes file
    DrawCode<-Barcodes[grep(utf8ToInt(LabChars[j]),Barcodes[,1]),2]
    # And append
    Bincode<-paste(Bincode,DrawCode,sep="")
  }
  CheckCalc<-CheckCalc+(grep(StartCode,Barcodes[,1])-1) # Add start code value to calculation (again see Wikipedia for details)
  # Now put together the label barcode by adding the extras
  Labels$Barcode[i]<-paste(c(1:(10)*0),collapse="") # 'Quiet zone' - see Wikipedia entry
  Labels$Barcode[i]<-paste(Labels$Barcode[i],Barcodes[grep(paste(StartCode),Barcodes[,1]),2],sep="") # Add Start code
  Labels$Barcode[i]<-paste(Labels$Barcode[i],Bincode,sep="") # Add Binary code for label
  CheckCode<-CheckCalc-trunc(CheckCalc/103)*103 # Calculate check code
  Labels$Barcode[i]<-paste(Labels$Barcode[i],Barcodes[CheckCode+1,2],sep="") # Add check code binary
  Labels$Barcode[i]<-paste(Labels$Barcode[i],"1100011101011",sep="") # Add Stop code 
  Labels$Barcode[i]<-paste(Labels$Barcode[i],paste(c(1:(10)*0),collapse=""),sep="") # Add second quiet zone
}

## Now draw barcode

pdf(file="BarcodesOut.pdf",width=8.5,height=11,pointsize=12,onefile=T)

par(mfrow=c(20,4),omi=c(0.511811,0.275591,0.511811,0),mai=c(0.0787402,0.0787402,0.0787402,0.3937012),lend="square",lmitre=1)  # Set up output

if (blankgraphs>0){
 for (j in 1:blankgraphs){
   plot(0,0,col="white",xlab="",ylab="",axes=F)
 }
}
for (i in 1:nrow(Labels)){
 BarLength<-nchar(Labels$Barcode[i]) # Calculates length of barcode (i.e. number of 1s and 0s)
 if (nchar(as.vector(Labels[i,1])) <= MaxLength){ ## Make sure Barcode label is not too long
  plot(0,0,col="white",xlab="",ylab="",axes=F,xlim=c(0,BarLength),ylim=c(0,1))
  xpos<-0 # Resets the drawing position for vertical lines of each barcode
  BinCode<-as.numeric(unlist(strsplit(as.character(Labels$Barcode[i]), split="")))
  for (j in 1:length(BinCode)){ # For each binary digit
    lines(c(xpos,xpos),c(0,1),col=rgb(1-BinCode[j],1-BinCode[j],1-BinCode[j],1),lwd=140/length(BinCode))
    xpos<-xpos + 1 # Move over to get ready for the next line
  }
  if (AddLegend==T){
    rect(30,-5,BarLength-30,0.3,col="white",border="white")
    text(BarLength/2,0.1,Labels[i,1])
  }
 }
 if (nchar(as.vector(Labels[i,1])) > MaxLength){
  plot(0,0,col="white",xlab="",ylab="",axes=F,xlim=c(0,BarLength),ylim=c(0,1))
  rect(30,-5,BarLength-30,0.3,col="white",border="white")
  text(BarLength/2,0.6,Labels[i,1])
  text(BarLength/2,0.1,"CODE TOO LONG")   
 } 
}
dev.off()

