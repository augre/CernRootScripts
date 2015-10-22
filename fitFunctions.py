from numpy import sqrt, pi, exp, log

def gaussian(x, par0, par1):
    arg=(x[0]-par0)/par1 if par1!=0 else 0.0
    y= exp(-0.5*arg*arg)/(par1*sqrt(2.0*pi))
    return y

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

def findInverseValueTriple(y, par, fromx, tox):
    xStatus=0
    a=[0]
    for i in xrange(fromx, tox):
        a[0]=i
        if tripleGaussian(a, par) < y:
            xStatus=i
#            print "xstatus: ",xStatus," tripleV: ",tripleGaussian(a, par),"y: ",y
        else:
            break
    a[0]=xStatus
    while tripleGaussian(a, par)< y:
        a[0]+=.1
    a[0]-=.1
    while tripleGaussian(a, par)< y:
        a[0]+=.01
    a[0]-=.01
#    print "y eredmeny: ",tripleGaussian(a, par)
    return a
