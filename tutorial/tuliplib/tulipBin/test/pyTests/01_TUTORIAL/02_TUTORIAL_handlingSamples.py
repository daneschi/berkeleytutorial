# Imports
import sys
sys.path.insert(0, '../../py')

import tulipUQ as uq
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

  # Construct three sample objects
  randomSamples        = uq.uqSamples()
  sparseGridSamples    = uq.uqSamples()
  cartesianGridSamples = uq.uqSamples()

  # Add variables to random sampling
  randomSamples.addVariable('Var1',uq.kSAMPLEUniform,0.0,1.0)
  randomSamples.addVariable('Var2',uq.kSAMPLEUniform,0.0,1.0)
  randomSamples.generateRandomSamples(100)
  s1 = uq.stdMat()
  randomSamples.getValues(s1);
  npS1 = np.array(s1)

  # Add variables to sparse grid samples
  sparseGridSamples.addVariable('Var1',uq.kSAMPLEUniform,0.0,1.0)
  sparseGridSamples.addVariable('Var2',uq.kSAMPLEUniform,0.0,1.0)
  sparseGridSamples.generateSparseGrid(5)
  s2 = uq.stdMat()
  sparseGridSamples.getValues(s2);
  npS2 = np.array(s2)

  # Add variables to Cartesian grid samples
  cartesianGridSamples.addVariable('Var1',uq.kSAMPLEUniform,0.0,1.0)
  cartesianGridSamples.addVariable('Var2',uq.kSAMPLEUniform,0.0,1.0)
  cartesianGridSamples.generateCartesianGrid(20,uq.kCC,uq.kHaarRange)
  s3 = uq.stdMat()
  cartesianGridSamples.getValues(s3);
  npS3 = np.array(s3)

  plt.scatter(npS1[:,0],npS1[:,1],lw=0,alpha=0.7,c='g')
  plt.scatter(npS2[:,0],npS2[:,1],lw=0,alpha=0.7,c='b')
  plt.scatter(npS3[:,0],npS3[:,1],lw=0,alpha=0.7,c='k')
  plt.show()
