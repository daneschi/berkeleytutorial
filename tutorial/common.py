# Import tulip
import sys
sys.path.insert(0, '../tuliplib/tulipBin/py') # path relative to location of the notebook that loads common.py
import numpy as np
# Import UQ Library
import tulipUQ as uq
# Import Computational Model Library
import tulipCM as cm
# Import Data Library
import tulipDA as da
# Import Action Library
import tulipAC as ac

def npToStdMat(npMat):
  res = uq.stdMat()
  aux = uq.stdVec()
  for loopA in range(npMat.shape[1]):
    aux.clear()
    for loopB in range(npMat.shape[0]):
      aux.push_back(npMat[loopB,loopA])
    res.push_back(aux)
  return res

def makeSymmetric(minP,maxP):
  if(len(minP) != len(maxP)):
    print ('ERROR: Incompatible pVal Extremes.')
    sys.exit(-1)
  for loopA in range(len(minP)):
    if(np.fabs(maxP[loopA])>np.fabs(minP[loopA])):
      minP[loopA] = -np.fabs(maxP[loopA])
    else:
      maxP[loopA] = np.fabs(minP[loopA])
  # Return Modified Extremes
  return minP,maxP

def normalizeColumns(pVals,minP,maxP):
  for loopA in range(pVals.shape[1]):
    minVal = minP[loopA]
    maxVal = maxP[loopA]
    for loopB in range(pVals.shape[0]):
      pVals[loopB,loopA] = 2.0*((pVals[loopB,loopA]-minVal)/(maxVal-minVal))-1.0
  # Return
  return pVals;

def buildRegressionMatrix(pTrainVals,ord):
  # Construct samples
  samples = uq.uqSamples(pTrainVals.shape[1])
  currSample = uq.stdVec()
  for loopA in range(pTrainVals.shape[0]):
    currSample.clear()
    for loopB in range(pTrainVals.shape[1]):
      currSample.push_back(pTrainVals[loopA,loopB])
    samples.addOneSample(currSample)
  # Construct Polynomial Matrix on samples
  polyMat = uq.uqPolyMatrix(samples,ord,uq.kPolyLegendre,uq.kMIPartialOrder)
  # Return Matrix
  return polyMat

def buildMultiresolutionMatrix(xTrain,maxOrder,maxDetailLevel):
  # Construct samples
  samples = uq.uqSamples(xTrain.shape[1])
  currSample = uq.stdVec()
  for loopA in range(xTrain.shape[0]):
    currSample.clear()
    for loopB in range(xTrain.shape[1]):
      currSample.push_back(xTrain[loopA,loopB])
    samples.addOneSample(currSample)

  # Set Parameters for multiresolution basis
  maxOrder                = maxOrder
  addLegendrePoly         = True
  addMW                   = True
  useBinaryPartitions     = False
  mwMatType               = uq.kMWFixedMaxDetailLevel
  mwMatIncludeNullColumns = True
  useExactMW              = False
  mwQuadOrder             = 10
  measure                 = npToStdMat(np.ones((2*mwQuadOrder,1)))
  # print np.array(measure)
  maxColumns              = 0
  maxDetailLevel          = maxDetailLevel

  # Construct Multiresolution Matrix on samples
  mwMat = uq.uqMWMatrix(maxOrder,samples, \
                        addLegendrePoly,addMW,useBinaryPartitions, \
                        mwMatType,mwMatIncludeNullColumns, \
                        useExactMW,mwQuadOrder,measure, \
                        maxColumns,maxDetailLevel)
  # Return Matrix
  return mwMat

# TRAIN WITH OLS
class tulipOLS:
  def __init__(self):
    self.outletNum = 0
    pass
  def train(self,pMat,qTrainVals):
    npMat = np.array(pMat.getMatrix())
    coeffs = np.linalg.lstsq(npMat,qTrainVals)[0]
    # Compute Train Error Vector
    trainError = qTrainVals - np.dot(npMat,coeffs)
    # Compute Noise Estimate 
    if(npMat.shape[0]-npMat.shape[1] > 0):
      noiseEstimate = np.sqrt(np.sum(np.square(trainError))/(npMat.shape[0]-npMat.shape[1]))
    else:
      noiseEstimate = 0.0
    # OLS Estimate of the coefficient Covariance
    coeffsCov = noiseEstimate * noiseEstimate * np.linalg.inv(np.dot(npMat.transpose(),npMat))
    # Return
    return coeffs,coeffsCov,noiseEstimate

# TRAIN WITH RVM
class tulipRVM:
  def __init__(self):
    pass

  def train(self,pMat,qTrainVals):
    # Eval functional value with simple function
    rhs = uq.stdVec()
    for loopA in range(len(qTrainVals)):
      rhs.push_back(qTrainVals[loopA])
    
    # Construct the regression algorithm
    bcs = uq.uqAlgorithmBCS();
    # Set options: Print Progress to screen
    bcs.opts.printProgressToScreen = True;
    bcs.opts.printDBGMessages      = False;
    bcsCoeffs = uq.stdVec()
    coeffPrec = uq.stdMat()
    resNorm = 0.0
    bcsReturn = bcs.run(pMat.getRowCount(),pMat.getColCount(), 
                        rhs,pMat.getMatrix(),
                        bcsCoeffs,coeffPrec,resNorm);

    # Print coefficients on screen
    coeffs = np.array(bcsCoeffs)
    # Return
    return np.array(bcsCoeffs),np.array(coeffPrec),bcsReturn

# Compute the Inverse Permutation of a given array given the partition indices
def computeInversePermutation(idx,vector):
  res = np.zeros(np.max(idx)+1)
  mask = np.zeros(len(res), dtype=bool)
  mask[idx] = True
  res[idx] = vector
  return res[mask]
