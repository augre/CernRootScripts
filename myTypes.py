import ROOT

class Location:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class RootFile:
    def __init__(self, fn="Dosimetry_Detector_tot.root", hn="h3D_Dose_t"):
        """
        If no arguments are given to RootFile, the default is:
        Dosimetry_Detector_tot.root
        h3D_Dose_t
        """
        self.fileName=fn
        self.histName=hn
    def loadFile(self):
        self.fileObj=ROOT.TFile(self.fileName)
    def loadHist(self):
        self.histObj=self.fileObj.Get(self.histName)
    def getNbinsXYZ(self):
        self.binN=Location(self.histObj.GetNbinsX(),self.histObj.GetNbinsY(),self.histObj.GetNbinsZ())
    def getMinXYZ(self):
        self.minL=Location(self.histObj.GetXaxis().GetXmin(),self.histObj.GetYaxis().GetXmin(),self.histObj.GetZaxis().GetXmin())
    def getMaxXYZ(self):
        self.maxL=Location(self.histObj.GetXaxis().GetXmax(),self.histObj.GetYaxis().GetXmax(),self.histObj.GetZaxis().GetXmax())
    def initTH2DforXYPlane(self):
        self.rootValXY=ROOT.TH2D("xyPlane","xy plane",self.binN.x,self.minL.x,self.maxL.x,self.binN.y,self.minL.y,self.maxL.y)
    def getXYPlane(self):
        for y in range(0,self.binN.y):
            for x in range(0,self.binN.x):
                #print "y:",y,"x:",x
                binXY=self.histObj.GetBinContent(self.histObj.GetBin(x+1, y+1, self.binN.z/2))
                self.rootValXY.SetBinContent(self.rootValXY.GetBin(x+1,y+1), binXY)
                #print binXY
    def initTH2DforYZPlane(self):
        self.rootValYZ=ROOT.TH2D("yzPlane","yz plane",self.binN.z,self.minL.z,self.maxL.z,self.binN.y,self.minL.y,self.maxL.y)
    def getYZPlane(self):
        for y in range(0,self.binN.y):
            for z in range(0,self.binN.z):
                binYZ=self.histObj.GetBinContent(self.histObj.GetBin(self.binN.x/2, y+1, z+1))
                self.rootValYZ.SetBinContent(self.rootValXY.GetBin(z+1,y+1), binYZ)
    def writePlanesToPngFiles(self,currentDir):
        c2=ROOT.TCanvas("c2")
        ROOT.gStyle.SetOptStat(0)
        self.rootValXY.SetContour(10)
        self.rootValXY.DrawCopy("colz")
        h2=self.rootValXY.DrawClone("cont3 same")
        h2.SetLineColor(2)
        c2.Print(currentDir+"xyPlane.png")
        c2=ROOT.TCanvas("c2")
        ROOT.gStyle.SetOptStat(0)
        self.rootValYZ.SetContour(10)
        self.rootValYZ.DrawCopy("colz")
        h2=self.rootValYZ.DrawClone("cont3 same")
        h2.SetLineColor(2)
        c2.Print(currentDir+"yzPlane.png")
    def initTH1DforEachAxis(self):
        self.rootValX=ROOT.TH1D("valsX","Energy deposited in 1mm cubes on X axis", self.binN.x, self.minL.x, self.maxL.x)
        self.rootValY=ROOT.TH1D("valsY","Energy deposited in 1mm cubes on Y axis", self.binN.y, self.minL.y, self.maxL.y)
        self.rootValZ=ROOT.TH1D("valsZ","Energy deposited in 1mm cubes on Z axis", self.binN.z, self.minL.z, self.maxL.z)
    def getTH1DforEachAxis(self):
        for i in xrange(0,self.binN.x):
            self.rootValX.SetBinContent(i+1 ,self.histObj.GetBinContent(self.histObj.GetBin(i+1, self.binN.y/2, self.binN.z/2)))
        for i in xrange(0,self.binN.y):
            self.rootValY.SetBinContent(i+1 ,self.histObj.GetBinContent(self.histObj.GetBin(self.binN.x/2, i+1, self.binN.z/2)))
        for i in xrange(0,self.binN.z):
            self.rootValZ.SetBinContent(i+1 ,self.histObj.GetBinContent(self.histObj.GetBin(self.binN.x/2, self.binN.y/2, i+1)))
        self.rootValX.Sumw2()
        self.rootValY.Sumw2()
        self.rootValZ.Sumw2()
    def fillUpAllVariables(self):
        """
        This calls all the methods that fill up the class's variables
        Warning: Only use it if you dont want to modify the objects after(like Rebin()) 
                 and only for initialization
        """
        self.loadFile()
        self.loadHist()
        self.getNbinsXYZ()
        self.getMinXYZ()
        self.getMaxXYZ()
        self.initTH2DforXYPlane()
        self.getXYPlane()
        self.initTH2DforYZPlane()
        self.getYZPlane()
        self.initTH1DforEachAxis()
        self.getTH1DforEachAxis()
