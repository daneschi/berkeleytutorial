# Imports
import sys,math
sys.path.insert(0, '../')
import numpy as np
import matplotlib.pyplot as plt
from common import *

# READ PRESSURES AND FLOWS FROM FILE
qVals = np.loadtxt('Qgeneral')
pVals = np.loadtxt('Pgeneral')

# REMOVE SAMPLES FROM THE INITIAL TRANSIENT
qVals = qVals[50:,:]
pVals = pVals[50:,:]
  
# NORMALIZE DATA
maxP = np.max(pVals,axis=0)
minP = np.min(pVals,axis=0)
minP,maxP = makeSymmetric(minP,maxP)
pVals = normalizeColumns(pVals,minP,maxP)

# EXTRACT NUMBER OF SAMPLES AND OUTLETS
totSamples = qVals.shape[0]
totOutlets = qVals.shape[1]
totInputs  = pVals.shape[1]

# DECIDE NUMBER OF TRAINING AND TESTING SETS
trainSizeRatio = 0.67
trainSize = int(trainSizeRatio*totSamples)

# DETERMINE RANDOM INDEXES TO EXTRACT AND DO TRAINING/TESTING SEPARATION
indices = np.random.permutation(totSamples)
training_idx, test_idx = indices[:trainSize], indices[trainSize:]
pTrainVals, pTestVals = pVals[training_idx,:], pVals[test_idx,:]
qTrainVals, qTestVals = qVals[training_idx,:], qVals[test_idx,:]


# ASSEMBLE POLYNOMIAL MATRIX FROM TRAINING INPUT PRESSURES
pMat = buildRegressionMatrix(pTrainVals,2)
  
# OLS REGRESSION
ols = tulipOLS()
olsCoeffs,olsCoeffsCov,olsNoise = ols.train(pMat,qTrainVals[:,0])

# RVM REGRESSION
rvm = tulipRVM()
rvmCoeffs,rvmCoeffsCov,rvmNoise = rvm.train(pMat,qTrainVals[:,0])

# PERFORM TESTING
# Compute a Polynomial Matrix at the Testing Locations
pTestMat = np.array(buildRegressionMatrix(pTestVals,2).getMatrix())
# Compute the average reconstructed Qtys
olsQ = np.dot(pTestMat,olsCoeffs)
rvmQ = np.dot(pTestMat,rvmCoeffs)
# Compute the uncertainty region
olsAux = np.dot(np.dot(pTestMat,olsCoeffsCov),pTestMat.transpose())
rvmAux = np.dot(np.dot(pTestMat,rvmCoeffsCov),pTestMat.transpose())
shrink_idx = olsAux < 0
olsAux[shrink_idx] = 0.0
shrink_idx = rvmAux < 0.0
rvmAux[shrink_idx] = 0.0
olsSTDQ = olsNoise + np.sqrt(olsAux)
rvmSTDQ = rvmNoise + np.sqrt(rvmAux)

# Re-permute array in the correct temporal order
test  = computeInversePermutation(test_idx,qTestVals[:,0])
olsQ  = computeInversePermutation(test_idx,olsQ)
rvmQ  = computeInversePermutation(test_idx,rvmQ)
olsQ2 = computeInversePermutation(test_idx,np.diag(olsSTDQ))
rvmQ2 = computeInversePermutation(test_idx,np.diag(rvmSTDQ))

# Write Covariance in Matrix Form
plt.subplot(1,2,1)
plt.plot(np.arange(len(test)),test,'k--',label='Exact',alpha=0.6,lw=1.5)
plt.plot(np.arange(len(olsQ)),olsQ,'r-',label='OLS',alpha=0.6,lw=1.0)
plt.fill_between(np.arange(len(olsQ)),olsQ+olsQ2, olsQ-olsQ2,facecolor='gray',interpolate=True,alpha=0.6)
plt.xlabel('Simulation Step')
plt.ylabel('Flow Rate [cm$^3$/s]')
plt.subplot(1,2,2)
plt.plot(np.arange(len(test)),test,'k--',label='Exact',alpha=0.6,lw=1.5)
plt.plot(np.arange(len(rvmQ)),rvmQ,'b-',label='RVM',alpha=0.6,lw=1.0)
plt.fill_between(np.arange(len(rvmQ)),rvmQ+rvmQ2, rvmQ-rvmQ2,facecolor='gray',interpolate=True,alpha=0.6)
plt.xlabel('Simulation Step')
plt.ylabel('Flow Rate [cm$^3$/s]')
plt.show()
