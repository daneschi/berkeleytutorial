# Imports
import sys
sys.path.insert(0, '../../py')

import tulipUQ as uq
import numpy as np
import matplotlib.pyplot as plt

# =============
# MAIN FUNCTION
# =============
if __name__ == "__main__":

  # Create an 1D multi-element approximant file
  currApprox = uq.uq1DApproximant_ME()

  # Import the multi-element approximant from a file
  marginalFile = 'marginal_0.txt'
  error = currApprox.importFromTextFile(marginalFile)
  if(error != 0):
    print 'ERROR: Cannot Read Approximant From File.'
    sys.exit(-1)

  # Evaluate Extremes
  limits = stdVec()
  currApprox.getExtremes(limits)
  numberOfPoints = 100
  xVals = stdVec()
  currVal = 0.0
  for loopA in xrange(numberOfPoints):
    currVal = limits[0] + (((loopA)/(double)(numberOfPoints-1)))*(limits[1] - limits[0])
    xVals.push_back(currVal)

  # Eval all Points
  yVals = stdVec()
  currApprox.evaluate(xVals,yVals)

  # Write Vectors to Screen
  npX = np.array(xVals)
  print 'npX: ',npX
  npY = np.array(yVals)
  print 'npY: ',npY

  
  