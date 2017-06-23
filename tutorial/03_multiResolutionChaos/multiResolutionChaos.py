# Imports
import sys,math
sys.path.insert(0, '../')
import numpy as np
import matplotlib.pyplot as plt
from common import *

# Model Function
def runModel(xVals):
  return 1.0/(np.fabs(0.3 - np.square(xVals))+0.1)

# Plot a stochastic response with steep gradients
xExact = np.arange(500)/499.0
yExact = runModel(xExact)

# Plot Function
plt.plot(xExact,yExact,'r-')
plt.show()

# Random Polynomial OLS Regression 
np.random.seed(0)
# xVals = np.sort(np.random.rand(100))
xVals = np.arange(100)/99.0
yVals = runModel(xVals)

# Normalize Inputs
xTrain = np.resize(2.0*xVals - 1.0,(len(xVals),1))

# Init RVM Object
rvm = tulipRVM()

# Make Polynomial Regressions with RVM
for loopA in range(0,50,5):
  polyMat = buildRegressionMatrix(xTrain,loopA)
  rvmCoeffs,rvmCoeffsCov,rvmNoise = rvm.train(polyMat,yVals)
  plt.plot(xVals,np.dot(np.array(polyMat.getMatrix()),rvmCoeffs),'-',alpha=0.7,label='degree '+str(loopA))
plt.plot(xExact,yExact,'k-',alpha=0.8,label='Exact')
plt.legend()
plt.show()

# Make Polynomial Regressions with RVM
mwMat = buildMultiresolutionMatrix(np.resize(xVals,(len(xVals),1)))
rvmCoeffs,rvmCoeffsCov,rvmNoise = rvm.train(mwMat,yVals)
plt.plot(xVals,np.dot(np.array(mwMat.getMatrix()),rvmCoeffs),'o-',alpha=0.7,label='mw',markersize=3.0)
plt.plot(xExact,yExact,'k-',alpha=0.8,label='Exact')
plt.legend()
plt.show()
