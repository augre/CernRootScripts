#!/usr/bin/env python
import ROOT as r
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, pi, exp, linspace, loadtxt
from lmfit import  Model
from lmfit.models import VoigtModel, PseudoVoigtModel, LinearModel
import sys, getopt
from myTypes import Location, RootFile

def fitFunc(x, par):
    """
    The fit function to determine the parameters of the sum of three Gaussians
    """

    PDF=0.0
    g1=0.0
    g2=0.0
    g3=0.0

    #Calculate exponents of the Gaussians
    arg1=(x[0]-par[1])/par[2] if par[2]!=0 else 0.0
    arg2=(x[0]-par[3])/par[4] if par[4]!=0 else 0.0 
    arg3=(x[0]-par[5])/par[6] if par[6]!=0 else 0.0 

    # add each Gaussian contribution to the PDF
    g1= exp(-0.5*arg1*arg1)/(par[2]*sqrt(2.0*pi)) 
    g2= exp(-0.5*arg2*arg2)/(par[4]*sqrt(2.0*pi)) 
    g3= exp(-0.5*arg3*arg3)/(par[6]*sqrt(2.0*pi)) 
    PDF=par[0]*(par[7]*g1 + par[8]*g2 + (1-par[7]-par[8])*g3)

    return PDF

def main(argv):
    inputfile = 'Dosimetry_Detector_tot.root'
    outputfile = 'outputPlots.png'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    f = RootFile()
    f.loadFile()
    f.loadHist()
    f.histObj.Rebin3D(2,2,2)
    f.getNbinsXYZ()
    f.getMinXYZ()
    f.getMaxXYZ()
    f.fileObj.Print()
    
    
    print "xbins:",f.binN.x,"f.binN.y:",f.binN.y,"f.binN.z:",f.binN.z
    

    rootValXY=r.TH2D("xyPlane","xy plane",f.binN.x,f.minL.x,f.maxL.x,f.binN.y,f.minL.y,f.maxL.y)
    for y in range(0,f.binN.y):
        for x in range(0,f.binN.x):
            #print "y:",y,"x:",x
            binXY=f.histObj.GetBinContent(f.histObj.GetBin(x+1, y+1, f.binN.z/2))
            rootValXY.SetBinContent(rootValXY.GetBin(x+1,y+1), binXY)
            #print binXY
    rootValXY.Draw("cont3 same")

    c2=r.TCanvas("c2")
    rootValXY.Draw()
    c2.Print("test.png")

    c1=r.TCanvas("c1", "", 1000,1000)
    c1.Divide(1,3)
    c1.cd(1)
    
    initialBin=f.histObj.GetBin(1,f.binN.y/2,f.binN.z/2)
    print "Initial bin on x:",initialBin
    rootValX=r.TH1D("valsX","Energy deposited in 1mm cubes on X axis", f.binN.x, f.minL.x, f.maxL.x)
    for i in xrange(0,f.binN.x):
        rootValX.SetBinContent(i+1 ,f.histObj.GetBinContent(initialBin+i))
    
    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    rootValX.SetMarkerStyle(20)
    

    
    myFitFunc=r.TF1("fitFunc",fitFunc,-80,80, 9)
    myFitFunc.SetParName(0, "norm")
    myFitFunc.SetParName(1, "mu1")
    myFitFunc.SetParName(2, "sigma1")
    myFitFunc.SetParName(3, "mu2")
    myFitFunc.SetParName(4, "sigma2")
    myFitFunc.SetParName(5, "mu3")
    myFitFunc.SetParName(6, "sigma3")
    myFitFunc.SetParName(7, "frac1")
    myFitFunc.SetParName(8, "frac2")

    myFitFunc.SetParameters(1500, 5, .5, 6, 1.5, 5, 5, .4, .3)

    rootValX.Fit("fitFunc")

    rootValX.Draw("E1")
    
    c1.cd(2)
    initialBin=f.histObj.GetBin(f.binN.x/2,1,f.binN.z/2)
    print "Initial bin on y:",initialBin
    rootValY=r.TH1D("valsY","Energy deposited in 1mm cubes on Y axis", f.binN.y, f.minL.y, f.maxL.y)
    for i in xrange(0,f.binN.y):
        rootValY.SetBinContent(i+1 ,f.histObj.GetBinContent(initialBin+i*162))
    
    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    rootValY.SetMarkerStyle(20)
    
    rootValY.Fit("fitFunc")
    
    rootValY.Draw("E1")
    
    c1.cd(3)
    initialBin=f.histObj.GetBin(f.binN.x/2,f.binN.y/2,1)
    print "Initial bin on z:",initialBin
    rootValZ=r.TH1D("valsZ","Energy deposited in 1mm cubes on Z axis", f.binN.z, f.minL.z, f.maxL.z)
    for i in xrange(0,f.binN.z):
        rootValZ.SetBinContent(i+1 ,f.histObj.GetBinContent(initialBin+i*26244))
    
    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    rootValY.SetMarkerStyle(20)
    
    
    rootValZ.Fit("fitFunc")
    rootValZ.Draw("E1")
    
    c1.Print(outputfile)


if __name__ == "__main__":
       main(sys.argv[1:])
