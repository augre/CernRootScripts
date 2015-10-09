import ROOT

class Location:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class RootFile:
    def __init__(self, fn="Dosimetry_Detector_tot.root", hn="h3D_Dose_t"):
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
    def fillUpAllVariables(self):
        self.loadFile()
        self.loadHist()
        self.getNbinsXYZ()
        self.getMinXYZ()
        self.getMaxXYZ()
