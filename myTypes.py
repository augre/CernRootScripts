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

    def fillUpAllVariables(self):
        """
        This goes calls all the methods that fill up the class's variables
        Warning: Only use it if you dont modify want to modify the objects after(like Rebin()) 
                 and only for initialization
        """
        self.loadFile()
        self.loadHist()
        self.getNbinsXYZ()
        self.getMinXYZ()
        self.getMaxXYZ()
        self.initTH2DforXYPlane()
        self.getXYPlane()
