from numpy import sqrt, pi, exp, log
from ROOT import TMath as rm

def gaussian(x, par0, par1):
    arg=(x[0]-par0)/par1 if par1!=0 else 0.0
    y= exp(-0.5*arg*arg)/(par1*sqrt(2.0*pi))
    return y

def voigt(x, par):
    y=rm.Voigt(x[0], par[1], par[2])
    return par[0]*y

def inverseGaussian(y, par1, par2):
    arg=sqrt(log(y)*par1*sqrt(2*pi)/-0.5)
    x=arg*par1+par0
    return x

def tripleGaussian(x, par):
    """
    The fit function to determine the parameters of the sum of three Gaussians
    """
    g1=gaussian(x, par[1], par[2])
    g2=gaussian(x, par[3], par[4])
    g3=gaussian(x, par[5], par[6])
    y=par[0]*(par[7]*g1 + par[8]*g2 + (1-par[7]-par[8])*g3)

    return y


def inverseTripleGaussian(y, par):
    pass

def findInverseValue(func, y, par, fromx, tox,step=1):
    xStatus=0
    a=[0]
    for i in xrange(fromx, tox, step):
        a[0]=i
        if func(a, par) < y:
            xStatus=i
#            print "xstatus: ",xStatus," tripleV: ",func(a, par),"y: ",y
        else:
            break
    a[0]=xStatus
    while func(a, par)< y:
        a[0]=a[0]+.1 if step > 0 else a[0]-.1
    a[0]=a[0]-.1 if step > 0 else a[0]+.1
    while func(a, par)< y:
        a[0]=a[0]+.01 if step > 0 else a[0]-.01
    a[0]=a[0]-.01 if step > 0 else a[0]+.01
#    print "y eredmeny: ",func(a, par)
    return a
