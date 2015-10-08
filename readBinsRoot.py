#!/usr/bin/env python
import ROOT as r
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, pi, exp, linspace, loadtxt
from lmfit import  Model
from lmfit.models import VoigtModel, PseudoVoigtModel, LinearModel
import sys, getopt

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


    f = r.TFile(inputfile)
    hist3D=f.Get("h3D_Dose_t")
    f.Print()
    
    hist3D.Rebin3D(2,2,2)
    
    binx=hist3D.GetNbinsX()
    biny=hist3D.GetNbinsY()
    binz=hist3D.GetNbinsZ()
    print "xbins:",binx,"biny:",biny,"binz:",binz
    minx=hist3D.GetXaxis().GetXmin()
    miny=hist3D.GetYaxis().GetXmin()
    minz=hist3D.GetZaxis().GetXmin()
    maxx=hist3D.GetXaxis().GetXmax()
    maxy=hist3D.GetYaxis().GetXmax()
    maxz=hist3D.GetZaxis().GetXmax()
    

    rootValXY=r.TH2D("xyPlane","xy plane",biny,miny,maxy,binz,minz,maxz)
    for y in range(0,biny):
        for x in range(0,binx):
            #print "y:",y,"x:",x
            binXY=hist3D.GetBinContent(hist3D.GetBin(x+1, y+1, binz/2))
            rootValXY.SetBinContent(rootValXY.GetBin(x+1,y+1), binXY)
            #print binXY
    rootValXY.Draw()

    c2=r.TCanvas("c2")
    rootValXY.Draw()
    c2.Print("test.png")

    c1=r.TCanvas("c1", "", 1000,1000)
    c1.Divide(1,3)
    c1.cd(1)
    
    initialBin=hist3D.GetBin(1,biny/2,binz/2)
    print "Initial bin on x:",initialBin
    rootValX=r.TH1D("valsX","Energy deposited in 1mm cubes on X axis", binx, minx, maxx)
    #valuesOnX=[]
    for i in xrange(0,binx):
    #    valuesOnX.append(hist3D.GetBinContent(initialBin+i))
        rootValX.SetBinContent(i+1 ,hist3D.GetBinContent(initialBin+i))
    
    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    rootValX.SetMarkerStyle(20)
    

    #fitFcn=r.TF1("fitFcn","[0]*TMath::Voigt(x, [1],[2], 4)",-80,80)
    #fitFcn.SetParameter(0, 1.0)
    #fitFcn.SetParameter(1, 1.0)
    #fitFcn.SetParameter(2, 1.0)
    #fitFcn.SetLineWidth(4)
    #fitFcn.SetLineColor(r.kMagenta)
    #rootValX.Fit("fitFcn")
    
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

    #rootValX.Fit("fitFunc")

    rootValX.Draw("E1")
    
    c1.cd(2)
    initialBin=hist3D.GetBin(binx/2,1,binz/2)
    print "Initial bin on y:",initialBin
    rootValY=r.TH1D("valsY","Energy deposited in 1mm cubes on Y axis", biny, miny, maxy)
    #valuesOnY=[]
    for i in xrange(0,biny):
    #    valuesOnY.append(hist3D.GetBinContent(initialBin+i*162))
        rootValY.SetBinContent(i+1 ,hist3D.GetBinContent(initialBin+i*162))
    
    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    rootValY.SetMarkerStyle(20)
    
    #fitFcnY=r.TF1("fitFcnY","[0]*TMath::Voigt(x, [1],[2], 4)",-80,80)
    #fitFcnY.SetParameter(0, 3.0)
    #fitFcnY.SetParameter(1, 1.0)
    #fitFcnY.SetParameter(2, 1.0)
    #fitFcnY.SetLineWidth(4)
    #fitFcnY.SetLineColor(r.kMagenta)
    #rootValY.Fit("fitFcnY")

    rootValY.Fit("fitFunc")
    
    rootValY.Draw("E1")
    
    c1.cd(3)
    initialBin=hist3D.GetBin(binx/2,biny/2,1)
    print "Initial bin on z:",initialBin
    rootValZ=r.TH1D("valsZ","Energy deposited in 1mm cubes on Z axis", binz, minz, maxz)
    #valuesOnZ=[]
    for i in xrange(0,binz):
    #    valuesOnZ.append(hist3D.GetBinContent(initialBin+i*26244))
        rootValZ.SetBinContent(i+1 ,hist3D.GetBinContent(initialBin+i*26244))
    
    r.gStyle.SetEndErrorSize(3)
    r.gStyle.SetErrorX(0.)
    rootValY.SetMarkerStyle(20)
    
    #fitFcnZ=r.TF1("fitFcnZ","[0]*TMath::Voigt(x, [1],[2], 4)",-80,80)
    #fitFcnZ.SetParameter(0, 1.0)
    #fitFcnZ.SetParameter(1, 1.0)
    #fitFcnZ.SetParameter(2, 1.0)
    #fitFcnZ.SetLineWidth(4)
    #fitFcnZ.SetLineColor(r.kMagenta)
    #rootValZ.Fit("fitFcnZ")
    
    rootValZ.Fit("fitFunc")
    rootValZ.Draw("E1")
    
    c1.Print(outputfile)

    #valuesOnX=np.array(valuesOnX)
    #valuesOnY=np.array(valuesOnY)
    #valuesOnZ=np.array(valuesOnZ)
    #gmod =  PseudoVoigtModel()
    ##line_mod = LinearModel(prefix='line_')
    #
    #t1=np.arange(0, 160)
    #
    #
    #pars=gmod.guess(valuesOnX,x=t1 )
    ##pars+=line_mod.make_params(intercept=1)
    ##line_mod+=gmod
    #result = gmod.fit(valuesOnX, pars,x=t1)
    #resultP=list(result.params.valuesdict().items())
    #report=result.fit_report()
    #print report
    #plt.figure(1)
    #plt.subplot(311)
    #plt.plot(t1, valuesOnX, "bo", t1, result.init_fit, "k--",t1, result.best_fit, 'r-')
    #start=report.find("[[Variables]]")
    #end=report.find("[[Correlations]]")
    #plt.text(1,50,report[start:])
    #plt.title("1mm cubes on x axis")
    #
    #pars=gmod.guess(valuesOnY,x=t1 )
    #result = gmod.fit(valuesOnY, pars,x=t1)
    #resultP=list(result.params.valuesdict().items())
    #report=result.fit_report()
    #print report
    #plt.subplot(312)
    #plt.plot(t1, valuesOnY, "bo", t1, result.best_fit, 'k')
    #start=report.find("[[Variables]]")
    #end=report.find("[[Correlations]]")
    #plt.text(1,50,report[start:])
    #plt.title("1mm cubes on y axis")
    #
    #pars=gmod.guess(valuesOnZ,x=t1 )
    #result = gmod.fit(valuesOnZ, pars,x=t1)
    #resultP=list(result.params.valuesdict().items())
    #report=result.fit_report()
    #print report
    #plt.subplot(313)
    #plt.plot(t1, valuesOnZ, "bo", t1, result.best_fit, 'k')
    #plt.text(1,50,report[start:])
    #start=report.find("[[Variables]]")
    #end=report.find("[[Correlations]]")
    #plt.title("1mm cubes on z axis")
    #
    #plt.show()

if __name__ == "__main__":
       main(sys.argv[1:])
