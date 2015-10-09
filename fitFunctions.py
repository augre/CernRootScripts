from numpy import sqrt, pi, exp

def tripleGaussian(x, par):
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
