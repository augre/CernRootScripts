#!/usr/bin/env python
import ROOT as r
#import matplotlib.pyplot as plt
#import numpy as np
from math import sqrt, pi, exp
#from scipy.optimize import fmin
#from lmfit import  Model
#from lmfit.models import VoigtModel, PseudoVoigtModel, LinearModel
import sys, getopt
from os import getcwd
from myTypes import Location, RootFile
#import pdb
from fitFunctions import tripleGaussian, voigt

def printInfo(myFitFunc, axis="x"):
    #Get maximum of fit function
    fitFuncMax=myFitFunc.GetMaximum(-80,80)
    print "y max= ", fitFuncMax
    #get x value @ .9*ymax, .8*ymax, .5*ymax
    x90=myFitFunc.GetX(.9*fitFuncMax,-80, 0)
    x80=myFitFunc.GetX(.8*fitFuncMax,-80, 0)
    x50=myFitFunc.GetX(.5*fitFuncMax,-80, 0)
    x90plus=myFitFunc.GetX(.9*fitFuncMax,0, 80)
    x80plus=myFitFunc.GetX(.8*fitFuncMax,0, 80)
    x50plus=myFitFunc.GetX(.5*fitFuncMax,0, 80)
    print "90% of max value @ x= ",x90
    print "80% of max value @ x= ",x80
    print "50% of max value @ x= ",x50
    print "90% of max value @ x= ",x90plus
    print "80% of max value @ x= ",x80plus
    print "50% of max value @ x= ",x50plus
    print "\n===================================="
    print "=====Penumbra and Focal \"Point\"====="
    print "===================================="
    print axis,"axis distance from 90% to 50% on minus side is: ",x90-x50, "mm"
    print axis,"axis distance from 90% to 50% on plus side is: ",x50plus-x90plus, "mm"
    print axis,"axis distance from 90% minus to 90% plus is: ",x90plus-x90, "mm"
    print axis,"axis distance from 80% minus to 80% plus is: ",x80plus-x80, "mm"
    print "====================================\n"


def main(argv):
    currentDir=getcwd().split("/")[-1]
    inputfile = 'Dosimetry_detector_complete1_tot.root'
    outputfile = 'voigt.png'
    function=voigt
    fname="voigt"
    myFitFunc=r.TF1("voigt",function,0,120, 4)
    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:f:",["ifile=","ofile=","function="])
    except getopt.GetoptError:
        print argv[0],'-i <inputfile> -o <outputfile> -f <function>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print argv[0],'-i <inputfile> -o <outputfile> -f <function>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-f", "--function"):
            if arg == "voigt":
                function = voigt
                fname="voigt"
                myFitFunc=r.TF1("voigt",function,0,120, 4)
                myFitFunc.SetParName(0, "norm")
                myFitFunc.SetParName(1, "sigma")
                myFitFunc.SetParName(2, "lg")
                myFitFunc.SetParName(3, "max")
            elif arg == "tripleGaussian":
                function = tripleGaussian
                fname="tripleGaussian"
                myFitFunc=r.TF1("tripleGaussian",function,0,120, 9)
                myFitFunc.SetParName(0, "norm")
                myFitFunc.SetParName(1, "mu1")
                myFitFunc.SetParName(2, "sigma1")
                myFitFunc.SetParName(3, "mu2")
                myFitFunc.SetParName(4, "sigma2")
                myFitFunc.SetParName(5, "mu3")
                myFitFunc.SetParName(6, "sigma3")
                myFitFunc.SetParName(7, "frac1")
                myFitFunc.SetParName(8, "frac2")
            else:
                print "you can choose from voigt,tripleGaussian"

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    print 'Function is "', fname
    print  "working dir is ", getcwd().split("/")[-1]

    f = RootFile(fn=inputfile, hn="edepXYZ_Tot")
    f.loadFile()
    f.loadHist()
    f.histObj.Rebin3D(2,2,2)
    f.getNbinsXYZ()
    f.getMinXYZ()
    f.getMaxXYZ()
    f.initTH2DforXYPlane()
    f.getXYPlane()
    f.initTH2DforYZPlane()
    f.getYZPlane()
    f.initTH1DforEachAxis()
    f.getTH1DforEachAxis()
    f.fileObj.Print()
    
    f.writePlanesToPngFiles()

    print "f.binN.x:",f.binN.x,"f.binN.y:",f.binN.y,"f.binN.z:",f.binN.z
#    pdb.set_trace()
#    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    

    c1=r.TCanvas("c1", "", 1000,1000)
    c1.Divide(1,3)

    c1.cd(1)
    if function==tripleGaussian:
        myFitFunc.SetParameters(1500, 5, .5, 6, 1.5, 5, 5, .4, .3)
    elif function==voigt:
	maxbin=f.rootValX.GetMaximumBin()
	print "maxbin:", maxbin,"maxbincontent:",f.rootValX.GetBinContent(maxbin)
        myFitFunc.SetParameters(f.rootValX.GetBinContent(maxbin), 5, .5, maxbin)
    f.rootValX.Fit(fname, "I")
    f.rootValX.SetMarkerStyle(20)
    f.rootValX.Draw("E1")

    printInfo(myFitFunc, "x")

    c1.cd(2)
    if function==tripleGaussian:
        myFitFunc.SetParameters(150, 5, .5, 6, 1.5, 5, 5, .4, .3)
    elif function==voigt:
	maxbin=f.rootValY.GetMaximumBin()
	print "maxbin:", maxbin,"maxbincontent:",f.rootValY.GetBinContent(maxbin)
        myFitFunc.SetParameters(f.rootValY.GetBinContent(maxbin), 5, .5, maxbin)
    f.rootValY.Fit(fname, "I")
    f.rootValY.SetMarkerStyle(20)
    f.rootValY.Draw("E1")

    printInfo(myFitFunc,"y")

    c1.cd(3)
    if function==tripleGaussian:
        myFitFunc.SetParameters(1500, 5, .5, 6, 1.5, 5, 5, .4, .3)
    elif function==voigt:
	maxbin=f.rootValZ.GetMaximumBin()
	print "maxbin:", maxbin,"maxbincontent:",f.rootValZ.GetBinContent(maxbin)
        myFitFunc.SetParameters(f.rootValZ.GetBinContent(maxbin), 5, .5, maxbin)
    f.rootValZ.Fit(fname,"I")
    f.rootValZ.SetMarkerStyle(20)
    f.rootValZ.Draw("E1")

    printInfo(myFitFunc,"z")

    c1.Print(outputfile)


    
if __name__ == "__main__":
       main(sys.argv)
