#!/usr/bin/env python
import ROOT as r
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, pi, exp, linspace, loadtxt
from lmfit import  Model
from lmfit.models import VoigtModel, PseudoVoigtModel, LinearModel
import sys, getopt
from myTypes import Location, RootFile
#import pdb
from fitFunctions import tripleGaussian


def main(argv):
    inputfile = 'Dosimetry_Detector_tot.root'
    outputfile = 'outputPlots.png'
    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print argv[0],'-i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print argv[0],'-i <inputfile> -o <outputfile>'
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
    f.initTH2DforXYPlane()
    f.getXYPlane()
    f.initTH1DforEachAxis()
    f.getTH1DforEachAxis()
    f.fileObj.Print()
    
    

    print "xbins:",f.binN.x,"f.binN.y:",f.binN.y,"f.binN.z:",f.binN.z
    
#    pdb.set_trace()

   
    maxxy=f.rootValXY.GetBinContent(f.rootValXY.GetMaximumBin())
    max3D=f.histObj.GetBinContent(f.histObj.GetMaximumBin())
    print "maxXY:",maxxy,"max3D",max3D
    print maxxy
    c2=r.TCanvas("c2")
    r.gStyle.SetOptStat(0)
    f.rootValXY.SetContour(10)
    f.rootValXY.DrawCopy("colz")
    f.rootValXY.Draw("cont3 same")
    f.rootValXY.Draw()
    f.rootValXY.SetLineColor(r.kRed)
    c2.Print("test.png")

#    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    

    #choose fitFunction and set up parameter names and values    
    myFitFunc=r.TF1("tripleGaussian",tripleGaussian,-80,80, 9)
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

    c1=r.TCanvas("c1", "", 1000,1000)
    c1.Divide(1,3)

    c1.cd(1)
    f.rootValX.Fit("tripleGaussian")
    f.rootValX.SetMarkerStyle(20)
    f.rootValX.Draw("E1")

    par=myFitFunc.GetParameters()
    

    print "Parameters: ",par[0],par[1],par[8]
    x=[0]
    print "y @ x=0: ", tripleGaussian(x,par )
    
    c1.cd(2)
    f.rootValY.Fit("tripleGaussian")
    f.rootValY.SetMarkerStyle(20)
    f.rootValY.Draw("E1")
    
    c1.cd(3)
    f.rootValZ.Fit("tripleGaussian")
    f.rootValZ.SetMarkerStyle(20)
    f.rootValZ.Draw("E1")
    
    c1.Print(outputfile)

    
if __name__ == "__main__":
       main(sys.argv)
