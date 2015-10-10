#!/usr/bin/env python
import sys, getopt
import ROOT
import numpy.testing as npt
from myTypes import RootFile

def main(argv):
    f = RootFile()
    f.fillUpAllVariables()
    f.fileObj.Print()
    
    title="title..."
    
    
    h2_sum_x = ROOT.TH2D("h2_sum_x","Cumulative yz-projection",f.binN.y,f.minL.y,f.maxL.y,f.binN.z,f.minL.z,f.maxL.z)
    h2_sum_y = ROOT.TH2D("h2_sum_y","Cumulative xz-projection",f.binN.x,f.minL.x,f.maxL.x,f.binN.z,f.minL.z,f.maxL.z)
    h2_sum_z = ROOT.TH2D("h2_sum_z","Cumulative xy-projection",f.binN.x,f.minL.x,f.maxL.x,f.binN.y,f.minL.y,f.maxL.y)
    dose_max=f.histObj.Project3D("xy").GetBinContent(f.histObj.Project3D("xy").GetMaximumBin())
    
    
    c1=ROOT.TCanvas("c1", title ,1200,1200)
    c1.Divide(3,2)

    c1.cd(1)
    hist2Dxy=f.histObj.Project3D("yz")
    
    h2_sum_x.Add(hist2Dxy,1.);
    
    h2_sum_x.Smooth()
#    h2_sum_x.Smooth()
#    h2_sum_x.Smooth()
    
    h2_sum_x.SetTitle(title+"dose deposition yz projection")
    h2_sum_x.DrawCopy("colz")
    h2_sum_x.SetContour(10)
    h2_sum_x.GetXaxis().SetTitle("Distance in mm")
    h2_sum_x.Draw("cont3 same")
    
    xmin = h2_sum_x.GetXaxis().GetXmin()
    xmax = h2_sum_x.GetXaxis().GetXmax()
    line_x=ROOT.TLine(xmin,0,xmax,0)
    line_x.SetLineColor(ROOT.kRed)
    line_x.Draw()

    c1.cd(2)
    hist2Dxz=f.histObj.Project3D("yz")
    
    h2_sum_y.Add(hist2Dxy,1.);
    
    h2_sum_y.Smooth()
#    h2_sum_x.Smooth()
#    h2_sum_x.Smooth()
    
    h2_sum_y.SetTitle(title+"dose deposition yz projection")
    h2_sum_y.DrawCopy("colz")
    h2_sum_y.SetContour(10)
    h2_sum_y.GetXaxis().SetTitle("Distance in mm")
    h2_sum_y.Draw("cont3 same")
    
    xmin = h2_sum_y.GetXaxis().GetXmin()
    xmax = h2_sum_y.GetXaxis().GetXmax()
    line_x=ROOT.TLine(xmin,0,xmax,0)
    line_x.SetLineColor(ROOT.kRed)
    line_x.Draw()

    c1.cd(3)
    hist2Dxy=f.histObj.Project3D("xy")
    
    h2_sum_z.Add(hist2Dxy,1.);
    
    h2_sum_z.Smooth()
#    h2_sum_z.Smooth()
#    h2_sum_z.Smooth()
    
    h2_sum_z.SetTitle(title+ "dose deposition xy projection")
    h2_sum_z.DrawCopy("colz")
    h2_sum_z.SetContour(10)
    h2_sum_z.GetXaxis().SetTitle("Distance in mm")
    h2_sum_z.Draw("cont3 same")
    
    zmin = h2_sum_z.GetXaxis().GetXmin()
    zmax = h2_sum_z.GetXaxis().GetXmax()
    line_z=ROOT.TLine(zmin,0,zmax,0)
    line_z.SetLineColor(ROOT.kViolet)
    line_z.Draw()
    
    c1.cd(4)
    projX=h2_sum_x.ProjectionX("Profile x-axis",f.binN.x/2,f.binN.x/2)
    projX.SetTitle("Profile x-axis; Position [u.u]; Intensity [u.u]")
    projX.GetXaxis().SetTitle("Distance in mm")
    projX.SetLineColor(ROOT.kRed)
    projX.Draw()
    maxiX=projX.GetMaximum()
    print "maxiX=",maxiX
    
    c1.cd(5)
    projX=h2_sum_y.ProjectionX("Profile y-axis",f.binN.y/2,f.binN.y/2)
    projX.SetTitle("Profile x-axis; Position [u.u]; Intensity [u.u]")
    projX.GetXaxis().SetTitle("Distance in mm")
    projX.SetLineColor(ROOT.kRed)
    projX.Draw()
    maxiX=projX.GetMaximum()
    print "maxiX=",maxiX


    c1.cd(6)
    projZ=h2_sum_z.ProjectionX("Profile z-axis",f.binN.z/2,f.binN.z/2)#.Clone("projX")
    projZ.SetTitle("Profile z-axis; Position [u.u]; Intensity [u.u]")
    projZ.GetXaxis().SetTitle("Distance in mm")
    projZ.SetLineColor(ROOT.kViolet)
    projZ.Draw()
    maxiZ=projZ.GetMaximum()
    print "maxiZ=",maxiZ
        

    
    c1.Print("doesline.png")

if __name__ == "__main__":
       main(sys.argv)
