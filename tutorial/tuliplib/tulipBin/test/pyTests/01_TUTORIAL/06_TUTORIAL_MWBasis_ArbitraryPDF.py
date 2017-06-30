# Imports
import sys
sys.path.insert(0, '../../py')

import tulipUQ as uq
import numpy as np
import matplotlib.pyplot as plt

# =============================
# PERFORM MW ORTHOGONALITY TEST
# =============================
def performMWOrthogonalityTest(grid,mwMat,measure):

  # Get Maximum Weight Order
  maxOrder = grid.getMaxWeightOrder()

  # Assumes the matrix is evaluated at a grid of integration points
  integral    = 0.0;
  firstBasis  = 0.0;
  secondBasis = 0.0;
  currMeasure = 0.0;
  intWeigth   = 0.0;
  currIDX     = 0;
  testIDX     = 0;
  print ''
  print 'MW ORTHOGONALITY TEST'
  print 'Number of Basis: %d' % (mwMat.getColCount())
  print 'Number of Samples: %d' % (mwMat.getRowCount())
  print ''
  
  for loopA in xrange(mwMat.getColCount()):
    
    for loopB in xrange(mwMat.getColCount()):
      
      integral = 0.0
      for loopC in xrange(mwMat.getRowCount()):
        
        firstBasis  = mwMat.getMatrixAt(loopC,loopA)
        secondBasis = mwMat.getMatrixAt(loopC,loopB)
        intWeigth   = grid.getWeightAt(loopC,maxOrder)
        currMeasure = 1.0
        currIDX = loopC
        
        for loopD in xrange(grid.getTotDims()):
          testIDX = currIDX % grid.getTotSamples()
          currMeasure *= measure[loopD][testIDX]
          currIDX = currIDX / grid.getTotSamples()

        integral += firstBasis * secondBasis * currMeasure * intWeigth

      print '%15.6e ' % (integral),

    print ''

  print ''

# ==========================
# SCALE 1D GRID ON PARTITION
# ==========================
def scale1DGridOnPartition(points,lb,ub,outLocs):
  sampleValue = 0.0;
  outLocs.clear();
  for loopA in xrange(points.getTotSamples()):
    sampleValue = points.getValuesAt(loopA,0)
    outLocs.push_back(lb + sampleValue * (ub-lb))

# =============
# MAIN FUNCTION
# =============
if __name__ == "__main__":

  # READ MARGINAL FROM FILE
  #approx = uq.uq1DApproximant_ME();
  #marginalFile = ""
  #error = approx.importFromTextFile(marginalFile)
  #if(error != 0):
  #  print 'ERROR: Cannot Read Approximant From File.'
  #  sys.exit(-1)
  
  # EVALUATE RANGE
  #tmpLimits = uq.stdVec()
  #approx.getExtremes(tmpLimits)
  #measureSize = fabs(tmpLimits[1] - tmpLimits[0])
  #print 'CURRENT LIMITS: %f %f' % (tmpLimits[0],tmpLimits[1])
  
  # FORM SAMPLES USING INTEGRATION GRID IN 1D
  mwOrder = 2
  mwQuadOrder = 30
  measure1DGridPoints = uq.uqSamples()
  measure1DGridPoints.addVariable('grid1D',uq.kSAMPLEUniform,0.0,1.0)
  measure1DGridPoints.generateCartesianGrid(mwQuadOrder,uq.kDoubleCC,uq.kHaarRange)

  intLocations = uq.stdVec()
  #scale1DGridOnPartition(measure1DGridPoints,tmpLimits[0],tmpLimits[1],intLocations);
  scale1DGridOnPartition(measure1DGridPoints,0.0,1.0,intLocations)

  # EVALUATE MARGINAL AT QUADRATURE POINTS
  measure = uq.stdMat()
  tmp = uq.stdVec()
  currInt = 0.0
  currLoc = 0.0
  currVal = 0.0
  for loopA in xrange(intLocations.size()):
    currLoc = intLocations[loopA]
    #currVal = approx.evaluate(currLoc);
    currVal = 1.0
    currInt += currVal * measure1DGridPoints.getWeightAt(loopA,measure1DGridPoints.getMaxWeightOrder())
    tmp.push_back(currVal)

  print 'CURRENT INTEGRAL: %f' % (currInt)
  for loopA in xrange(intLocations.size()):
    tmp[loopA] /= currInt
  measure.push_back(tmp)

  # CONSTRUCT MULTIWAVELET BASIS WITH MARGINAL    
  addLegendrePoly         = True
  addMW                   = True
  useBinPartitions        = True
  mwMatType               = uq.kMWFixedMaxDetailLevel
  mwMatIncludeNullColumns = True
  useExactMW              = False  
  maxColumns              = 0
  maxDetailLevel          = 0

  # FORM MW MATRIX
  mwMat = uq.uqMWMatrix(mwOrder,measure1DGridPoints,
                        addLegendrePoly,addMW,useBinPartitions,
                        mwMatType,mwMatIncludeNullColumns,
                        useExactMW,mwQuadOrder,measure,
                        maxColumns,maxDetailLevel)

  # Convert to Numpy
  mw = np.array(mwMat.getMatrix())
  xVals = uq.stdMat()
  measure1DGridPoints.getValues(xVals)
  xv = np.array(xVals)
  
  plt.plot(xv,mw)
  plt.show()

  # Perform Orthogonality Test
  performMWOrthogonalityTest(measure1DGridPoints,mwMat,measure)

