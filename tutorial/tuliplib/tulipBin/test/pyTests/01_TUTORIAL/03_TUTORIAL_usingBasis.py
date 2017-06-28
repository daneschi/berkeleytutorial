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

  # SET PARAMETERS
  steps     = 100
  currOrder = 3

  # Allocate Result
  results = np.zeros((steps,5))

  # SIMPLE POLYNOMIALS
  polyIntMonomial = uq.uqPolyBasis(uq.kPolyMonomials,currOrder+1)
  polyIntLegendre = uq.uqPolyBasis(uq.kPolyLegendre,currOrder+1)
  polyIntHermite  = uq.uqPolyBasis(uq.kPolyHermite,currOrder+1)

  currentLoc = 0.0
  for loopA in xrange(steps):
    currentLoc = loopA/float(steps - 1)
    results[loopA,0] = polyIntMonomial.evaluate(currentLoc,currOrder)
    results[loopA,1] = polyIntLegendre.evaluate(currentLoc,currOrder)
    results[loopA,2] = polyIntHermite.evaluate(currentLoc,currOrder)

  # ORTHOGONAL POLYNOMIALS
  # Define the number of quadrature points
  quadLevel = 10

  # Define the Uniform Measure
  measureAtQuadPoints = uq.stdVec(2*quadLevel,0.0)
  for loopA in xrange(2*quadLevel):
    measureAtQuadPoints[loopA] = 1.0

  orthoPoly = uq.uqOrthoPolyBasis(currOrder+1,quadLevel,measureAtQuadPoints)
  
  currentLoc = 0.0;
  for loopA in xrange(steps):
    currentLoc = loopA/float(steps - 1)
    results[loopA,3] = orthoPoly.evaluate(currentLoc,currOrder)

  # MULTIWAVELETS
  mwInt = uq.uqMWBasis(currOrder+1,quadLevel)
  currentLoc = 0.0
  for loopA in xrange(steps):
    currentLoc = loopA/float(steps - 1)
    results[loopA,4] = mwInt.EvalMotherMW(currentLoc,currOrder)

  # PLOT BASIS
  xVals = np.arange(steps)/float(steps - 1)
  print results
  plt.plot(xVals,results[:,0],label='monomial')
  plt.plot(xVals,results[:,1],label='Legendre')
  plt.plot(xVals,results[:,2],label='Hermite')
  plt.plot(xVals,results[:,3],label='orthoPolyLegendre')
  plt.plot(xVals,results[:,4],label='mw')
  plt.legend()
  plt.show()

