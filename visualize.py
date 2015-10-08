import ROOT
import numpy.testing as npt

f = ROOT.TFile("Dosimetry_Detector_tot.root")
hist3D=f.Get("h3D_Dose_t")
f.Print()

title="setHoles 5 "

binx=hist3D.GetNbinsX()
binx_c=binx/2
biny=hist3D.GetNbinsY()
biny_c=biny/2
binz=hist3D.GetNbinsZ()
binz_c=binz/2
minx=hist3D.GetXaxis().GetXmin()
miny=hist3D.GetYaxis().GetXmin()
minz=hist3D.GetZaxis().GetXmin()
maxx=hist3D.GetXaxis().GetXmax()
maxy=hist3D.GetYaxis().GetXmax()
maxz=hist3D.GetZaxis().GetXmax()
h2_sum_x = ROOT.TH2D("h2_sum_x","Cumulative yz-projection",biny,miny,maxy,binz,minz,maxz)
h2_sum_z = ROOT.TH2D("h2_sum_z","Cumulative xy-projection",binx,minx,maxx,biny,miny,maxy)
dose_max=hist3D.Project3D("xy").GetBinContent(hist3D.Project3D("xy").GetMaximumBin())


c1=ROOT.TCanvas("c1", title , 800, 800)
c1.Divide(2,2)

c1.cd(2)
hist2Dxy=hist3D.Project3D("xy")

h2_sum_z.Add(hist2Dxy,1.);

h2_sum_z.Smooth()
h2_sum_z.Smooth()
h2_sum_z.Smooth()

h2_sum_z.SetTitle(title+ "dose deposition xy projection")
h2_sum_z.DrawCopy("colz")
h2_sum_z.SetContour(10)
h2_sum_z.GetXaxis().SetTitle("Distance in mm")
h2_sum_z.Draw("cont3 same")

zmin = h2_sum_z.GetXaxis().GetXmin()
zmax = h2_sum_z.GetXaxis().GetXmax()
line_z=ROOT.TLine(zmin,0,zmax,0)
line_z.SetLineColor(ROOT.kViolet)
line_z.Draw("same")
lineXY_90=ROOT.TLine(-10,-80, -10,0)
lineXY_90.Draw("same")
lineXY_90p=ROOT.TLine(10,-80, 10,0)
lineXY_90p.Draw("same")


c1.cd(1)
hist2Dxy=hist3D.Project3D("yz")

h2_sum_x.Add(hist2Dxy,1.);

h2_sum_x.Smooth()
h2_sum_x.Smooth()
h2_sum_x.Smooth()

h2_sum_x.SetTitle(title+"dose deposition yz projection")
h2_sum_x.DrawCopy("colz")
h2_sum_x.SetContour(10)
h2_sum_x.GetXaxis().SetTitle("Distance in mm")
h2_sum_x.Draw("cont3 same")

xmin = h2_sum_x.GetXaxis().GetXmin()
xmax = h2_sum_x.GetXaxis().GetXmax()
line_x=ROOT.TLine(xmin,0,xmax,0)
line_x.SetLineColor(ROOT.kRed)
line_x.Draw("same")
lineYZ_90=ROOT.TLine(-8.5,-80, -8.5,0)
lineYZ_90.Draw("same")
lineYZ_90p=ROOT.TLine(7.5,-80, 7.5,0)
lineYZ_90p.Draw("same")
lineYZ_50=ROOT.TLine(-17,-80, -17,0)
lineYZ_50.Draw("same")
lineYZ_50p=ROOT.TLine(17,-80, 17,0)
lineYZ_50p.Draw("same")


c1.cd(4)
projZ=h2_sum_z.ProjectionX("Profile z-axis",binz_c,binz_c)#.Clone("projX")
projZ.SetTitle("Profile z-axis; Position [u.u]; Intensity [u.u]")
projZ.GetXaxis().SetTitle("Distance in mm")
projZ.SetLineColor(ROOT.kViolet)
projZ.Draw()
maxiZ=projZ.GetMaximum()
print "maxiZ=",maxiZ
lineZ_90=ROOT.TLine(-10,0, -10, maxiZ*.9)
lineZ_90.Draw("same")
lineZ_90p=ROOT.TLine(10,0, 10, maxiZ*.9)
lineZ_90p.Draw("same")

c1.cd(3)
projX=h2_sum_x.ProjectionX("Profile x-axis",binx_c,binx_c)
projX.SetTitle("Profile x-axis; Position [u.u]; Intensity [u.u]")
projX.GetXaxis().SetTitle("Distance in mm")
projX.SetLineColor(ROOT.kRed)
projX.Draw()
maxiX=projX.GetMaximum()
print "maxiX=",maxiX
lineX_90=ROOT.TLine(-8.5,0, -8.5, maxiX*.9)
lineX_90.Draw("same")
lineX_90p=ROOT.TLine(7.5,0,  7.5, maxiX*.9)
lineX_90p.Draw("same")
lineX_50=ROOT.TLine(-17,0, -17, maxiX*.5)
lineX_50.Draw("same")
lineX_50p=ROOT.TLine(17,0,  17, maxiX*.5)
lineX_50p.Draw("same")
