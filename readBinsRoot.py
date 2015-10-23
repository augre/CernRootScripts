#!/usr/bin/env python
import ROOT as r
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, pi, exp, linspace, loadtxt
from scipy.optimize import fmin
#from lmfit import  Model
#from lmfit.models import VoigtModel, PseudoVoigtModel, LinearModel
import sys, getopt
from myTypes import Location, RootFile
#import pdb
from fitFunctions import tripleGaussian, findInverseValueTriple, voigt


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
#    myFitFunc=r.TF1("tripleGaussian",tripleGaussian,-80,80, 9)
#    myFitFunc.SetParName(0, "norm")
#    myFitFunc.SetParName(1, "mu1")
#    myFitFunc.SetParName(2, "sigma1")
#    myFitFunc.SetParName(3, "mu2")
#    myFitFunc.SetParName(4, "sigma2")
#    myFitFunc.SetParName(5, "mu3")
#    myFitFunc.SetParName(6, "sigma3")
#    myFitFunc.SetParName(7, "frac1")
#    myFitFunc.SetParName(8, "frac2")

#    myFitFunc.SetParameters(1500, 5, .5, 6, 1.5, 5, 5, .4, .3)

    myFitFunc=r.TF1("voigt",voigt,-80,80, 3)
    myFitFunc.SetParameters(500, 5, .5, )
    c1=r.TCanvas("c1", "", 1000,1000)
    c1.Divide(1,3)

    c1.cd(1)
    f.rootValX.Fit("voigt")
    f.rootValX.SetMarkerStyle(20)
    f.rootValX.Draw("E1")

#    #Get maximum of fit function
#    par=myFitFunc.GetParameters()
#    fitFuncMax=fmin(lambda x: -tripleGaussian(x, par), -80)
#    print fitFuncMax
#    #get x value @ .9*y and .5*y
#    x90=findInverseValueTriple(.9*tripleGaussian(fitFuncMax,par), par,-80, 80 )
#    x50=findInverseValueTriple(.5*tripleGaussian(fitFuncMax,par), par,-80, 80 )
#    x90plus=findInverseValueTriple(.9*tripleGaussian(fitFuncMax,par), par,80, -80, -1)
#    x50plus=findInverseValueTriple(.5*tripleGaussian(fitFuncMax,par), par,80, -80, -1)
#    print "90% of y max @ x= ",x90
#    print "50% of y max @ x= ",x50
#    print "90% of y max @ x= ",x90plus
#    print "50% of y max @ x= ",x50plus
#    print "x axis distance from 90% to 50% on minus side is: ",x90[0]-x50[0], "mm"
#    print "x axis distance from 90% to 50% on plus side is: ",x50plus[0]-x90plus[0], "mm"
#    print "x axis distance from 90% minus to 90% plus is: ",x90plus[0]-x90[0], "mm"

    c1.cd(2)
    f.rootValY.Fit("voigt")
    f.rootValY.SetMarkerStyle(20)
    f.rootValY.Draw("E1")

#    #Get maximum of fit function
#    par=myFitFunc.GetParameters()
#    fitFuncMax=fmin(lambda x: -tripleGaussian(x, par), -80)
#    print fitFuncMax
#    #get x value @ .9*y and .5*y
#    x90=findInverseValueTriple(.9*tripleGaussian(fitFuncMax,par), par,-80, 80 )
#    x50=findInverseValueTriple(.5*tripleGaussian(fitFuncMax,par), par,-80, 80 )
#    x90plus=findInverseValueTriple(.9*tripleGaussian(fitFuncMax,par), par,80, -80, -1)
#    x50plus=findInverseValueTriple(.5*tripleGaussian(fitFuncMax,par), par,80, -80, -1)
#    print "90% of y max @ x= ",x90
#    print "50% of y max @ x= ",x50
#    print "90% of y max @ x= ",x90plus
#    print "50% of y max @ x= ",x50plus
#    print "y axis distance from 90% to 50% is: ",x90[0]-x50[0], "mm"
#    print "y axis distance from 90% to 50% on plus side is: ",x50plus[0]-x90plus[0], "mm"
#    print "y axis distance from 90% minus to 90% plus is: ",x90plus[0]-x90[0], "mm"


    c1.cd(3)
    f.rootValZ.Fit("voigt")
    f.rootValZ.SetMarkerStyle(20)
    f.rootValZ.Draw("E1")

#    #Get maximum of fit function
#    par=myFitFunc.GetParameters()
#    fitFuncMax=fmin(lambda x: -tripleGaussian(x, par), -80)
#    print fitFuncMax
#    #get x value @ .9*y and .5*y
#    x90=findInverseValueTriple(.9*tripleGaussian(fitFuncMax,par), par,-80, 80 )
#    x50=findInverseValueTriple(.5*tripleGaussian(fitFuncMax,par), par,-80, 80 )
#    x90plus=findInverseValueTriple(.9*tripleGaussian(fitFuncMax,par), par,80, -80, -1)
#    x50plus=findInverseValueTriple(.5*tripleGaussian(fitFuncMax,par), par,80, -80, -1)
#    print "90% of y max @ x= ",x90
#    print "50% of y max @ x= ",x50
#    print "90% of y max @ x= ",x90plus
#    print "50% of y max @ x= ",x50plus
#    print "z axis distance from 90% to 50% is: ",x90[0]-x50[0], "mm"
#    print "z axis distance from 90% to 50% on plus side is: ",x50plus[0]-x90plus[0], "mm"
#    print "z axis distance from 90% minus to 90% plus is: ",x90plus[0]-x90[0], "mm"


    c1.Print(outputfile)

    
if __name__ == "__main__":
       main(sys.argv)
